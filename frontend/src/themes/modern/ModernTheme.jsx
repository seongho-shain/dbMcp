import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';
import './ModernTheme.css';

const ModernButton = ({ children, variant = 'primary', onClick, disabled = false }) => {
  return (
    <button 
      className={`modern-btn modern-btn--${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

const ModernCard = ({ title, children, className = '' }) => {
  return (
    <div className={`modern-card ${className}`}>
      {title && <div className="modern-card__header">{title}</div>}
      <div className="modern-card__content">
        {children}
      </div>
    </div>
  );
};

const ModernInput = ({ placeholder, value, onChange, type = 'text' }) => {
  return (
    <div className="modern-input-group">
      <input
        type={type}
        className="modern-input"
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
    </div>
  );
};

const ModernMessage = ({ message, isUser = false, timestamp }) => {
  return (
    <div className={`modern-message ${isUser ? 'modern-message--user' : 'modern-message--ai'}`}>
      <div className="modern-message__content">
        {message}
      </div>
      {timestamp && (
        <div className="modern-message__timestamp">
          {timestamp}
        </div>
      )}
    </div>
  );
};

const ModernChatInterface = () => {
  const { getThemeInfo } = useTheme();
  const themeInfo = getThemeInfo('modern');

  return (
    <div className="modern-chat">
      <div className="modern-chat__header">
        <h3>{themeInfo.icon} {themeInfo.name} Chat</h3>
        <div className="modern-chat__status">
          <span className="modern-status-dot"></span>
          Online
        </div>
      </div>
      
      <div className="modern-chat__messages">
        <ModernMessage 
          message="안녕하세요! Modern 테마의 AI 어시스턴트입니다. 어떤 것을 도와드릴까요?"
          isUser={false}
          timestamp="오후 2:30"
        />
        <ModernMessage 
          message="Modern 테마가 정말 멋지네요! 더 많은 기능을 보여주세요."
          isUser={true}
          timestamp="오후 2:31"
        />
        <ModernMessage 
          message="감사합니다! 이 테마는 다크 모드, 네온 효과, 그리고 글래스모피즘 디자인을 특징으로 합니다."
          isUser={false}
          timestamp="오후 2:31"
        />
      </div>
      
      <div className="modern-chat__input">
        <ModernInput placeholder="메시지를 입력하세요..." />
        <ModernButton variant="primary">전송</ModernButton>
      </div>
    </div>
  );
};

const ModernDashboard = () => {
  const { getThemeInfo } = useTheme();
  const themeInfo = getThemeInfo('modern');

  return (
    <div className="modern-dashboard">
      <div className="modern-dashboard__header">
        <h2>{themeInfo.icon} {themeInfo.name} Dashboard</h2>
        <p>{themeInfo.description}</p>
      </div>
      
      <div className="modern-dashboard__grid">
        <ModernCard title="🎯 학습 현황">
          <div className="modern-stats">
            <div className="modern-stat">
              <span className="modern-stat__value">85%</span>
              <span className="modern-stat__label">완료율</span>
            </div>
            <div className="modern-stat">
              <span className="modern-stat__value">24</span>
              <span className="modern-stat__label">세션</span>
            </div>
          </div>
        </ModernCard>
        
        <ModernCard title="🚀 최신 기능">
          <div className="modern-features">
            <div className="modern-feature">
              <span className="modern-feature__icon">✨</span>
              <span>AI 기반 학습 분석</span>
            </div>
            <div className="modern-feature">
              <span className="modern-feature__icon">🎨</span>
              <span>다크 모드 지원</span>
            </div>
            <div className="modern-feature">
              <span className="modern-feature__icon">⚡</span>
              <span>실시간 동기화</span>
            </div>
          </div>
        </ModernCard>
      </div>
      
      <div className="modern-dashboard__chat">
        <ModernChatInterface />
      </div>
    </div>
  );
};

export default ModernDashboard;