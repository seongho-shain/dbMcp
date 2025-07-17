import { useState } from 'react'
import { AuthProvider, useAuth } from './AuthContext'
import TeacherLogin from './TeacherLogin'
import StudentLogin from './StudentLogin'
import TeacherSignup from './TeacherSignup'
import TeacherDashboard from './TeacherDashboard'
import StudentDashboard from './StudentDashboard'
import './App.css'

function App() {
  const [authMode, setAuthMode] = useState('student') // 'student', 'teacher', 'signup'
  
  return (

      <AuthProvider>
        <AuthenticatedApp authMode={authMode} setAuthMode={setAuthMode} />
      </AuthProvider>

  )
}

function AuthenticatedApp({ authMode, setAuthMode }) {
  const { user, loading } = useAuth()
  
  if (loading) {
    return <div className="theme-recommend recommend-dashboard">
      <div className="loading">Loading...</div>
    </div>
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
    )
  }
  
  return (
    <div className="theme-recommend recommend-dashboard">
      <div className="recommend-dashboard__header">
        <div className="recommend-header-content">
          <h1>AI 교육 대시보드</h1>
          <div className="recommend-header-actions">
          </div>
        </div>
      </div>
      {user.user_type === 'teacher' ? <TeacherDashboard /> : <StudentDashboard />}
    </div>
  )
}

export default App