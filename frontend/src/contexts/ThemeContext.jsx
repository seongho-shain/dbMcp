import React, { createContext, useContext, useState, useEffect } from 'react';

// 테마 타입 정의
export const THEMES = {
  MODERN: 'modern',
  CUTE: 'cute',
  SIMPLE: 'simple',
  RECOMMEND: 'recommend'
};

// 테마 컨텍스트 생성
const ThemeContext = createContext();

// 테마 프로바이더 컴포넌트
export const ThemeProvider = ({ children }) => {
  const [currentTheme, setCurrentTheme] = useState(THEMES.RECOMMEND);

  // 로컬 스토리지에서 테마 복원
  useEffect(() => {
    const savedTheme = localStorage.getItem('selectedTheme');
    if (savedTheme && Object.values(THEMES).includes(savedTheme)) {
      setCurrentTheme(savedTheme);
    }
  }, []);

  // 테마 변경 함수
  const changeTheme = (theme) => {
    if (Object.values(THEMES).includes(theme)) {
      setCurrentTheme(theme);
      localStorage.setItem('selectedTheme', theme);
      
      // 루트 엘리먼트에 테마 클래스 적용
      document.documentElement.className = `theme-${theme}`;
    }
  };

  // 다음 테마로 순환
  const nextTheme = () => {
    const themeArray = Object.values(THEMES);
    const currentIndex = themeArray.indexOf(currentTheme);
    const nextIndex = (currentIndex + 1) % themeArray.length;
    changeTheme(themeArray[nextIndex]);
  };

  // 테마 메타데이터
  const getThemeInfo = (theme) => {
    const themeInfos = {
      [THEMES.MODERN]: {
        name: 'Modern',
        description: '현대적이고 세련된 디자인',
        icon: '🚀',
        color: '#667eea'
      },
      [THEMES.CUTE]: {
        name: 'Cute',
        description: '귀엽고 친근한 파스텔 디자인',
        icon: '🎀',
        color: '#fbbf24'
      },
      [THEMES.SIMPLE]: {
        name: 'Simple',
        description: '깔끔하고 미니멀한 디자인',
        icon: '⚪',
        color: '#6b7280'
      },
      [THEMES.RECOMMEND]: {
        name: 'Recommend',
        description: '교육에 최적화된 추천 디자인',
        icon: '⭐',
        color: '#3b82f6'
      }
    };
    return themeInfos[theme] || themeInfos[THEMES.RECOMMEND];
  };

  // 초기 테마 클래스 적용
  useEffect(() => {
    document.documentElement.className = `theme-${currentTheme}`;
  }, [currentTheme]);

  const value = {
    currentTheme,
    changeTheme,
    nextTheme,
    getThemeInfo,
    availableThemes: Object.values(THEMES)
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

// 테마 컨텍스트 사용 훅
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// 테마별 스타일 적용 훅
export const useThemeStyles = () => {
  const { currentTheme } = useTheme();
  
  const getThemeClass = (baseClass) => {
    return `${baseClass} ${baseClass}--${currentTheme}`;
  };

  return {
    currentTheme,
    getThemeClass
  };
};