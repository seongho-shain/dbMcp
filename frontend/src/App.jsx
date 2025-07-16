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
    return <div className="loading">Loading...</div>
  }
  
  if (!user) {
    return (
      <div className="auth-container">
        <div className="auth-mode-selector">
          <button 
            className={authMode === 'student' ? 'active' : ''}
            onClick={() => setAuthMode('student')}
          >
            학생 로그인
          </button>
          <button 
            className={authMode === 'teacher' ? 'active' : ''}
            onClick={() => setAuthMode('teacher')}
          >
            선생님 로그인
          </button>
          <button 
            className={authMode === 'signup' ? 'active' : ''}
            onClick={() => setAuthMode('signup')}
          >
            선생님 회원가입
          </button>
        </div>
        
        {authMode === 'student' && <StudentLogin />}
        {authMode === 'teacher' && <TeacherLogin />}
        {authMode === 'signup' && <TeacherSignup onSuccess={() => setAuthMode('teacher')} />}
      </div>
    )
  }
  
  if (user.user_type === 'teacher') {
    return <TeacherDashboard />
  } else {
    return <StudentDashboard />
  }
}

export default App