import React, { useState } from 'react';

interface HomeProps {
  selectedGrade: number;
  setSelectedGrade: (grade: number) => void;
  onSelectSubject: (subject: string) => void;
  username: string;
  onGoToDashboard: () => void;
}

const Home: React.FC<HomeProps> = ({ 
  selectedGrade, 
  setSelectedGrade, 
  onSelectSubject, 
  username,
  onGoToDashboard
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  const subjects = [
    { name: 'Science', emoji: '🔬', color: 'from-purple-400 to-indigo-500', desc: 'Explore the stars, forces, and living things!' },
    { name: 'Mathematics', emoji: '🧮', color: 'from-cyan-400 to-blue-500', desc: 'Play with numbers, shapes, and equations!' },
    { name: 'Social Science', emoji: '🏛️', color: 'from-amber-400 to-orange-500', desc: 'Discover society, laws, and cultures!' },
    { name: 'English', emoji: '📚', color: 'from-pink-400 to-rose-500', desc: 'Read stories, write poems, and master grammar!' },
    { name: 'Biology', emoji: '🌿', color: 'from-emerald-400 to-teal-500', desc: 'Learn about plants, cells, and ecosystems!' },
    { name: 'Physics', emoji: '⚡', color: 'from-sky-400 to-indigo-500', desc: 'Unravel motion, gravity, light, and sound!' },
    { name: 'Chemistry', emoji: '🧪', color: 'from-violet-400 to-purple-600', desc: 'Mix formulas, discover atoms and compounds!' },
    { name: 'History', emoji: '⚔️', color: 'from-amber-600 to-amber-800', desc: 'Travel in time to meet kings and revolutions!' },
    { name: 'Geography', emoji: '🗺️', color: 'from-teal-500 to-emerald-600', desc: 'Map oceans, rivers, and the layers of Earth!' }
  ];

  const filteredSubjects = subjects.filter(sub => 
    sub.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-12">
      {/* Welcome Hero Banner */}
      <section className="bg-gradient-to-r from-brand-500 to-cyan-500 text-white rounded-kids p-8 sm:p-12 shadow-xl relative overflow-hidden flex flex-col md:flex-row items-center justify-between gap-8">
        <div className="space-y-4 max-w-xl text-center md:text-left z-10">
          <h2 className="brand-title text-4xl sm:text-5xl">
            Welcome, {username}! 🎈
          </h2>
          <p className="text-lg font-medium opacity-90">
            What fun adventure are we exploring today? Choose your grade and subject to unlock magical maps, flowcharts, and quizzes!
          </p>
          <div className="flex gap-4 justify-center md:justify-start">
            <button 
              onClick={onGoToDashboard}
              className="px-6 py-3 bg-white text-brand-600 font-extrabold rounded-xl shadow-lg hover:shadow-white/20 transition transform active:scale-95 text-sm"
            >
              📊 Check My Badges
            </button>
          </div>
        </div>
        
        {/* Animated Graphic Mascot */}
        <div className="text-8xl sm:text-9xl floating-slow z-10 select-none">
          🤖
        </div>

        {/* Decorative background circles */}
        <div className="absolute -top-10 -left-10 w-40 h-40 bg-white/10 rounded-full blur-xl" />
        <div className="absolute -bottom-10 -right-10 w-60 h-60 bg-white/10 rounded-full blur-xl" />
      </section>

      {/* Grade Selector & Search Panel */}
      <section className="glass-card rounded-kids p-6 shadow-sm border border-slate-100 flex flex-col lg:flex-row gap-6 justify-between items-center">
        {/* Grade dials */}
        <div className="w-full lg:w-auto">
          <label className="block text-slate-500 font-bold mb-2 text-sm text-center lg:text-left">
            🎯 Select Your Grade / Class:
          </label>
          <div className="flex flex-wrap gap-2 justify-center">
            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(g => (
              <button
                key={`g-${g}`}
                onClick={() => setSelectedGrade(g)}
                className={`w-10 h-10 rounded-xl font-extrabold text-sm transition transform active:scale-90 ${
                  selectedGrade === g 
                    ? 'bg-brand-500 text-white shadow-md' 
                    : 'bg-white hover:bg-brand-50 text-slate-600 border border-slate-200'
                }`}
              >
                {g}
              </button>
            ))}
          </div>
        </div>

        {/* Search subjects */}
        <div className="w-full lg:max-w-md relative">
          <input 
            type="text" 
            className="w-full pl-12 pr-4 py-3 border-2 border-slate-200 focus:border-brand-400 rounded-xl outline-none transition text-sm font-semibold"
            placeholder="Search subjects or topics..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <span className="absolute left-4 top-3.5 text-slate-400 text-lg">🔍</span>
        </div>
      </section>

      {/* Subject cards Grid */}
      <section className="space-y-6">
        <h3 className="brand-title text-2xl text-slate-700 flex items-center gap-2">
          🎒 Subjects to Explore
        </h3>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredSubjects.map((sub, i) => (
            <div 
              key={sub.name}
              onClick={() => onSelectSubject(sub.name)}
              className="sparkle-hover bg-white border-2 border-slate-100 hover:border-brand-200 rounded-kids p-6 shadow-sm hover:shadow-lg cursor-pointer transition duration-300 flex flex-col justify-between"
            >
              <div className="space-y-4">
                <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${sub.color} flex items-center justify-center text-3xl shadow-md`}>
                  {sub.emoji}
                </div>
                <div>
                  <h4 className="text-xl font-extrabold text-slate-800">{sub.name}</h4>
                  <p className="text-slate-500 font-medium text-sm mt-1">{sub.desc}</p>
                </div>
              </div>
              <div className="mt-6 flex items-center text-xs font-bold text-brand-500 hover:text-brand-600 gap-1">
                Explore Lessons <span>➡️</span>
              </div>
            </div>
          ))}
          {filteredSubjects.length === 0 && (
            <div className="col-span-full text-center py-12 text-slate-400 font-bold">
              🚫 No subjects match your search terms
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default Home;
