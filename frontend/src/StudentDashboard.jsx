import { useAuth } from './AuthContext'
import ChatInterface from './components/ChatInterface'
import './App.css'

function StudentDashboard() {
  const { user, logout } = useAuth()

  return (
    <div className="recommend-dashboard__main">
      <div className="recommend-dashboard__header">
        <div className="recommend-header-content">
          <div className="recommend-header-info">
            <h1>학생 대시보드</h1>
            <div className="recommend-badges">
              <span className="recommend-badge">{user.name}님 반갑습니다!</span>
            </div>
          </div>
          <div className="recommend-header-actions">
            <button onClick={logout} className="recommend-btn recommend-btn--secondary">로그아웃</button>
          </div>
        </div>
      </div>
      
      <div className="recommend-dashboard__grid">
        <div className="recommend-card">
          <div className="recommend-card__header">📚 클래스 정보</div>
          <div className="recommend-card__content">
            <div className="recommend-stats-grid">
              <div className="recommend-stat-item">
                <span className="recommend-stat-item__value">{user.class_code}</span>
                <span className="recommend-stat-item__label">클래스 코드</span>
              </div>
              <div className="recommend-stat-item">
                <span className="recommend-stat-item__value">{user.session_id}</span>
                <span className="recommend-stat-item__label">세션 ID</span>
              </div>
            </div>
            <div style={{ marginTop: 'var(--recommend-spacing-lg)' }}>
              <p><strong>참여 시간:</strong> {new Date(user.created_at).toLocaleString()}</p>
            </div>
          </div>
        </div>
        
        <div className="recommend-card recommend-card--highlight">
          <div className="recommend-card__header">🎯 학습 가이드</div>
          <div className="recommend-card__content">
            <div className="recommend-features">
              <div className="recommend-feature">
                <div className="recommend-feature__icon">✅</div>
                <div className="recommend-feature__content">
                  <h4>클래스 참여 완료</h4>
                  <p>성공적으로 클래스에 참여했습니다!</p>
                </div>
              </div>
              <div className="recommend-feature">
                <div className="recommend-feature__icon">💬</div>
                <div className="recommend-feature__content">
                  <h4>AI 채팅 이용</h4>
                  <p>아래 채팅창에서 AI와 1:1 대화를 나누어보세요.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="recommend-dashboard__grid">
        <div className="recommend-card" style={{ gridColumn: '1 / -1' }}>
          <div className="recommend-card__header">🤖 AI 채팅</div>
          <div className="recommend-card__content">
            <ChatInterface />
          </div>
        </div>
      </div>
    </div>
  )
}

export default StudentDashboard