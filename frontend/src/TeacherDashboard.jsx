import { useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import ChatInterface from './components/ChatInterface';
import ImageGenerator from './components/ImageGeneration/ImageGenerator';
import './TeacherDashboard.css';

const API_BASE_URL = 'http://localhost:8000';

function TeacherDashboard() {
  const [sessions, setSessions] = useState([]);
  const [students, setStudents] = useState({});
  const [loading, setLoading] = useState(false);
  const [creatingClass, setCreatingClass] = useState(false);
  const [selectedSession, setSelectedSession] = useState(null);
  const [currentGallerySession, setCurrentGallerySession] = useState(null);
  const { user, logout, updateUser } = useAuth();

  const fetchSessions = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/teacher/${user.id}/sessions`);
      if (response.ok) {
        const data = await response.json();
        setSessions(data);

        const studentsData = {};
        for (const session of data) {
          const studentsResponse = await fetch(`${API_BASE_URL}/session/${session.id}/students`);
          if (studentsResponse.ok) {
            const sessionStudents = await studentsResponse.json();
            studentsData[session.id] = sessionStudents;
          }
        }
        setStudents(studentsData);
      }
    } catch (error) {
      console.error('Error fetching sessions:', error);
    } finally {
      setLoading(false);
    }
  };

  const createNewClass = async () => {
    setCreatingClass(true);
    try {
      const response = await fetch(`${API_BASE_URL}/teacher/create-class`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ teacher_id: user.id }),
      });

      if (response.ok) {
        const data = await response.json();
        alert(`새 클래스가 생성되었습니다! 클래스 코드: ${data.class_code}`);
        fetchSessions();
      }
    } catch (error) {
      console.error('Error creating class:', error);
      alert('클래스 생성에 실패했습니다.');
    } finally {
      setCreatingClass(false);
    }
  };

  const setGallerySession = (session) => {
    setCurrentGallerySession(session);
    // Update user context with current session info for gallery
    if (updateUser) {
      updateUser({
        ...user,
        current_session_id: session?.id,
        current_class_code: session?.class_code
      });
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  return (
    <div className="recommend-dashboard__main">
      <div className="recommend-dashboard__header">
        <div className="recommend-header-content">
          <div className="recommend-header-info">
            <h1>선생님 대시보드</h1>
            <div className="recommend-badges">
              <span className="recommend-badge">{user.name} 선생님 반갑습니다!</span>
            </div>
          </div>
          <div className="recommend-header-actions">
            <button onClick={logout} className="recommend-btn recommend-btn--secondary">로그아웃</button>
          </div>
        </div>
      </div>

      <div className="recommend-dashboard__grid">
        <div className="recommend-card">
          <div className="recommend-card__header">⚡ 클래스 관리</div>
          <div className="recommend-card__content">
            <div className="recommend-features">
              <div className="recommend-feature">
                <button
                  onClick={createNewClass}
                  disabled={creatingClass}
                  className="recommend-btn recommend-btn--primary"
                >
                  {creatingClass ? '클래스 생성 중...' : '새 클래스 생성'}
                </button>
              </div>
              <div className="recommend-feature">
                <button onClick={fetchSessions} disabled={loading} className="recommend-btn recommend-btn--secondary">
                  새로고침
                </button>
              </div>
            </div>
            {loading && <p>로딩 중...</p>}
          </div>
        </div>

        <div className="recommend-card">
          <div className="recommend-card__header">📊 클래스 현황</div>
          <div className="recommend-card__content">
            <div className="recommend-stats-grid">
              <div className="recommend-stat-item">
                <span className="recommend-stat-item__value">{sessions.length}</span>
                <span className="recommend-stat-item__label">총 클래스</span>
              </div>
              <div className="recommend-stat-item">
                <span className="recommend-stat-item__value">
                  {Object.values(students).reduce((total, sessionStudents) => total + sessionStudents.length, 0)}
                </span>
                <span className="recommend-stat-item__label">참여 학생</span>
              </div>
            </div>
          </div>
        </div>

        <div className="recommend-card">
          <div className="recommend-card__header">🎨 갤러리 세션 선택</div>
          <div className="recommend-card__content">
            <div className="recommend-features">
              <div className="recommend-feature">
                <div className="recommend-feature__icon">📋</div>
                <div className="recommend-feature__content">
                  <h4>현재 갤러리 세션</h4>
                  <p>
                    {currentGallerySession 
                      ? `${currentGallerySession.class_code} (${students[currentGallerySession.id]?.length || 0}명 참여)`
                      : '선택된 세션이 없습니다'
                    }
                  </p>
                  {sessions.length > 0 && (
                    <div className="gallery-session-selector">
                      <select 
                        value={currentGallerySession?.id || ''} 
                        onChange={(e) => {
                          const sessionId = parseInt(e.target.value);
                          const session = sessions.find(s => s.id === sessionId);
                          setGallerySession(session);
                        }}
                        className="recommend-select"
                      >
                        <option value="">갤러리 세션 선택</option>
                        {sessions.map(session => (
                          <option key={session.id} value={session.id}>
                            {session.class_code} ({students[session.id]?.length || 0}명 참여)
                          </option>
                        ))}
                      </select>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="recommend-dashboard__grid">
        <div className="recommend-card" style={{ gridColumn: '1 / -1' }}>
          <div className="recommend-card__header">🎓 내 클래스 세션</div>
          <div className="recommend-card__content">
            {sessions.length === 0 && !loading ? (
              <div className="recommend-welcome">
                <div className="recommend-welcome__icon">📝</div>
                <p>생성된 클래스가 없습니다. 새 클래스를 생성해보세요!</p>
              </div>
            ) : (
              <div className="recommend-dashboard__grid">
                {sessions.map((session) => (
                  <div key={session.id} className="recommend-card">
                    <div className="recommend-card__header">클래스 코드: {session.class_code}</div>
                    <div className="recommend-card__content">
                      <div className="recommend-metrics">
                        <div className="recommend-metric">
                          <div className="recommend-metric__header">
                            <span className="recommend-metric__label">생성일</span>
                            <span className="recommend-metric__value">{new Date(session.created_at).toLocaleDateString()}</span>
                          </div>
                        </div>
                        <div className="recommend-metric">
                          <div className="recommend-metric__header">
                            <span className="recommend-metric__label">만료일</span>
                            <span className="recommend-metric__value">
                              {session.expires_at ? new Date(session.expires_at).toLocaleDateString() : '없음'}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="recommend-features">
                        <div className="recommend-feature">
                          <div className="recommend-feature__icon">👥</div>
                          <div className="recommend-feature__content">
                            <h4>참여 학생 ({students[session.id]?.length || 0}명)</h4>
                            {students[session.id]?.length > 0 ? (
                              <div>
                                {students[session.id].map((student) => (
                                  <p key={student.id} style={{ margin: '0.25rem 0', fontSize: '0.8rem' }}>
                                    {student.name} ({new Date(student.created_at).toLocaleDateString()})
                                  </p>
                                ))}
                              </div>
                            ) : (
                              <p>참여한 학생이 없습니다.</p>
                            )}
                          </div>
                        </div>
                      </div>

                      <button
                        onClick={() => setSelectedSession(session)}
                        className="recommend-btn recommend-btn--primary"
                      >
                        💬 AI 채팅
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {selectedSession && (
        <div className="recommend-dashboard__grid">
          
              <ChatInterface />
           
        </div>
      )}

      <div className="recommend-dashboard__grid">
        <div className="recommend-card" style={{ gridColumn: '1 / -1', padding: 0, overflow: 'hidden' }}>
          <ImageGenerator 
            user={user} 
            sessionId={currentGallerySession?.id || (user.current_session_id || null)} 
          />
        </div>
      </div>
    </div>
  );
}

export default TeacherDashboard;