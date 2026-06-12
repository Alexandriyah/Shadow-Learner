import React, { useState, useEffect } from 'react';
import Layout from './components/Layout';
import Home from './pages/Home';
import SubjectExplorer from './pages/SubjectExplorer';
import TopicViewer from './pages/TopicViewer';
import ProgressDashboard from './pages/ProgressDashboard';
import { API_BASE_URL } from './config';

export interface User {
  username: string;
  email: string;
  grade: number;
}

export type Page = 'home' | 'explorer' | 'topic' | 'dashboard' | 'login' | 'signup';

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<Page>('login');
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [selectedGrade, setSelectedGrade] = useState<number>(5);
  const [selectedSubject, setSelectedSubject] = useState<string>('Science');
  const [selectedTopic, setSelectedTopic] = useState<{ id: number; name: string } | null>(null);
  
  // Auth Form State
  const [usernameInput, setUsernameInput] = useState('');
  const [emailInput, setEmailInput] = useState('');
  const [passwordInput, setPasswordInput] = useState('');
  const [gradeInput, setGradeInput] = useState(5);
  const [authError, setAuthError] = useState('');
  const [loading, setLoading] = useState(false);

  // Restore session
  useEffect(() => {
    const savedToken = localStorage.getItem('vl_token');
    const savedUser = localStorage.getItem('vl_user');
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
      const parsedUser = JSON.parse(savedUser);
      setSelectedGrade(parsedUser.grade || 5);
      setCurrentPage('home');
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('vl_token');
    localStorage.removeItem('vl_user');
    setToken(null);
    setUser(null);
    setCurrentPage('login');
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError('');
    setLoading(true);
    try {
      const formData = new URLSearchParams();
      formData.append('username', usernameInput);
      formData.append('password', passwordInput);

      const res = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData.toString()
      });

      if (!res.ok) {
        throw new Error('Invalid username or password');
      }

      const data = await res.json();
      const accessToken = data.access_token;
      
      // Fetch user profile
      const userRes = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: { 'Authorization': `Bearer ${accessToken}` }
      });
      const userData = await userRes.json();

      localStorage.setItem('vl_token', accessToken);
      localStorage.setItem('vl_user', JSON.stringify(userData));
      
      setToken(accessToken);
      setUser(userData);
      setSelectedGrade(userData.grade || 5);
      setCurrentPage('home');
      
      // Reset inputs
      setUsernameInput('');
      setPasswordInput('');
    } catch (err: any) {
      setAuthError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setAuthError('');
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username: usernameInput,
          email: emailInput,
          grade: gradeInput,
          password: passwordInput
        })
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Registration failed');
      }

      // Automatically log in
      await handleLogin(e);
    } catch (err: any) {
      setAuthError(err.message || 'Sign up failed');
    } finally {
      setLoading(false);
    }
  };

  // Main Page Content Renderer
  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return (
          <Home 
            selectedGrade={selectedGrade}
            setSelectedGrade={setSelectedGrade}
            onSelectSubject={(subject: any) => {
              setSelectedSubject(subject);
              setCurrentPage('explorer');
            }}
            username={user?.username || 'Learner'}
            onGoToDashboard={() => setCurrentPage('dashboard')}
          />
        );
      case 'explorer':
        return (
          <SubjectExplorer 
            subjectName={selectedSubject}
            grade={selectedGrade}
            token={token}
            onSelectTopic={(topicId: any, name: any) => {
              setSelectedTopic({ id: topicId, name });
              setCurrentPage('topic');
            }}
            onBack={() => setCurrentPage('home')}
          />
        );
      case 'topic':
        return selectedTopic ? (
          <TopicViewer 
            topic={selectedTopic}
            token={token}
            onBack={() => setCurrentPage('explorer')}
          />
        ) : (
          <div className="text-center p-8">No topic selected</div>
        );
      case 'dashboard':
        return (
          <ProgressDashboard 
            token={token}
            onBack={() => setCurrentPage('home')}
            onSelectTopic={(name: any) => {
              // Reconstruct topic view if possible or just navigate
              setSelectedTopic({ id: 0, name }); // ID will load name-based content
              setCurrentPage('topic');
            }}
          />
        );
      default:
        return null;
    }
  };

  if (currentPage === 'login' || currentPage === 'signup') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-brand-100 via-indigo-50 to-cyan-100 p-4">
        <div className="w-full max-w-md bg-white/85 backdrop-blur-md border-2 border-brand-200 rounded-kids shadow-2xl p-8 transition duration-300 hover:shadow-brand-200/50">
          <div className="text-center mb-8">
            <h1 className="brand-title text-4xl text-brand-600 mb-2 flex justify-center items-center gap-2">
              ✨ VisualLearn AI 🚀
            </h1>
            <p className="text-slate-500 font-medium">Making learning visual & fun!</p>
          </div>

          {authError && (
            <div className="mb-4 p-3 bg-red-100 border border-red-200 text-red-600 rounded-lg text-sm text-center font-medium">
              ⚠️ {authError}
            </div>
          )}

          <form onSubmit={currentPage === 'login' ? handleLogin : handleSignup} className="space-y-4">
            <div>
              <label className="block text-slate-600 font-bold mb-1 text-sm">Username</label>
              <input 
                type="text" 
                required
                className="w-full px-4 py-2 border-2 border-slate-200 rounded-xl focus:border-brand-400 outline-none transition"
                value={usernameInput}
                onChange={(e: { target: { value: any; }; }) => setUsernameInput(e.target.value)}
                placeholder="Enter a fun username!"
              />
            </div>

            {currentPage === 'signup' && (
              <>
                <div>
                  <label className="block text-slate-600 font-bold mb-1 text-sm">Email</label>
                  <input 
                    type="email" 
                    required
                    className="w-full px-4 py-2 border-2 border-slate-200 rounded-xl focus:border-brand-400 outline-none transition"
                    value={emailInput}
                    onChange={(e: { target: { value: any; }; }) => setEmailInput(e.target.value)}
                    placeholder="learner@school.com"
                  />
                </div>
                <div>
                  <label className="block text-slate-600 font-bold mb-1 text-sm">Grade / Class</label>
                  <select 
                    className="w-full px-4 py-2 border-2 border-slate-200 rounded-xl focus:border-brand-400 outline-none bg-white transition"
                    value={gradeInput}
                    onChange={(e: { target: { value: any; }; }) => setGradeInput(Number(e.target.value))}
                  >
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(g => (
                      <option key={g} value={g}>Grade {g}</option>
                    ))}
                  </select>
                </div>
              </>
            )}

            <div>
              <label className="block text-slate-600 font-bold mb-1 text-sm">Password</label>
              <input 
                type="password" 
                required
                className="w-full px-4 py-2 border-2 border-slate-200 rounded-xl focus:border-brand-400 outline-none transition"
                value={passwordInput}
                onChange={(e: { target: { value: any; }; }) => setPasswordInput(e.target.value)}
                placeholder="••••••••"
              />
            </div>

            <button 
              type="submit" 
              disabled={loading}
              className="w-full py-3 bg-brand-500 hover:bg-brand-600 text-white font-bold rounded-xl shadow-lg transition duration-200 transform active:scale-95 disabled:opacity-50"
            >
              {loading ? 'Crunching numbers...' : (currentPage === 'login' ? 'Let\'s Learn! 🚀' : 'Create Account! 🎉')}
            </button>
          </form>

          <div className="mt-6 text-center text-sm font-semibold text-slate-500">
            {currentPage === 'login' ? (
              <p>
                New learner?{' '}
                <button 
                  onClick={() => { setCurrentPage('signup'); setAuthError(''); }} 
                  className="text-brand-500 hover:underline"
                >
                  Create an account
                </button>
              </p>
            ) : (
              <p>
                Already have an account?{' '}
                <button 
                  onClick={() => { setCurrentPage('login'); setAuthError(''); }} 
                  className="text-brand-500 hover:underline"
                >
                  Sign in
                </button>
              </p>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <Layout 
      username={user?.username || 'Learner'} 
      grade={selectedGrade} 
      onLogout={handleLogout}
      onNavigate={(page: any) => setCurrentPage(page)}
      currentPage={currentPage}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {renderPage()}
      </div>
    </Layout>
  );
};

export default App;
