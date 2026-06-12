import React, { useState, useEffect } from 'react';
import { API_BASE_URL } from '../config';

interface RecentAttempt {
  topic_name: string;
  subject_name: string;
  quiz_score: number;
  completion_time: number;
  mastery_level: string;
  attempted_at: string;
}

interface DashboardInfo {
  total_quizzes_taken: number;
  average_score: number;
  mastered_count: number;
  proficient_count: number;
  needs_improvement_count: number;
  recent_attempts: RecentAttempt[];
}

interface RecommendedTopic {
  name: string;
  subject: string;
  grade: number;
  difficulty: string;
}

interface ProgressDashboardProps {
  token: string | null;
  onBack: () => void;
  onSelectTopic: (name: string) => void;
}

const ProgressDashboard: React.FC<ProgressDashboardProps> = ({ token, onBack, onSelectTopic }) => {
  const [stats, setStats] = useState<DashboardInfo | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendedTopic[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      setLoading(true);
      try {
        const statsRes = await fetch(`${API_BASE_URL}/progress/dashboard`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (statsRes.ok) {
          const statsData = await statsRes.json();
          setStats(statsData);
        }

        const recsRes = await fetch(`${API_BASE_URL}/recommendations`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (recsRes.ok) {
          const recsData = await recsRes.json();
          setRecommendations(recsData);
        }
      } catch (err) {
        console.error('Failed to load dashboard:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [token]);

  if (loading) {
    return (
      <div className="text-center py-24 text-slate-400 font-bold">
        ⏳ Calculating your badges and learning stats...
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <button 
          onClick={onBack}
          className="text-slate-500 font-bold hover:text-slate-700 flex items-center gap-1 text-sm transition"
        >
          ⬅️ Back to home page
        </button>
        <h2 className="brand-title text-3xl text-slate-800 mt-2">
          🏆 My Learning Progress Dashboard
        </h2>
      </div>

      {/* Numerical Stats overview */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white border-2 border-indigo-100 rounded-kids p-6 shadow-sm flex flex-col justify-between">
          <div className="text-sm text-slate-400 font-bold uppercase">Quizzes Completed</div>
          <div className="text-4xl font-extrabold text-brand-600 mt-2">
            {stats?.total_quizzes_taken || 0}
          </div>
          <p className="text-xs text-slate-400 font-medium mt-1">Keep it up! ⚡</p>
        </div>

        <div className="bg-white border-2 border-indigo-100 rounded-kids p-6 shadow-sm flex flex-col justify-between">
          <div className="text-sm text-slate-400 font-bold uppercase">Average Score</div>
          <div className="text-4xl font-extrabold text-cyan-500 mt-2">
            {stats?.average_score || 0}%
          </div>
          <p className="text-xs text-slate-400 font-medium mt-1">Excellent performance!</p>
        </div>

        <div className="bg-white border-2 border-indigo-100 rounded-kids p-6 shadow-sm flex flex-col justify-between">
          <div className="text-sm text-slate-400 font-bold uppercase">Mastered Badges</div>
          <div className="text-4xl font-extrabold text-amber-500 mt-2">
            {stats?.mastered_count || 0}
          </div>
          <p className="text-xs text-slate-400 font-medium mt-1">Highest mastery rating! 🏆</p>
        </div>

        <div className="bg-white border-2 border-indigo-100 rounded-kids p-6 shadow-sm flex flex-col justify-between">
          <div className="text-sm text-slate-400 font-bold uppercase">Proficient Badges</div>
          <div className="text-4xl font-extrabold text-emerald-500 mt-2">
            {stats?.proficient_count || 0}
          </div>
          <p className="text-xs text-slate-400 font-medium mt-1">Solid skills established!</p>
        </div>
      </section>

      {/* Main dashboard body */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left column: Recent history */}
        <section className="lg:col-span-2 bg-white p-6 border-2 border-slate-100 rounded-kids shadow-sm space-y-6">
          <h3 className="brand-title text-xl text-slate-700">📖 Recent Learning Activity</h3>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs font-semibold text-slate-500">
              <thead>
                <tr className="border-b border-slate-100 text-slate-400 uppercase tracking-wider">
                  <th className="pb-3">Lesson Topic</th>
                  <th className="pb-3">Subject</th>
                  <th className="pb-3 text-center">Score</th>
                  <th className="pb-3 text-center">Time</th>
                  <th className="pb-3 text-right">Mastery Rating</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {stats?.recent_attempts.map((attempt, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/50 transition duration-150">
                    <td className="py-3.5 font-bold text-slate-700 cursor-pointer hover:text-brand-500" onClick={() => onSelectTopic(attempt.topic_name)}>
                      {attempt.topic_name.split('(')[0]}
                    </td>
                    <td className="py-3.5">{attempt.subject_name}</td>
                    <td className="py-3.5 text-center font-extrabold text-slate-800">{attempt.quiz_score}%</td>
                    <td className="py-3.5 text-center">{attempt.completion_time}s</td>
                    <td className="py-3.5 text-right font-extrabold text-brand-500">{attempt.mastery_level}</td>
                  </tr>
                ))}
                {(!stats?.recent_attempts || stats.recent_attempts.length === 0) && (
                  <tr>
                    <td colSpan={5} className="py-8 text-center text-slate-400">
                      No attempts logged yet. Take a quiz to seed your progress dashboard!
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        {/* Right column: ML Recommendations path */}
        <section className="bg-gradient-to-br from-brand-50 to-cyan-50 p-6 border-2 border-brand-200 rounded-kids shadow-sm space-y-6">
          <h3 className="brand-title text-xl text-brand-700">🔮 Personalized AI Recommendations</h3>
          <p className="text-slate-500 font-bold text-xs">Based on your learning history and scores, your AI guide suggests studying these topics next:</p>

          <div className="space-y-4">
            {recommendations.map((topic, i) => (
              <div 
                key={`rec-${i}`}
                onClick={() => onSelectTopic(topic.name)}
                className="bg-white p-4 rounded-xl border border-indigo-100 hover:border-brand-300 shadow-sm cursor-pointer hover:shadow-md transition transform active:scale-98 flex items-center justify-between"
              >
                <div>
                  <div className="text-[10px] text-cyan-600 font-bold uppercase tracking-wider">
                    {topic.subject} • Grade {topic.grade}
                  </div>
                  <h4 className="font-bold text-slate-700 text-sm mt-0.5">
                    {topic.name.split('(')[0]}
                  </h4>
                </div>
                <span className="text-xs">➡️</span>
              </div>
            ))}
            {recommendations.length === 0 && (
              <div className="text-center p-8 bg-white border rounded-xl text-slate-400 text-xs">
                Analyzing scores to compile recommendations...
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
};

export default ProgressDashboard;
