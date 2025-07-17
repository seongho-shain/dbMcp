import { useState } from 'react'
import { useAuth } from './AuthContext'
import Particles from './components/Particles'
import './Login.css'

const API_BASE_URL = 'http://localhost:8000'

function StudentLogin() {
  const [formData, setFormData] = useState({ name: '', class_code: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const { login } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch(`${API_BASE_URL}/student/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      })

      if (response.ok) {
        const data = await response.json()
        login(data.user, data.user_type)
        alert(data.message)
      } else {
        const errorData = await response.json()
        setError(errorData.detail || 'Login failed')
      }
    } catch (error) {
      setError('Network error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="auth-form">
      <h2>학생 로그인</h2>
      {error && <div className="error-message">{error}</div>}
      
      <div className="form-group">
        <input
          type="text"
          placeholder="이름"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
        />
      </div>
      
      <div className="form-group">
        <input
          type="text"
          placeholder="클래스 코드"
          value={formData.class_code}
          onChange={(e) => setFormData({ ...formData, class_code: e.target.value.toUpperCase() })}
          required
        />
      </div>
      
      <button type="submit" disabled={loading}>
        {loading ? '로그인 중...' : '로그인'}
      </button>
    </form>
  )
}

export default StudentLogin