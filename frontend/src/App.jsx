import { useState } from 'react';
import { AuthProvider, useAuth } from './AuthContext';
import TeacherLogin from './TeacherLogin';
import StudentLogin from './StudentLogin';
import TeacherSignup from './TeacherSignup';
import TeacherDashboard from './TeacherDashboard';
import StudentDashboard from './StudentDashboard';
import Gallery from './Gallery';
import Particles from './components/Particles';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <AuthenticatedApp />
    </AuthProvider>
  );
}

function AuthenticatedApp() {
  const { user, loading } = useAuth();
  const [authMode, setAuthMode] = useState('student');
  const [activeNav, setActiveNav] = useState('tool');

  // Get session info for gallery
  const getSessionInfo = () => {
    if (!user) return null;
    
    if (user.user_type === 'student') {
      return {
        sessionId: user.session_id,
        sessionInfo: {
          class_code: user.class_code,
          id: user.session_id
        }
      };
    } else if (user.user_type === 'teacher') {
      // For teachers, we'll use the first session if available
      // In a real app, you might want to let teachers select which session's gallery to view
      return {
        sessionId: user.current_session_id || null,
        sessionInfo: user.current_session_id ? {
          class_code: user.current_class_code || 'Unknown',
          id: user.current_session_id
        } : null
      };
    }
    
    return null;
  };

  if (loading) {
    return <div className="theme-recommend recommend-dashboard"><div className="loading">Loading...</div></div>;
  }

  if (!user) {
    return (
      <div className="theme-recommend recommend-dashboard">
        <Particles 
          count={80}
          size={2.5}
          speed={0.3}
          color="#1e91d6"
          opacity={0.4}
        />
        <div className="auth-container">
          <div className="auth-mode-selector">
            <button 
              className={`recommend-btn ${authMode === 'student' ? 'recommend-btn--primary' : 'recommend-btn--secondary'}`}
              onClick={() => setAuthMode('student')}
            >
              학생 로그인
            </button>
            <button 
              className={`recommend-btn ${authMode === 'teacher' ? 'recommend-btn--primary' : 'recommend-btn--secondary'}`}
              onClick={() => setAuthMode('teacher')}
            >
              선생님 로그인
            </button>
            <button 
              className={`recommend-btn ${authMode === 'signup' ? 'recommend-btn--primary' : 'recommend-btn--secondary'}`}
              onClick={() => setAuthMode('signup')}
            >
              선생님 회원가입
            </button>
          </div>
          
          {authMode === 'student' && <StudentLogin />}
          {authMode === 'teacher' && <TeacherLogin />}
          {authMode === 'signup' && <TeacherSignup onSuccess={() => setAuthMode('teacher')} />}
        </div>
      </div>
    );
  }

  return (
    <div className="main-container">
      <header className="app-header">
        <h1>AI 교육 대시보드</h1>
        <nav className="app-nav">
          <button 
            className={`nav-button ${activeNav === 'tool' ? 'active' : ''}`}
            onClick={() => setActiveNav('tool')}
          >
            툴
          </button>
          <button 
            className={`nav-button ${activeNav === 'gallery' ? 'active' : ''}`}
            onClick={() => setActiveNav('gallery')}
          >
            갤러리
          </button>
        </nav>
      </header>
      <main className="app-content">
        {activeNav === 'tool' && (user.user_type === 'teacher' ? <TeacherDashboard /> : <StudentDashboard />)}
        {activeNav === 'gallery' && (
          <Gallery 
            sessionId={getSessionInfo()?.sessionId}
            sessionInfo={getSessionInfo()?.sessionInfo}
          />
        )}
      </main>
    </div>
  );
}

export default App;
