import { useState } from 'react';
import { useAuth } from '../../../AuthContext';
import './Auth.css';

function TeacherSignup({ onSuccess }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { signup } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await signup({
        email,
        password,
        name
      }, 'teacher');
      onSuccess();
    } catch (err) {
      setError('회원가입에 실패했습니다. 이미 사용 중인 이메일일 수 있습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="recommend-login-container">
      <div className="recommend-login-header">
        <h2>선생님 회원가입</h2>
        <p>계정 정보를 입력해주세요</p>
      </div>
      
      <form onSubmit={handleSubmit} className="recommend-login-form">
        <div className="recommend-input-group">
          <label htmlFor="name">이름</label>
          <input
            id="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            placeholder="이름을 입력하세요"
          />
        </div>
        
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
          {isLoading ? '가입 중...' : '회원가입'}
        </button>
      </form>
    </div>
  );
}

export default TeacherSignup;