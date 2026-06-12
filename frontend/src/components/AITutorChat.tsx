import React, { useState, useRef, useEffect } from 'react';
import { API_BASE_URL } from '../config';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface AITutorChatProps {
  topicName: string;
  token: string | null;
}

const AITutorChat: React.FC<AITutorChatProps> = ({ topicName, token }) => {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: `Hi there! I am your AI learning buddy. Ask me anything about ${topicName}! Try asking 'Why does it happen?' or 'How does it work?'` }
  ]);
  const [userInput, setUserInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [speakingIdx, setSpeakingIdx] = useState<number | null>(null);

  const chatBottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const newMsg: Message = { role: 'user', content: text };
    setMessages(prev => [...prev, newMsg]);
    setUserInput('');
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE_URL}/tutor/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          topic_name: topicName,
          messages: [...messages, newMsg]
        })
      });
      const data = await res.json();

      setMessages(prev => [...prev, { role: 'assistant', content: data.reply }]);
    } catch (err) {
      console.error('Tutor chat failed:', err);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Oops! I had a little hiccup. Could you ask me again? 🧠' }]);
    } finally {
      setLoading(false);
    }
  };

  // Mock Speech-to-Text input
  const triggerVoiceListen = () => {
    setIsListening(true);
    setTimeout(() => {
      setIsListening(false);
      const voiceQuestions = [
        "Why is this topic important?",
        "Can you explain it again with an example?",
        "How does this relate to science?",
        "Can you give me a real-world application?"
      ];
      const selected = voiceQuestions[Math.floor(Math.random() * voiceQuestions.length)];
      setUserInput(selected);
    }, 2000);
  };

  // Mock Text-to-Speech reader
  const speakMessage = (content: string, idx: number) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      setSpeakingIdx(idx);

      const utterance = new SpeechSynthesisUtterance(content);
      utterance.rate = 0.95; // child speed
      utterance.pitch = 1.1; // friendly voice

      utterance.onend = () => {
        setSpeakingIdx(null);
      };

      window.speechSynthesis.speak(utterance);
    } else {
      // Basic fallback animation
      setSpeakingIdx(idx);
      setTimeout(() => setSpeakingIdx(null), 3000);
    }
  };

  return (
    <div className="bg-slate-50 border-2 border-brand-200 rounded-kids p-4 h-[500px] flex flex-col shadow-inner">
      {/* Messages Window */}
      <div className="flex-grow overflow-y-auto space-y-4 mb-4 pr-2">
        {messages.map((m, i) => (
          <div
            key={`msg-${i}`}
            className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`max-w-[80%] p-4 rounded-2xl text-sm relative ${m.role === 'user'
                ? 'bg-brand-500 text-white rounded-br-none'
                : 'bg-white border border-slate-200 text-slate-700 rounded-bl-none shadow-sm'
              }`}>
              <p>{m.content}</p>

              {/* Voice playback for assistant messages */}
              {m.role === 'assistant' && (
                <button
                  onClick={() => speakMessage(m.content, i)}
                  className="absolute bottom-1 right-2 text-brand-400 hover:text-brand-600 p-1 rounded-full text-xs font-bold"
                  title="Listen to lesson"
                >
                  {speakingIdx === i ? '🔊 Speaking...' : '🗣️ Listen'}
                </button>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-white border border-slate-200 text-slate-400 p-4 rounded-2xl rounded-bl-none text-sm shadow-sm italic font-bold">
              🤔 Buddy is thinking...
            </div>
          </div>
        )}
        <div ref={chatBottomRef} />
      </div>

      {/* Input bar */}
      <form
        onSubmit={(e) => { e.preventDefault(); handleSendMessage(userInput); }}
        className="flex gap-2 items-center"
      >
        <button
          type="button"
          onClick={triggerVoiceListen}
          className={`p-3 rounded-xl border-2 font-bold shadow-md transition transform active:scale-95 text-lg ${isListening
              ? 'bg-red-500 border-red-500 text-white animate-pulse'
              : 'bg-cyan-500 border-cyan-500 hover:bg-cyan-600 text-white'
            }`}
          title="Ask by voice"
        >
          {isListening ? '🎙️ Listening...' : '🎤 Ask by Voice'}
        </button>

        <input
          type="text"
          className="flex-grow px-4 py-3 border-2 border-slate-200 focus:border-brand-400 rounded-xl outline-none transition text-sm font-semibold"
          placeholder="Ask your AI tutor a question..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
        />

        <button
          type="submit"
          className="px-6 py-3 bg-brand-500 hover:bg-brand-600 text-white font-bold rounded-xl shadow-md transition transform active:scale-95 text-sm"
        >
          Send 🚀
        </button>
      </form>
    </div>
  );
};

export default AITutorChat;
