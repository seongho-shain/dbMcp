import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';
import './CuteTheme.css';

const CuteButton = ({ children, variant = 'primary', onClick, disabled = false }) => {
  return (
    <button 
      className={`cute-btn cute-btn--${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

const CuteCard = ({ title, children, className = '' }) => {
  return (
    <div className={`cute-card ${className}`}>
      {title && <div className="cute-card__header">{title}</div>}
      <div className="cute-card__content">
        {children}
      </div>
    </div>
  );
};

const CuteInput = ({ placeholder, value, onChange, type = 'text' }) => {
  return (
    <div className="cute-input-group">
      <input
        type={type}
        className="cute-input"
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
    </div>
  );
};

const CuteMessage = ({ message, isUser = false, timestamp }) => {
  return (
    <div className={`cute-message ${isUser ? 'cute-message--user' : 'cute-message--ai'}`}>
      <div className="cute-message__avatar">
        {isUser ? '🧑‍🎓' : '🤖'}
      </div>
      <div className="cute-message__bubble">
        <div className="cute-message__content">
          {message}
        </div>
        {timestamp && (
          <div className="cute-message__timestamp">
            {timestamp}
          </div>
        )}
      </div>
    </div>
  );
};

const CuteChatInterface = () => {
  const { getThemeInfo } = useTheme();
  const themeInfo = getThemeInfo('cute');

  return (
    <div className="cute-chat">
      <div className="cute-chat__header">
        <h3>{themeInfo.icon} {themeInfo.name} Chat</h3>
        <div className="cute-chat__mood">
          <span className="cute-mood-icon">😊</span>
          <span>Happy</span>
        </div>
      </div>
      
      <div className="cute-chat__messages">
        <CuteMessage 
          message="안녕하세요! 귀여운 테마의 AI 어시스턴트예요~ 무엇을 도와드릴까요? 💕"
          isUser={false}
          timestamp="오후 2:30"
        />
        <CuteMessage 
          message="와! 정말 귀여운 디자인이네요! 더 많은 기능을 보고 싶어요 ✨"
          isUser={true}
          timestamp="오후 2:31"
        />
        <CuteMessage 
          message="고마워요! 🥰 이 테마는 파스텔 색상과 부드러운 모양으로 친근한 느낌을 주도록 만들어졌어요!"
          isUser={false}
          timestamp="오후 2:31"
        />
      </div>
      
      <div className="cute-chat__input">
        <CuteInput placeholder="메시지를 입력해주세요~ 💬" />
        <CuteButton variant="primary">전송 💌</CuteButton>
      </div>
    </div>
  );
};

const CuteDashboard = () => {
  const { getThemeInfo } = useTheme();
  const themeInfo = getThemeInfo('cute');

  return (
    <div className="cute-dashboard">
      <div className="cute-dashboard__header">
        <h2>{themeInfo.icon} {themeInfo.name} Dashboard</h2>
        <p>{themeInfo.description}</p>
        <div className="cute-decorations">
          <span className="cute-star">⭐</span>
          <span className="cute-heart">💖</span>
          <span className="cute-flower">🌸</span>
        </div>
      </div>
      
      <div className="cute-dashboard__grid">
        <CuteCard title="🎯 학습 현황">
          <div className="cute-stats">
            <div className="cute-stat">
              <div className="cute-stat__icon">📚</div>
              <span className="cute-stat__value">85%</span>
              <span className="cute-stat__label">완료율</span>
            </div>
            <div className="cute-stat">
              <div className="cute-stat__icon">🎓</div>
              <span className="cute-stat__value">24</span>
              <span className="cute-stat__label">세션</span>
            </div>
          </div>
        </CuteCard>
        
        <CuteCard title="🌟 특별 기능">
          <div className="cute-features">
            <div className="cute-feature">
              <span className="cute-feature__icon">🎨</span>
              <span>파스텔 테마</span>
            </div>
            <div className="cute-feature">
              <span className="cute-feature__icon">🤗</span>
              <span>친근한 인터페이스</span>
            </div>
            <div className="cute-feature">
              <span className="cute-feature__icon">💕</span>
              <span>감정 표현 지원</span>
            </div>
          </div>
        </CuteCard>
        
        <CuteCard title="🎁 오늘의 선물">
          <div className="cute-gift">
            <div className="cute-gift__box">🎁</div>
            <p>매일 새로운 스티커와 이모지를 받아보세요!</p>
            <CuteButton variant="secondary">선물 받기</CuteButton>
          </div>
        </CuteCard>
      </div>
      
      <div className="cute-dashboard__chat">
        <CuteChatInterface />
      </div>
    </div>
  );
};

export default CuteDashboard;