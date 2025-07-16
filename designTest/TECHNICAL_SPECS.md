# 기술적 구현 사양 (Technical Specifications)

## 📋 목적
이 문서는 디자인 컨셉을 실제 코드로 구현할 때 필요한 기술적 제약사항, 요구사항, 그리고 구현 지침을 제공합니다. 모든 Agent는 이 사양을 준수하여 호환성과 품질을 보장해야 합니다.

## 🏗️ 프로젝트 구조 및 제약사항

### 현재 프로젝트 구조
```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx
│   │   └── ChatInterface.css
│   ├── App.jsx
│   ├── App.css
│   ├── Auth.css
│   ├── index.css
│   └── main.jsx
├── package.json
├── vite.config.js
└── index.html
```

### 변경 가능한 파일
- ✅ `src/App.css` - 메인 애플리케이션 스타일
- ✅ `src/Auth.css` - 인증 관련 스타일
- ✅ `src/components/ChatInterface.css` - 채팅 인터페이스 스타일
- ✅ `src/index.css` - 전역 스타일 (일부 수정 가능)

### 변경 금지 파일
- ❌ `src/main.jsx` - 애플리케이션 진입점
- ❌ `package.json` - 의존성 추가 금지
- ❌ `vite.config.js` - 빌드 설정 변경 금지
- ❌ React 컴포넌트 (.jsx 파일들) - 구조 변경 금지

## 🔧 기술 스택 및 제약사항

### 사용 가능한 기술
```json
{
  "CSS": "순수 CSS (CSS3 기능 포함)",
  "PostCSS": "불가 (설정 변경 금지)",
  "Sass/SCSS": "불가 (의존성 추가 금지)",
  "CSS-in-JS": "불가 (의존성 추가 금지)",
  "CSS Modules": "불가 (설정 변경 금지)",
  "Tailwind CSS": "불가 (의존성 추가 금지)"
}
```

### 브라우저 호환성
```yaml
최소 지원 브라우저:
  Chrome: 90+
  Firefox: 88+
  Safari: 14+
  Edge: 90+
  
모바일 지원:
  iOS Safari: 14+
  Android Chrome: 90+
```

### CSS 기능 제약사항
```css
/* 사용 가능한 CSS 기능 */
✅ CSS Custom Properties (CSS Variables)
✅ Flexbox
✅ CSS Grid
✅ CSS Animations & Transitions
✅ Media Queries
✅ Pseudo-classes & Pseudo-elements
✅ CSS Functions (calc, clamp, min, max)

/* 사용 금지 CSS 기능 */
❌ CSS @import (성능 이슈)
❌ CSS Filters (성능 이슈)
❌ CSS Backdrop-filter (호환성 이슈)
❌ CSS Subgrid (호환성 이슈)
❌ Experimental CSS properties
```

## 📁 파일 구조 및 네이밍 규칙

### CSS 파일 구조
```css
/* 1. CSS Variables */
:root {
  /* 색상 변수 */
  --primary-color: #3b82f6;
  
  /* 간격 변수 */
  --spacing-sm: 0.5rem;
  
  /* 타이포그래피 변수 */
  --font-size-base: 1rem;
}

/* 2. 기본 리셋 (필요시) */
* {
  box-sizing: border-box;
}

/* 3. 컴포넌트 스타일 */
.component {
  /* 스타일 */
}

/* 4. 유틸리티 클래스 */
.text-center {
  text-align: center;
}

/* 5. 미디어 쿼리 */
@media (max-width: 768px) {
  /* 반응형 스타일 */
}
```

### 클래스 네이밍 규칙
```css
/* BEM 방법론 권장 */
.block { }
.block__element { }
.block--modifier { }

/* 예시 */
.chat-interface { }
.chat-interface__header { }
.chat-interface__header--active { }

/* 또는 심플한 케밥 케이스 */
.chat-header { }
.chat-message { }
.chat-input { }
```

## 🎨 CSS 변수 시스템

### 색상 변수 구조
```css
:root {
  /* Primary Colors */
  --primary-50: #eff6ff;
  --primary-100: #dbeafe;
  --primary-200: #bfdbfe;
  --primary-300: #93c5fd;
  --primary-400: #60a5fa;
  --primary-500: #3b82f6;
  --primary-600: #2563eb;
  --primary-700: #1d4ed8;
  --primary-800: #1e40af;
  --primary-900: #1e3a8a;
  
  /* Gray Colors */
  --gray-50: #f9fafb;
  --gray-100: #f3f4f6;
  --gray-200: #e5e7eb;
  --gray-300: #d1d5db;
  --gray-400: #9ca3af;
  --gray-500: #6b7280;
  --gray-600: #4b5563;
  --gray-700: #374151;
  --gray-800: #1f2937;
  --gray-900: #111827;
  
  /* Semantic Colors */
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
  --info: #3b82f6;
}
```

