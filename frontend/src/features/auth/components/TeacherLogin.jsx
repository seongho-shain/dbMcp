import { useState } from 'react';
import { useAuth } from '../../../AuthContext';
import './Auth.css';

function TeacherLogin() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await login({
        email,
        password
      }, 'teacher');
    } catch (err) {
      setError('로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="recommend-login-container">
      <div className="recommend-login-header">
        <h2>선생님 로그인</h2>
        <p>이메일과 비밀번호를 입력해주세요</p>
      </div>
      
      <form onSubmit={handleSubmit} className="recommend-login-form">
        <div className="recommend-input-group">
          <label htmlFor="email">이메일</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="이메일을 입력하세요"
          />
        </div>
        
        <div className="recommend-input-group">
          <label htmlFor="password">비밀번호</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="비밀번호를 입력하세요"
          />
        </div>
        
        {error && (
          <div className="recommend-error-message">
            {error}
          </div>
        )}
        
        <button 
          type="submit" 
          className="recommend-btn recommend-btn--primary"
          disabled={isLoading}
        >
          {isLoading ? '로그인 중...' : '로그인'}
        </button>
      </form>
    </div>
  );
}

export default TeacherLogin;