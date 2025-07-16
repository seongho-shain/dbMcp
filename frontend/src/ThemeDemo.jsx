import React from 'react';
import { ThemeProvider } from './contexts/ThemeContext';
import ThemeSelector from './components/ThemeSelector';
import ModernDashboard from './themes/modern/ModernTheme';
import CuteDashboard from './themes/cute/CuteTheme';
import SimpleDashboard from './themes/simple/SimpleTheme';
import RecommendDashboard from './themes/recommend/RecommendTheme';
import { useTheme } from './contexts/ThemeContext';
import './ThemeDemo.css';

// 각 테마별 컴포넌트를 렌더링하는 함수
const ThemeRenderer = () => {
  const { currentTheme } = useTheme();

  const renderTheme = () => {
    switch (currentTheme) {
      case 'modern':
        return <ModernDashboard />;
      case 'cute':
        return <CuteDashboard />;
      case 'simple':
        return <SimpleDashboard />;
      case 'recommend':
        return <RecommendDashboard />;
      default:
        return <RecommendDashboard />;
    }
  };

  return (
    <div className="theme-demo">
      <div className="theme-demo__header">
        <div className="theme-demo__nav">
          <div className="theme-demo__logo">
            <h1>🎨 Theme Demo</h1>
            <p>4가지 디자인 테마를 체험해보세요</p>
          </div>
          <ThemeSelector />
        </div>
      </div>
      
      <div className="theme-demo__content">
        {renderTheme()}
      </div>
    </div>
  );
};

// 메인 데모 컴포넌트
const ThemeDemo = () => {
  return (
    <ThemeProvider>
      <ThemeRenderer />
    </ThemeProvider>
  );
};

export default ThemeDemo;