### 간격 변수 구조
```css
:root {
  --spacing-0: 0;
  --spacing-1: 0.25rem;   /* 4px */
  --spacing-2: 0.5rem;    /* 8px */
  --spacing-3: 0.75rem;   /* 12px */
  --spacing-4: 1rem;      /* 16px */
  --spacing-5: 1.25rem;   /* 20px */
  --spacing-6: 1.5rem;    /* 24px */
  --spacing-8: 2rem;      /* 32px */
  --spacing-10: 2.5rem;   /* 40px */
  --spacing-12: 3rem;     /* 48px */
  --spacing-16: 4rem;     /* 64px */
  --spacing-20: 5rem;     /* 80px */
}
```

### 타이포그래피 변수 구조
```css
:root {
  /* Font Families */
  --font-sans: system-ui, -apple-system, sans-serif;
  --font-mono: ui-monospace, monospace;
  
  /* Font Sizes */
  --text-xs: 0.75rem;     /* 12px */
  --text-sm: 0.875rem;    /* 14px */
  --text-base: 1rem;      /* 16px */
  --text-lg: 1.125rem;    /* 18px */
  --text-xl: 1.25rem;     /* 20px */
  --text-2xl: 1.5rem;     /* 24px */
  --text-3xl: 1.875rem;   /* 30px */
  --text-4xl: 2.25rem;    /* 36px */
  
  /* Font Weights */
  --font-thin: 100;
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  --font-extrabold: 800;
  --font-black: 900;
  
  /* Line Heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;
}
```

## 📱 반응형 디자인 규칙

### 브레이크포인트 정의
```css
/* 모바일 우선 접근법 */
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}

/* 사용 예시 */
@media (min-width: 640px) {
  /* 태블릿 이상 */
}

@media (min-width: 1024px) {
  /* 데스크톱 이상 */
}
```

### 반응형 구현 가이드라인
```css
/* 1. 모바일 우선 */
.component {
  /* 모바일 스타일 */
  padding: var(--spacing-2);
  font-size: var(--text-sm);
}

/* 2. 태블릿 확장 */
@media (min-width: 768px) {
  .component {
    padding: var(--spacing-4);
    font-size: var(--text-base);
  }
}

/* 3. 데스크톱 확장 */
@media (min-width: 1024px) {
  .component {
    padding: var(--spacing-6);
    font-size: var(--text-lg);
  }
}
```

## ⚡ 성능 최적화 규칙

### 애니메이션 최적화
```css
/* 권장: transform과 opacity만 사용 */
.fade-in {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-in.active {
  opacity: 1;
  transform: translateY(0);
}

/* 금지: 레이아웃 속성 애니메이션 */
.bad-animation {
  /* ❌ 피하기 */
  transition: width 0.3s ease;
  transition: height 0.3s ease;
  transition: margin 0.3s ease;
  transition: padding 0.3s ease;
}
```

### CSS 최적화 규칙
```css
/* 1. 효율적인 선택자 사용 */
/* ✅ 좋음 */
.chat-message { }
.chat-message__content { }

/* ❌ 피하기 */
.chat .message .content .text { }
* + * { }

/* 2. will-change 속성 신중히 사용 */
.animated-element {
  will-change: transform;
  /* 애니메이션 후 제거 */
}

/* 3. 중복 스타일 방지 */
/* ✅ 좋음 */
.button {
  padding: var(--spacing-2) var(--spacing-4);
  border-radius: var(--radius-md);
}

.button-primary {
  background: var(--primary-500);
  color: white;
}
```

## 🔍 접근성 요구사항

### 색상 대비
```css
/* 최소 4.5:1 대비 유지 */
.text-primary {
  color: var(--gray-900); /* #111827 */
  background: white;      /* 대비 16.1:1 */
}

.text-secondary {
  color: var(--gray-700); /* #374151 */
  background: white;      /* 대비 8.9:1 */
}

/* 대비 확인 도구 사용 권장 */
/* https://webaim.org/resources/contrastchecker/ */
```

