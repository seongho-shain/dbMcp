import React, { useState } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import './ThemeSelector.css';

const ThemeSelector = () => {
  const { currentTheme, changeTheme, availableThemes, getThemeInfo } = useTheme();
  const [isOpen, setIsOpen] = useState(false);

  const handleThemeChange = (theme) => {
    changeTheme(theme);
    setIsOpen(false);
  };

  const toggleSelector = () => {
    setIsOpen(!isOpen);
  };

  const currentThemeInfo = getThemeInfo(currentTheme);

  return (
    <div className="theme-selector">
      <button
        className={`theme-selector__trigger ${isOpen ? 'theme-selector__trigger--open' : ''}`}
        onClick={toggleSelector}
        aria-label="테마 선택"
      >
        <span className="theme-selector__current-icon">{currentThemeInfo.icon}</span>
        <span className="theme-selector__current-name">{currentThemeInfo.name}</span>
        <span className="theme-selector__arrow">
          {isOpen ? '▲' : '▼'}
        </span>
      </button>

      {isOpen && (
        <div className="theme-selector__dropdown">
          <div className="theme-selector__header">
            <h3>테마 선택</h3>
            <p>원하는 디자인 테마를 선택하세요</p>
          </div>
          
          <div className="theme-selector__options">
            {availableThemes.map((theme) => {
              const themeInfo = getThemeInfo(theme);
              const isActive = theme === currentTheme;
              
              return (
                <button
                  key={theme}
                  className={`theme-option ${isActive ? 'theme-option--active' : ''}`}
                  onClick={() => handleThemeChange(theme)}
                  style={{ '--theme-color': themeInfo.color }}
                >
                  <div className="theme-option__icon">{themeInfo.icon}</div>
                  <div className="theme-option__content">
                    <div className="theme-option__name">{themeInfo.name}</div>
                    <div className="theme-option__description">{themeInfo.description}</div>
                  </div>
                  {isActive && (
                    <div className="theme-option__check">✓</div>
                  )}
                </button>
              );
            })}
          </div>
          
          <div className="theme-selector__footer">
            <p>선택한 테마는 자동으로 저장됩니다</p>
          </div>
        </div>
      )}
      
      {isOpen && (
        <div
          className="theme-selector__overlay"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  );
};

export default ThemeSelector;