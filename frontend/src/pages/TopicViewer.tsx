import React, { useState, useEffect } from 'react';
import MindMap from '../components/MindMap';
import Flowchart from '../components/Flowchart';
import AITutorChat from '../components/AITutorChat';
import QuizComponent from '../components/QuizComponent';
import { API_BASE_URL } from '../config';

interface TopicViewerProps {
  topic: { id: number; name: string };
  token: string | null;
  onBack: () => void;
}

const TopicViewer: React.FC<TopicViewerProps> = ({ topic, token, onBack }) => {
  const [content, setContent] = useState<any>(null);
  const [quizzes, setQuizzes] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'learn' | 'mindmap' | 'flowchart' | 'concept' | 'flashcards' | 'tutor' | 'quiz'>('learn');
  const [expLevel, setExpLevel] = useState<'Beginner' | 'Intermediate' | 'Advanced'>('Beginner');
  
  // Flashcard flipper state
  const [fcIdx, setFcIdx] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);

  // OCR simulation state
  const [ocrFile, setOcrFile] = useState<File | null>(null);
  const [ocrLoading, setOcrLoading] = useState(false);
  const [ocrResult, setOcrResult] = useState<any>(null);

  // Load Content
  useEffect(() => {
    const fetchContent = async () => {
      setLoading(true);
      try {
        // We use topic ID if valid (>0), otherwise resolve by name using backend fallback mapping
        // Fetch topic details first if ID is 0 (came from dashboard click)
        let topicId = topic.id;
        if (topicId === 0) {
          const tRes = await fetch(`${API_BASE_URL}/topics/0?name=${encodeURIComponent(topic.name)}`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          // For simplicity, we can load content directly or fallback
        }

        const res = await fetch(`${API_BASE_URL}/topics/${topicId}/content`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setContent(data);
        }
        
        // Pre-fetch quizzes
        const qRes = await fetch(`${API_BASE_URL}/topics/${topicId}/quizzes`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (qRes.ok) {
          const qData = await qRes.json();
          setQuizzes(qData);
        }
      } catch (err) {
        console.error('Error fetching topic content:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, [topic, token]);

  const handleSpeech = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.95;
      utterance.pitch = 1.1;
      window.speechSynthesis.speak(utterance);
    }
  };

  const handleOcrSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ocrFile) return;
    setOcrLoading(true);
    setOcrResult(null);

    const formData = new FormData();
    formData.append('image', ocrFile);

    try {
      const res = await fetch(`${API_BASE_URL}/tutor/ocr`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      if (res.ok) {
        const data = await res.json();
        setOcrResult(data);
      }
    } catch (err) {
      console.error('OCR process failed:', err);
    } finally {
      setOcrLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-24 text-slate-400 font-bold">
        ⏳ Drawing visual diagrams and preparing lessons...
      </div>
    );
  }

  if (!content) {
    return (
      <div className="text-center py-20 bg-white rounded-kids border-2 border-slate-100 p-8">
        <p className="text-red-500 font-bold">⚠️ Error loading lesson contents.</p>
        <button onClick={onBack} className="mt-4 px-6 py-2 bg-brand-500 text-white rounded-xl">Back</button>
      </div>
    );
  }

  // Active Explanations text
  const currentExplanation = 
    expLevel === 'Beginner' ? content.beginner_explanation :
    expLevel === 'Intermediate' ? content.intermediate_explanation :
    content.advanced_explanation;

  const currentFlashcard = content.flashcards && content.flashcards[fcIdx];

  return (
    <div className="space-y-6">
      {/* Top Breadcrumb Header */}
      <div>
        <button 
          onClick={onBack}
          className="text-slate-500 font-bold hover:text-slate-700 flex items-center gap-1 text-sm transition"
        >
          ⬅️ Back to explorer
        </button>
        <h2 className="brand-title text-3xl text-slate-800 mt-2">
          {topic.name}
        </h2>
      </div>

      {/* Tabs list controls */}
      <div className="flex border-b border-indigo-100 flex-wrap gap-2">
        {[
          { id: 'learn', label: '📖 Learn Story' },
          { id: 'mindmap', label: '🌐 Mind Map' },
          { id: 'flowchart', label: '🗺️ Flowchart' },
          { id: 'concept', label: '📊 Concept Map' },
          { id: 'flashcards', label: '🎴 Flashcards' },
          { id: 'tutor', label: '🗣️ AI Tutor' },
          { id: 'quiz', label: '✏️ Quiz Challenge' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`px-4 py-2.5 font-bold text-sm rounded-t-xl transition ${
              activeTab === tab.id
                ? 'bg-brand-500 text-white shadow-sm'
                : 'text-slate-500 hover:bg-slate-50'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Panels */}
      <div className="mt-6">
        {/* LEARN TAB */}
        {activeTab === 'learn' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left explanation card */}
            <div className="lg:col-span-2 bg-white p-6 rounded-kids border border-slate-100 shadow-sm space-y-6">
              {/* Level selector dials */}
              <div className="flex gap-2 bg-slate-50 p-1 rounded-xl w-fit border border-slate-200">
                {(['Beginner', 'Intermediate', 'Advanced'] as const).map(lvl => (
                  <button
                    key={lvl}
                    onClick={() => setExpLevel(lvl)}
                    className={`px-4 py-1.5 rounded-lg text-xs font-bold transition ${
                      expLevel === lvl
                        ? 'bg-white text-brand-600 shadow-sm border border-slate-200'
                        : 'text-slate-500 hover:text-slate-700'
                    }`}
                  >
                    {lvl} {lvl === 'Beginner' ? '👶' : lvl === 'Intermediate' ? '🧒' : '🎓'}
                  </button>
                ))}
              </div>

              {/* Text area */}
              <div className="prose max-w-none">
                <p className="text-slate-600 leading-relaxed font-medium text-base">
                  {currentExplanation}
                </p>
              </div>

              {/* Speech reader button */}
              <button
                onClick={() => handleSpeech(currentExplanation)}
                className="px-5 py-2.5 bg-cyan-50 hover:bg-cyan-100 text-cyan-700 border-2 border-cyan-100 rounded-xl font-bold text-sm flex items-center gap-2 transition active:scale-95"
              >
                🔊 Read Aloud! (Voice Learning)
              </button>

              {/* Real world examples */}
              {content.real_world_examples && (
                <div className="border-t border-slate-100 pt-6">
                  <h4 className="font-extrabold text-slate-700 text-sm mb-3">🌟 Real-World Examples:</h4>
                  <ul className="list-disc pl-5 space-y-2 text-xs text-slate-500 font-semibold">
                    {content.real_world_examples.map((ex: string, idx: number) => (
                      <li key={idx}>{ex}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Right column: Infographic facts + OCR uploads */}
            <div className="space-y-6">
              {/* Infographics */}
              {content.infographic && (
                <div className="bg-gradient-to-br from-amber-500 to-amber-600 text-white p-6 rounded-kids shadow-md space-y-4">
                  <h3 className="brand-title text-xl">💡 Quick Facts Infographic</h3>
                  <div className="space-y-3">
                    {content.infographic.facts?.map((f: string, i: number) => (
                      <div key={i} className="flex gap-2 items-start text-xs font-bold">
                        <span>✨</span>
                        <p>{f}</p>
                      </div>
                    ))}
                    {content.infographic.statistics?.map((stat: string, i: number) => (
                      <div key={`stat-${i}`} className="bg-white/10 p-2.5 rounded-xl border border-white/10 text-xs font-extrabold flex gap-2">
                        <span>📈</span>
                        <p>{stat}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* OCR textbook uploader */}
              <div className="bg-white p-6 border-2 border-dashed border-brand-200 rounded-kids shadow-sm space-y-4">
                <h3 className="brand-title text-base text-brand-600">📸 Scan Textbook / Notes</h3>
                <p className="text-slate-400 font-semibold text-xs">Upload notes page, book page, or diagram image to generate summaries.</p>
                
                <form onSubmit={handleOcrSubmit} className="space-y-2">
                  <input 
                    type="file" 
                    accept="image/*"
                    className="w-full text-xs text-slate-500 file:mr-2 file:py-1 file:px-3 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-brand-50 file:text-brand-600"
                    onChange={(e) => setOcrFile(e.target.files?.[0] || null)}
                  />
                  <button 
                    type="submit"
                    disabled={!ocrFile || ocrLoading}
                    className="w-full py-2 bg-brand-500 hover:bg-brand-600 text-white font-bold rounded-xl text-xs active:scale-95 transition disabled:opacity-50"
                  >
                    {ocrLoading ? 'Scanning...' : 'Extract Notes & Maps'}
                  </button>
                </form>

                {ocrResult && (
                  <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 text-xs font-medium space-y-2 max-h-40 overflow-y-auto">
                    <div className="font-extrabold text-slate-700">{ocrResult.title}</div>
                    <p className="text-slate-500">{ocrResult.summary}</p>
                    <ul className="list-disc pl-4 space-y-1 text-slate-400">
                      {ocrResult.key_points?.map((pt: string, idx: number) => (
                        <li key={idx}>{pt}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* MIND MAP TAB */}
        {activeTab === 'mindmap' && (
          <MindMap data={content.mind_map} />
        )}

        {/* FLOWCHART TAB */}
        {activeTab === 'flowchart' && (
          <Flowchart mermaidCode={content.flowchart} />
        )}

        {/* CONCEPT MAP TAB */}
        {activeTab === 'concept' && (
          <div className="bg-white p-6 rounded-kids border border-slate-100 shadow-sm space-y-6">
            <h3 className="brand-title text-xl text-slate-700 mb-2">🗺️ Interconnected Concept Nodes</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {content.concept_map?.map((rel: any, idx: number) => (
                <div key={idx} className="bg-indigo-50/50 p-4 border border-indigo-100 rounded-2xl flex flex-col justify-between text-center min-h-[120px]">
                  <div className="font-extrabold text-slate-600 text-sm">{rel.source}</div>
                  <div className="text-xs font-bold text-brand-500 italic my-2">⬇️ {rel.relation} ⬇️</div>
                  <div className="font-extrabold text-slate-700 text-sm">{rel.target}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* FLASHCARDS TAB */}
        {activeTab === 'flashcards' && (
          <div className="max-w-md mx-auto space-y-6">
            <h3 className="brand-title text-xl text-center text-slate-700">🎴 Click card to flip!</h3>
            
            {currentFlashcard ? (
              <div 
                onClick={() => setIsFlipped(!isFlipped)}
                className={`w-full h-60 rounded-kids cursor-pointer flex items-center justify-center p-8 text-center transition duration-300 transform select-none shadow-lg border-2 ${
                  isFlipped 
                    ? 'bg-amber-400 border-amber-300 text-white' 
                    : 'bg-white border-brand-200 text-slate-700 hover:border-brand-300'
                }`}
              >
                <p className="text-xl font-extrabold">
                  {isFlipped ? currentFlashcard.back : currentFlashcard.front}
                </p>
              </div>
            ) : (
              <div className="text-center p-8 text-slate-400 font-bold">No flashcards available.</div>
            )}

            {content.flashcards && content.flashcards.length > 0 && (
              <div className="flex justify-between items-center px-4 font-bold text-slate-500 text-sm">
                <button 
                  disabled={fcIdx === 0}
                  onClick={() => { setFcIdx(prev => prev - 1); setIsFlipped(false); }}
                  className="px-4 py-2 border rounded-xl hover:bg-slate-50 disabled:opacity-50"
                >
                  ⬅️ Previous
                </button>
                <span>Card {fcIdx + 1} of {content.flashcards.length}</span>
                <button 
                  disabled={fcIdx === content.flashcards.length - 1}
                  onClick={() => { setFcIdx(prev => prev + 1); setIsFlipped(false); }}
                  className="px-4 py-2 border rounded-xl hover:bg-slate-50 disabled:opacity-50"
                >
                  Next ➡️
                </button>
              </div>
            )}
          </div>
        )}

        {/* AI TUTOR TAB */}
        {activeTab === 'tutor' && (
          <AITutorChat topicName={topic.name} token={token} />
        )}

        {/* QUIZ TAB */}
        {activeTab === 'quiz' && (
          <QuizComponent 
            topicName={topic.name} 
            questions={quizzes} 
            token={token}
            onComplete={() => setActiveTab('learn')}
          />
        )}
      </div>
    </div>
  );
};

export default TopicViewer;
