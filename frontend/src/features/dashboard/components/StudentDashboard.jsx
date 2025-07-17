import { useAuth } from '../../../AuthContext';
import './StudentDashboard.css';

function StudentDashboard() {
  const { user, logout } = useAuth();

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
          <div className="recommend-card__header">🎯 네비게이션 가이드</div>
          <div className="recommend-card__content">
            <div className="recommend-features">
              <div className="recommend-feature">
                <div className="recommend-feature__icon">💡</div>
                <div className="recommend-feature__content">
                  <h4>상단 네비게이션 사용법</h4>
                  <p>상단 네비게이션에서 <strong>채팅</strong>, <strong>이미지</strong>, <strong>갤러리</strong> 탭을 클릭하여 각 기능을 사용하세요!</p>
                </div>
              </div>
              <div className="recommend-feature">
                <div className="recommend-feature__icon">🎨</div>
                <div className="recommend-feature__content">
                  <h4>AI 이미지 잘 쓰는 법 (Stability AI)</h4>
                  <p><strong>생생하고 상세하게 묘사하세요.</strong><br/>주제, 배경, 스타일, 색감, 구도 등을 구체적으로 작성하면 상상에 가까운 이미지를 얻을 수 있습니다. (예: "푸른 바다 위 절벽에 있는 하얀 등대, 유화 스타일, 해질녹 노을")</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}

export default StudentDashboard;