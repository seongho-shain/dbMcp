import React from 'react';
import { useTheme } from '../../contexts/ThemeContext';
import './RecommendTheme.css';

const RecommendButton = ({ children, variant = 'primary', onClick, disabled = false }) => {
  return (
    <button 
      className={`recommend-btn recommend-btn--${variant}`}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

const RecommendCard = ({ title, children, className = '' }) => {
  return (
    <div className={`recommend-card ${className}`}>
      {title && <div className="recommend-card__header">{title}</div>}
      <div className="recommend-card__content">
        {children}
      </div>
    </div>
  );
};

const RecommendInput = ({ placeholder, value, onChange, type = 'text' }) => {
  return (
    <div className="recommend-input-group">
      <input
        type={type}
        className="recommend-input"
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
    </div>
  );
};

const RecommendMessage = ({ message, isUser = false, timestamp, attachments }) => {
  return (
    <div className={`recommend-message ${isUser ? 'recommend-message--user' : 'recommend-message--ai'}`}>
      <div className="recommend-message__content">
        {message}
        {attachments && attachments.length > 0 && (
          <div className="recommend-message__attachments">
            {attachments.map((attachment, idx) => (
              <div key={idx} className="recommend-attachment">
                <span className="recommend-attachment__icon">📎</span>
                <span className="recommend-attachment__name">{attachment.name}</span>
              </div>
            ))}
          </div>
        )}
      </div>
      {timestamp && (
        <div className="recommend-message__timestamp">
          {timestamp}
        </div>
      )}
    </div>
  );
};

const RecommendChatInterface = () => {
  const { getThemeInfo } = useTheme();
  const themeInfo = getThemeInfo('recommend');

  return (
    <div className="recommend-chat">
      <div className="recommend-chat__header">
        <h3>{themeInfo.icon} {themeInfo.name} AI 어시스턴트</h3>
        <div className="recommend-chat__status">
          <span className="recommend-status-dot"></span>
          <span>온라인</span>
        </div>
      </div>
      
      <div className="recommend-chat__messages">
        <div className="recommend-welcome">
          <div className="recommend-welcome__icon">👋</div>
          <p>안녕하세요! 교육에 최적화된 AI 어시스턴트입니다.</p>
          <p>궁금한 것이 있으면 언제든지 물어보세요!</p>
        </div>
        
        <RecommendMessage 
          message="교육용 AI 어시스턴트에 대해 알려주세요."
          isUser={true}
          timestamp="오후 2:30"
        />
        <RecommendMessage 
          message="안녕하세요! 저는 교육 환경에 특화된 AI 어시스턴트입니다. 학습 지원, 질문 답변, 그리고 파일 분석 등 다양한 기능을 제공합니다. 이 테마는 교육 전문가들의 의견을 바탕으로 학습 집중도와 사용 편의성을 높이도록 설계되었습니다."
          isUser={false}
          timestamp="오후 2:30"
        />
        <RecommendMessage 
          message="파일 첨부 기능도 잘 작동하나요?"
          isUser={true}
          timestamp="오후 2:31"
          attachments={[{ name: 'test.pdf' }]}
        />
        <RecommendMessage 
          message="네, 파일 첨부 기능이 완벽하게 작동합니다! 이미지, 텍스트, PDF 등 다양한 형식을 지원하며, 드래그 앤 드롭으로 쉽게 업로드할 수 있습니다."
          isUser={false}
          timestamp="오후 2:31"
        />
      </div>
      
      <div className="recommend-chat__input">
        <div className="recommend-input-wrapper">
          <RecommendInput placeholder="메시지를 입력하거나 파일을 드래그하세요..." />
          <button className="recommend-attach-btn" title="파일 첨부">📎</button>
        </div>
        <RecommendButton variant="primary">전송</RecommendButton>
      </div>
    </div>
  );
};

const RecommendDashboard = () => {
  const { getThemeInfo } = useTheme();
  const themeInfo = getThemeInfo('recommend');

  return (
    <div className="recommend-dashboard">
      <div className="recommend-dashboard__header">
        <h1>{themeInfo.icon} {themeInfo.name} Dashboard</h1>
        <p>{themeInfo.description}</p>
        <div className="recommend-badges">
          <span className="recommend-badge">교육 특화</span>
          <span className="recommend-badge">접근성 최적화</span>
          <span className="recommend-badge">사용성 개선</span>
        </div>
      </div>
      
      <div className="recommend-dashboard__grid">
        <RecommendCard title="📊 학습 현황" className="recommend-card--highlight">
          <div className="recommend-progress-ring">
            <svg className="recommend-progress-ring__svg" width="120" height="120">
              <circle
                className="recommend-progress-ring__circle-bg"
                cx="60"
                cy="60"
                r="50"
                fill="none"
                stroke="#e2e8f0"
                strokeWidth="8"
              />
              <circle
                className="recommend-progress-ring__circle-progress"
                cx="60"
                cy="60"
                r="50"
                fill="none"
                stroke="#3b82f6"
                strokeWidth="8"
                strokeDasharray="314"
                strokeDashoffset="47"
              />
              <text x="60" y="60" textAnchor="middle" dy="0.3em" className="recommend-progress-ring__text">
                85%
              </text>
            </svg>
          </div>
          <div className="recommend-stats-grid">
            <div className="recommend-stat-item">
              <span className="recommend-stat-item__value">24</span>
              <span className="recommend-stat-item__label">완료 세션</span>
            </div>
            <div className="recommend-stat-item">
              <span className="recommend-stat-item__value">6</span>
              <span className="recommend-stat-item__label">남은 세션</span>
            </div>
          </div>
        </RecommendCard>
        
        <RecommendCard title="🎯 추천 기능">
          <div className="recommend-features">
            <div className="recommend-feature">
              <div className="recommend-feature__icon">🎨</div>
              <div className="recommend-feature__content">
                <h4>균형잡힌 디자인</h4>
                <p>현대적이면서도 교육에 적합한 색상과 레이아웃</p>
              </div>
            </div>
            <div className="recommend-feature">
              <div className="recommend-feature__icon">♿</div>
              <div className="recommend-feature__content">
                <h4>접근성 최적화</h4>
                <p>WCAG 2.1 AA 기준 준수로 모든 사용자가 편리하게</p>
              </div>
            </div>
            <div className="recommend-feature">
              <div className="recommend-feature__icon">📚</div>
              <div className="recommend-feature__content">
                <h4>학습 집중도 향상</h4>
                <p>산만함을 최소화하고 학습에 집중할 수 있는 환경</p>
              </div>
            </div>
          </div>
        </RecommendCard>
        
        <RecommendCard title="📈 성능 지표">
          <div className="recommend-metrics">
            <div className="recommend-metric">
              <div className="recommend-metric__header">
                <span className="recommend-metric__label">사용자 만족도</span>
                <span className="recommend-metric__value">94%</span>
              </div>
              <div className="recommend-metric__bar">
                <div className="recommend-metric__fill" style={{ width: '94%' }}></div>
              </div>
            </div>
            <div className="recommend-metric">
              <div className="recommend-metric__header">
                <span className="recommend-metric__label">학습 효율성</span>
                <span className="recommend-metric__value">88%</span>
              </div>
              <div className="recommend-metric__bar">
                <div className="recommend-metric__fill" style={{ width: '88%' }}></div>
              </div>
            </div>
            <div className="recommend-metric">
              <div className="recommend-metric__header">
                <span className="recommend-metric__label">접근성 점수</span>
                <span className="recommend-metric__value">96%</span>
              </div>
              <div className="recommend-metric__bar">
                <div className="recommend-metric__fill" style={{ width: '96%' }}></div>
              </div>
            </div>
          </div>
        </RecommendCard>
      </div>
      
      <div className="recommend-dashboard__main">
        <RecommendChatInterface />
      </div>
    </div>
  );
};

export default RecommendDashboard;