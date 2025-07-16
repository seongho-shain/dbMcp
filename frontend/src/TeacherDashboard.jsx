import { useState, useEffect } from 'react'
import { useAuth } from './AuthContext'
import './App.css'

const API_BASE_URL = 'http://localhost:8000'

function TeacherDashboard() {
  const [sessions, setSessions] = useState([])
  const [students, setStudents] = useState({})
  const [loading, setLoading] = useState(false)
  const [creatingClass, setCreatingClass] = useState(false)
  const { user, logout } = useAuth()

  const fetchSessions = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/teacher/${user.id}/sessions`)
      if (response.ok) {
        const data = await response.json()
        setSessions(data)
        
        // Fetch students for each session
        const studentsData = {}
        for (const session of data) {
          const studentsResponse = await fetch(`${API_BASE_URL}/session/${session.id}/students`)
          if (studentsResponse.ok) {
            const sessionStudents = await studentsResponse.json()
            studentsData[session.id] = sessionStudents
          }
        }
        setStudents(studentsData)
      }
    } catch (error) {
      console.error('Error fetching sessions:', error)
    } finally {
      setLoading(false)
    }
  }

  const createNewClass = async () => {
    setCreatingClass(true)
    try {
      const response = await fetch(`${API_BASE_URL}/teacher/create-class`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ teacher_id: user.id })
      })
      
      if (response.ok) {
        const data = await response.json()
        alert(`새 클래스가 생성되었습니다! 클래스 코드: ${data.class_code}`)
        fetchSessions()
      }
    } catch (error) {
      console.error('Error creating class:', error)
      alert('클래스 생성에 실패했습니다.')
    } finally {
      setCreatingClass(false)
    }
  }

  useEffect(() => {
    fetchSessions()
  }, [])

  return (
    <div className="app">
      <div className="header">
        <h1>선생님 대시보드</h1>
        <div className="user-info">
          <span className="welcome-message">{user.name} 선생님 반갑습니다!</span>
          <button onClick={logout} className="logout-btn">로그아웃</button>
        </div>
      </div>
      
      <div className="dashboard-content">
        <div className="actions">
          <button 
            onClick={createNewClass} 
            disabled={creatingClass}
            className="create-class-btn"
          >
            {creatingClass ? '클래스 생성 중...' : '새 클래스 생성'}
          </button>
          <button onClick={fetchSessions} disabled={loading}>
            새로고침
          </button>
        </div>

        {loading && <p>로딩 중...</p>}

        <div className="sessions-section">
          <h2>내 클래스 세션</h2>
          {sessions.length === 0 && !loading ? (
            <p>생성된 클래스가 없습니다. 새 클래스를 생성해보세요!</p>
          ) : (
            <div className="sessions-grid">
              {sessions.map((session) => (
                <div key={session.id} className="session-card">
                  <h3>클래스 코드: {session.class_code}</h3>
                  <p>생성일: {new Date(session.created_at).toLocaleString()}</p>
                  <p>만료일: {session.expires_at ? new Date(session.expires_at).toLocaleString() : '없음'}</p>
                  
                  <div className="students-section">
                    <h4>참여 학생 ({students[session.id]?.length || 0}명)</h4>
                    {students[session.id]?.length > 0 ? (
                      <ul className="students-list">
                        {students[session.id].map((student) => (
                          <li key={student.id}>
                            {student.name} (참여: {new Date(student.created_at).toLocaleString()})
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p>참여한 학생이 없습니다.</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default TeacherDashboard