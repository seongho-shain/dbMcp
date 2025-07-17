import { useState, useEffect } from 'react';
import { useAuth } from '../../../AuthContext';
import './TeacherDashboard.css';

const API_BASE_URL = 'http://localhost:8000';

function TeacherDashboard() {
  const [sessions, setSessions] = useState([]);
  const [students, setStudents] = useState({});
  const [loading, setLoading] = useState(false);
  const [creatingClass, setCreatingClass] = useState(false);
  const [currentSession, setCurrentSession] = useState(null);
  const { user, logout, updateUser } = useAuth();

  const fetchSessions = async () => {
    if (!user) return;
    
    setLoading(true);
    try {
      const teacherId = user.id || user.teacher_id || user.user_id;
      if (!teacherId) {
        console.error('Teacher ID not found in user object');
        return;
      }
      
      const response = await fetch(`${API_BASE_URL}/teacher/${teacherId}/sessions`);
      if (response.ok) {
        const data = await response.json();
        setSessions(data);

        const studentsData = {};
        for (const session of data) {
          const studentsResponse = await fetch(`${API_BASE_URL}/student/session/${session.id}/students`);
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
      console.log('User object:', user); // 디버깅용
      console.log('All user keys:', user ? Object.keys(user) : 'user is null'); // 디버깅용
      
      if (!user) {
        alert('사용자 정보가 없습니다. 다시 로그인해주세요.');
        return;
      }
      
      // user 객체에서 id를 찾아보기 (id, teacher_id, 다른 필드들 확인)
      const teacherId = user.id || user.teacher_id || user.user_id;
      console.log('Found teacher ID:', teacherId);
      
      if (!teacherId) {
        alert('선생님 ID를 찾을 수 없습니다. 다시 로그인해주세요.');
        return;
      }
      
      const requestBody = { teacher_id: teacherId };
      console.log('Request body:', requestBody);
      
      const response = await fetch(`${API_BASE_URL}/teacher/create-class`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody),
      });

      if (response.ok) {
        const data = await response.json();
        alert(`새 클래스가 생성되었습니다! 클래스 코드: ${data.class_code}`);
        fetchSessions();
      } else {
        const errorData = await response.json();
        console.error('Error response:', errorData);
        
        // 에러 메시지 더 자세히 표시
        let errorMessage = '알 수 없는 오류';
        if (errorData.detail) {
          if (Array.isArray(errorData.detail)) {
            errorMessage = errorData.detail.map(err => err.msg).join(', ');
          } else {
            errorMessage = errorData.detail;
          }
        }
        alert(`클래스 생성에 실패했습니다: ${errorMessage}`);
      }
    } catch (error) {
      console.error('Error creating class:', error);
      alert('클래스 생성에 실패했습니다.');
    } finally {
      setCreatingClass(false);
    }
  };

  const setCurrentSessionHandler = (session) => {
    setCurrentSession(session);
    // Update user context with current session info for chat, image, and gallery
    if (updateUser) {
      updateUser({
        ...user,
        current_session_id: session?.id,
        current_class_code: session?.class_code
      });
    }
  };

  const deleteSession = async (sessionId) => {
    if (!confirm('정말로 이 세션을 삭제하시겠습니까? 모든 데이터가 영구적으로 삭제됩니다.')) {
      return;
    }
    
    try {
      const response = await fetch(`${API_BASE_URL}/teacher/session/${sessionId}`, {
        method: 'DELETE'
      });
      
      if (response.ok) {
        alert('세션이 성공적으로 삭제되었습니다.');
        // 현재 세션이 삭제된 세션이면 초기화
        if (currentSession?.id === sessionId) {
          setCurrentSession(null);
          if (updateUser) {
            updateUser({
              ...user,
              current_session_id: null,
              current_class_code: null
            });
          }
        }
        // 세션 목록 새로고침
        fetchSessions();
      } else {
        const errorData = await response.json();
        alert(`세션 삭제 실패: ${errorData.detail || '알 수 없는 오류'}`);
      }
    } catch (error) {
      console.error('Error deleting session:', error);
      alert('세션 삭제 중 오류가 발생했습니다.');
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
          <div className="recommend-card__header">🎯 채팅 및 갤러리 세션 선택</div>
          <div className="recommend-card__content">
            <div className="recommend-features">
              <div className="recommend-feature">
                <div className="recommend-feature__icon">📋</div>
                <div className="recommend-feature__content">
                  <h4>현재 활성 세션</h4>
                  <p>
                    {currentSession 
                      ? `${currentSession.class_code} (${students[currentSession.id]?.length || 0}명 참여)`
                      : '선택된 세션이 없습니다'
                    }
                  </p>
                  <small style={{ color: 'var(--text-muted)', display: 'block', marginTop: '0.5rem' }}>
                    선택된 세션은 채팅, 이미지 생성, 갤러리에서 공통으로 사용됩니다.
                  </small>
                  {sessions.length > 0 && (
                    <div className="gallery-session-selector">
                      <select 
                        value={currentSession?.id || ''} 
                        onChange={(e) => {
                          const sessionId = parseInt(e.target.value);
                          const session = sessions.find(s => s.id === sessionId);
                          setCurrentSessionHandler(session);
                        }}
                        className="recommend-select"
                      >
                        <option value="">세션 선택</option>
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

                      <div className="recommend-actions">
                        <button
                          onClick={() => deleteSession(session.id)}
                          className="recommend-btn recommend-btn--danger"
                        >
                          🗑️ 삭제
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

    </div>
  );
}

export default TeacherDashboard;