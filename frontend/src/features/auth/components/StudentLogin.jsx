import { useState } from 'react';
import { useAuth } from '../../../AuthContext';
import './Auth.css';

function StudentLogin() {
  const [classCode, setClassCode] = useState('');
  const [studentName, setStudentName] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await login({
        class_code: classCode,
        name: studentName
      }, 'student');
    } catch (err) {
      setError('로그인에 실패했습니다. 클래스 코드와 이름을 확인해주세요.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="recommend-login-container">
      <div className="recommend-login-header">
        <h2>학생 로그인</h2>
        <p>클래스 코드와 이름을 입력해주세요</p>
      </div>
      
      <form onSubmit={handleSubmit} className="recommend-login-form">
        <div className="recommend-input-group">
          <label htmlFor="classCode">클래스 코드</label>
          <input
            id="classCode"
            type="text"
            value={classCode}
            onChange={(e) => setClassCode(e.target.value)}
            required
            placeholder="클래스 코드를 입력하세요"
          />
        </div>
        
        <div className="recommend-input-group">
          <label htmlFor="studentName">이름</label>
          <input
            id="studentName"
            type="text"
            value={studentName}
            onChange={(e) => setStudentName(e.target.value)}
            required
            placeholder="이름을 입력하세요"
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

export default StudentLogin;