### 포커스 관리
```css
/* 포커스 표시 */
.interactive:focus {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}

/* 포커스 제거 시 대안 제공 */
.interactive:focus:not(:focus-visible) {
  outline: none;
}

.interactive:focus-visible {
  outline: 2px solid var(--primary-500);
  outline-offset: 2px;
}
```

### 터치 타겟 크기
```css
/* 최소 44px x 44px */
.touch-target {
  min-height: 44px;
  min-width: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

## 🧪 테스트 및 검증

### CSS 유효성 검사
```bash
# W3C CSS Validator 사용
# https://jigsaw.w3.org/css-validator/

# 로컬 검증 도구 (옵션)
# stylelint 사용 권장
```

### 브라우저 호환성 테스트
```javascript
// 필수 테스트 브라우저
const testBrowsers = [
  'Chrome 90+',
  'Firefox 88+',
  'Safari 14+',
  'Edge 90+',
  'iOS Safari 14+',
  'Android Chrome 90+'
];
```

### 성능 테스트
```css
/* 성능 측정 도구 */
/* 1. Chrome DevTools Lighthouse */
/* 2. WebPageTest */
/* 3. GTmetrix */

/* 목표 성능 지표 */
/* First Contentful Paint: < 2s */
/* Largest Contentful Paint: < 2.5s */
/* Cumulative Layout Shift: < 0.1 */
```

## 🚫 금지 사항

### 기술적 금지 사항
```css
/* 1. 외부 CSS 프레임워크 금지 */
/* ❌ Bootstrap, Tailwind, Bulma 등 */

/* 2. CSS 전처리기 금지 */
/* ❌ Sass, Less, Stylus 등 */

/* 3. PostCSS 플러그인 금지 */
/* ❌ autoprefixer, cssnano 등 */

/* 4. 실험적 CSS 속성 금지 */
/* ❌ :has(), @layer, @container 등 */
```

### 디자인 금지 사항
```css
/* 1. 접근성 위반 */
/* ❌ 대비 부족한 색상 조합 */
/* ❌ 포커스 표시 제거 */
/* ❌ 터치 타겟 크기 부족 */

/* 2. 성능 저하 요소 */
/* ❌ 복잡한 애니메이션 */
/* ❌ 과도한 그림자 효과 */
/* ❌ 대용량 배경 이미지 */
```

## 📊 품질 검증 체크리스트

### 코드 품질
- [ ] CSS 유효성 검사 통과
- [ ] 모든 브라우저에서 정상 렌더링
- [ ] 반응형 디자인 정상 작동
- [ ] 성능 영향 최소화

### 접근성
- [ ] 색상 대비 4.5:1 이상
- [ ] 키보드 네비게이션 가능
- [ ] 스크린 리더 호환성
- [ ] 터치 타겟 크기 적절

### 사용성
- [ ] 직관적인 인터페이스
- [ ] 명확한 피드백 시스템
- [ ] 일관된 디자인 언어
- [ ] 교육 환경 적합성

## 🔧 디버깅 및 트러블슈팅

### 일반적인 문제 해결
```css
/* 1. 플렉스박스 정렬 문제 */
.flex-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 2. 그리드 레이아웃 문제 */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-4);
}

/* 3. Z-index 문제 */
.modal {
  z-index: 1000;
}
.dropdown {
  z-index: 999;
}
```

### 브라우저별 호환성 문제
```css
/* Safari 특정 이슈 */
.safari-fix {
  -webkit-appearance: none;
  -webkit-transform: translateZ(0);
}

/* iOS 특정 이슈 */
.ios-fix {
  -webkit-overflow-scrolling: touch;
  -webkit-tap-highlight-color: transparent;
}
```

## 📋 제출 전 최종 체크리스트

### 필수 확인 항목
- [ ] 모든 CSS 파일 유효성 검사 통과
- [ ] 반응형 디자인 정상 작동
- [ ] 모든 브라우저에서 테스트 완료
- [ ] 성능 영향 최소화 확인
- [ ] 접근성 요구사항 충족
- [ ] 코드 주석 작성 완료

### 문서화 요구사항
- [ ] 구현 가이드 작성
- [ ] 변경 사항 목록 작성
- [ ] 테스트 결과 첨부
- [ ] 알려진 이슈 및 해결 방안 기록

---

**최종 업데이트**: 2025-01-16  
**버전**: 1.0.0  
**관리자**: Development Team

> ⚠️ **중요 알림**: 이 기술 사양을 준수하지 않는 구현물은 프로젝트에 통합될 수 없습니다. 작업 전 반드시 모든 제약사항을 확인하고 준수하세요.