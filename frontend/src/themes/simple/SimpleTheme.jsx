import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';
import './SimpleTheme.css';

const SimpleButton = ({ children, variant = 'primary', onClick, disabled = false }) => {
  return (
    <button 
      className={`simple-btn simple-btn--${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

const SimpleCard = ({ title, children, className = '' }) => {
  return (
    <div className={`simple-card ${className}`}>
      {title && <div className="simple-card__header">{title}</div>}
      <div className="simple-card__content">
        {children}
      </div>
    </div>
  );
};

const SimpleInput = ({ placeholder, value, onChange, type = 'text' }) => {
  return (
    <div className="simple-input-group">
      <input
        type={type}
        className="simple-input"
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
    </div>
  );
};

const SimpleMessage = ({ message, isUser = false, timestamp }) => {
  return (
    <div className={`simple-message ${isUser ? 'simple-message--user' : 'simple-message--ai'}`}>
      <div className="simple-message__content">
        {message}
      </div>
      {timestamp && (
        <div className="simple-message__timestamp">
          {timestamp}
        </div>
      )}
    </div>
  );
};

const SimpleChatInterface = () => {
  const { getThemeInfo } = useTheme();
  const themeInfo = getThemeInfo('simple');

  return (
    <div className="simple-chat">
      <div className="simple-chat__header">
        <h3>{themeInfo.name}</h3>
        <div className="simple-chat__indicator"></div>
      </div>
      
      <div className="simple-chat__messages">
        <SimpleMessage 
          message="안녕하세요. Simple 테마의 AI 어시스턴트입니다. 깔끔하고 집중할 수 있는 환경을 제공합니다."
          isUser={false}
          timestamp="14:30"
        />
        <SimpleMessage 
          message="정말 깔끔하고 집중하기 좋은 디자인이네요."
          isUser={true}
          timestamp="14:31"
        />
        <SimpleMessage 
          message="네, 불필요한 요소를 제거하고 가독성과 집중도를 높이는 것이 목표입니다."
          isUser={false}
          timestamp="14:31"
        />
      </div>
      
      <div className="simple-chat__input">
        <SimpleInput placeholder="메시지 입력" />
        <SimpleButton variant="primary">전송</SimpleButton>
      </div>
    </div>
  );
};

const SimpleDashboard = () => {
  const { getThemeInfo } = useTheme();
  const themeInfo = getThemeInfo('simple');

  return (
    <div className="simple-dashboard">
      <div className="simple-dashboard__header">
        <h1>{themeInfo.name}</h1>
        <p>{themeInfo.description}</p>
      </div>
      
      <div className="simple-dashboard__grid">
        <SimpleCard title="학습 진도">
          <div className="simple-progress">
            <div className="simple-progress__bar">
              <div className="simple-progress__fill" style={{ width: '85%' }}></div>
            </div>
            <div className="simple-progress__text">85% 완료</div>
          </div>
          <div className="simple-stats">
            <div className="simple-stat">
              <span className="simple-stat__value">24</span>
              <span className="simple-stat__label">완료된 세션</span>
            </div>
            <div className="simple-stat">
              <span className="simple-stat__value">6</span>
              <span className="simple-stat__label">남은 세션</span>
            </div>
          </div>
        </SimpleCard>
        
        <SimpleCard title="최근 활동">
          <div className="simple-activity">
            <div className="simple-activity__item">
              <div className="simple-activity__time">오늘 14:00</div>
              <div className="simple-activity__text">수학 문제 풀이 완료</div>
            </div>
            <div className="simple-activity__item">
              <div className="simple-activity__time">오늘 13:30</div>
              <div className="simple-activity__text">과학 개념 학습</div>
            </div>
            <div className="simple-activity__item">
              <div className="simple-activity__time">어제 16:00</div>
              <div className="simple-activity__text">영어 단어 암기</div>
            </div>
          </div>
        </SimpleCard>
      </div>
      
      <div className="simple-dashboard__main">
        <div className="simple-dashboard__sidebar">
          <div className="simple-nav">
            <div className="simple-nav__item simple-nav__item--active">대시보드</div>
            <div className="simple-nav__item">학습 자료</div>
            <div className="simple-nav__item">진도 관리</div>
            <div className="simple-nav__item">설정</div>
          </div>
        </div>
        
        <div className="simple-dashboard__content">
          <SimpleChatInterface />
        </div>
      </div>
    </div>
  );
};

export default SimpleDashboard;