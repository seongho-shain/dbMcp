import { useAuth } from './AuthContext'
import ChatInterface from './components/ChatInterface'
import './App.css'

function StudentDashboard() {
  const { user, logout } = useAuth()

  return (
    <div className="app">
      <div className="header">
        <h1>학생 대시보드</h1>
        <div className="user-info">
          <span className="welcome-message">{user.name}님 반갑습니다!</span>
          <button onClick={logout} className="logout-btn">로그아웃</button>
        </div>
      </div>
      
      <div className="dashboard-content">
        <div className="student-info">
          <h2>클래스 정보</h2>
          <div className="info-card">
            <p><strong>클래스 코드:</strong> {user.class_code}</p>
            <p><strong>세션 ID:</strong> {user.session_id}</p>
            <p><strong>참여 시간:</strong> {new Date(user.created_at).toLocaleString()}</p>
          </div>
          
          <div className="student-actions">
            <p>클래스에 성공적으로 참여했습니다!</p>
            <p>아래 채팅창에서 AI와 1:1 대화를 나누어보세요.</p>
          </div>
        </div>
        
        <div className="chat-section">
          <ChatInterface />
        </div>
      </div>
    </div>
  )
}

export default StudentDashboard