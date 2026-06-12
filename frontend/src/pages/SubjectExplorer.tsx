import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '../config';

interface Topic {
  id: number;
  name: string;
  description: string;
  difficulty: string;
}

interface SubjectExplorerProps {
  subjectName: string;
  grade: number;
  token: string | null;
  onSelectTopic: (topicId: number, name: string) => void;
  onBack: () => void;
}

const SubjectExplorer: React.FC<SubjectExplorerProps> = ({
  subjectName,
  grade,
  token,
  onSelectTopic,
  onBack
}) => {
  const [topics, setTopics] = useState<Topic[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchTopics = async () => {
      setLoading(true);
      try {
        const res = await fetch(`${API_BASE_URL}/subjects/${subjectName}/topics?grade=${grade}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.ok ? await res.json() : [];
          setTopics(data);
        }
      } catch (err) {
        console.error('Error fetching topics:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTopics();
  }, [subjectName, grade, token]);

  const filteredTopics = topics.filter(t => 
    t.name.toLowerCase().includes(search.toLowerCase()) ||
    t.description.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-8">
      {/* Header controls */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <button 
            onClick={onBack}
            className="mb-2 text-slate-500 font-bold hover:text-slate-700 flex items-center gap-1 text-sm transition"
          >
            ⬅️ Back to Subjects
          </button>
          <h2 className="brand-title text-3xl text-slate-800">
            {subjectName} - Grade {grade} 🚀
          </h2>
        </div>
        
        {/* Search inside subject */}
        <div className="w-full sm:max-w-xs">
          <input 
            type="text" 
            className="w-full px-4 py-2 border-2 border-slate-200 focus:border-brand-400 rounded-xl outline-none transition text-sm font-semibold"
            placeholder="Search lessons..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {loading ? (
        <div className="text-center py-20 text-slate-400 font-bold">
          ⏳ Gathering cool lessons for you...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTopics.map(topic => (
            <div 
              key={topic.id}
              onClick={() => onSelectTopic(topic.id, topic.name)}
              className="sparkle-hover bg-white border-2 border-slate-100 hover:border-brand-200 rounded-kids p-6 shadow-sm hover:shadow-lg transition duration-200 cursor-pointer flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className={`text-xs font-extrabold px-2.5 py-0.5 rounded-full uppercase ${
                    topic.difficulty === 'Easy' 
                      ? 'bg-green-50 text-green-600 border border-green-100' 
                      : topic.difficulty === 'Hard' 
                      ? 'bg-red-50 text-red-600 border border-red-100' 
                      : 'bg-amber-50 text-amber-600 border border-amber-100'
                  }`}>
                    {topic.difficulty}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-slate-700 hover:text-brand-500">
                  {topic.name}
                </h3>
                <p className="text-slate-500 font-medium text-xs line-clamp-3">
                  {topic.description}
                </p>
              </div>
              <div className="mt-6 flex justify-end">
                <span className="px-4 py-1.5 bg-brand-50 hover:bg-brand-100 text-brand-600 font-extrabold text-xs rounded-xl shadow-sm transition">
                  Start Adventure ✨
                </span>
              </div>
            </div>
          ))}
          {filteredTopics.length === 0 && (
            <div className="col-span-full text-center py-20 bg-white border border-slate-100 rounded-kids text-slate-400 font-bold">
              📚 No lessons found for this subject and grade level.
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SubjectExplorer;
