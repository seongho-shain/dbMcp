import { useState } from 'react';
import { AuthProvider, useAuth } from './AuthContext';
import { StudentLogin, TeacherLogin, TeacherSignup } from './features/auth';
import { TeacherDashboard, StudentDashboard } from './features/dashboard';
import { Gallery } from './features/gallery';
import ChatInterface from './features/chat/components/ChatInterface';
import ImageGenerator from './features/imageGeneration/components/ImageGenerator';
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
            className={`nav-button ${activeNav === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveNav('chat')}
          >
            채팅
          </button>
          <button 
            className={`nav-button ${activeNav === 'image' ? 'active' : ''}`}
            onClick={() => setActiveNav('image')}
          >
            이미지
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
        {activeNav === 'chat' && (
          <ChatInterface 
            sessionId={getSessionInfo()?.sessionId}
            sessionInfo={getSessionInfo()?.sessionInfo}
          />
        )}
        {activeNav === 'image' && (
          <ImageGenerator 
            user={user}
            sessionId={getSessionInfo()?.sessionId}
          />
        )}
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