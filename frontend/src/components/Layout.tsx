import React from 'react';

interface LayoutProps {
  children: React.ReactNode;
  username: string;
  grade: number;
  onLogout: () => void;
  onNavigate: (page: any) => void;
  currentPage: string;
}

const Layout: React.FC<LayoutProps> = ({ 
  children, 
  username, 
  grade, 
  onLogout, 
  onNavigate,
  currentPage 
}) => {
  return (
    <div className="min-h-screen bg-indigo-50/20 text-slate-800 flex flex-col font-sans">
      {/* Header NavBar */}
      <header className="bg-white/80 backdrop-blur-md sticky top-0 z-40 border-b border-indigo-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-20">
            {/* Logo */}
            <div 
              className="flex items-center gap-2 cursor-pointer transition transform active:scale-95"
              onClick={() => onNavigate('home')}
            >
              <span className="text-3xl">✨</span>
              <span className="brand-title text-2xl font-bold bg-gradient-to-r from-brand-600 to-cyan-500 bg-clip-text text-transparent">
                VisualLearn AI
              </span>
              <span className="text-xl">🚀</span>
            </div>

            {/* Desktop Navigation Links */}
            <nav className="flex items-center gap-6">
              <button 
                onClick={() => onNavigate('home')}
                className={`px-4 py-2 rounded-xl font-bold transition ${
                  currentPage === 'home' 
                    ? 'bg-brand-100 text-brand-600' 
                    : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                🏠 Home
              </button>
              <button 
                onClick={() => onNavigate('dashboard')}
                className={`px-4 py-2 rounded-xl font-bold transition ${
                  currentPage === 'dashboard' 
                    ? 'bg-brand-100 text-brand-600' 
                    : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                📊 My Progress
              </button>
            </nav>

            {/* User Details & Logout */}
            <div className="flex items-center gap-4">
              <div className="hidden sm:flex flex-col text-right">
                <span className="font-bold text-slate-700">Hey, {username}! 👋</span>
                <span className="text-xs font-bold text-cyan-600 bg-cyan-50 px-2 py-0.5 rounded-full inline-block self-end">
                  Grade {grade}
                </span>
              </div>
              <button 
                onClick={onLogout}
                className="px-4 py-2 border-2 border-slate-200 hover:border-red-200 text-slate-600 hover:text-red-500 font-bold rounded-xl transition duration-150 active:scale-95 text-sm"
              >
                🚪 Log Out
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-grow">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-8 border-t border-slate-800 text-center text-sm font-semibold">
        <p className="mb-2">✨ VisualLearn AI - A Fun Machine Learning & GenAI Playground for Curious Kids 🚀</p>
        <p className="text-slate-600">© 2026 VisualLearn AI. Built for child-friendly interactive education.</p>
      </footer>
    </div>
  );
};

export default Layout;
