# 디자인 가이드라인 (Design Guidelines)

## 📋 목적
이 문서는 교육용 AI 챗봇 플랫폼의 프론트엔드 디자인 개선을 위한 공통 가이드라인을 제공합니다. 모든 agent들이 일관된 디자인 작업을 수행할 수 있도록 표준화된 규칙과 원칙을 정의합니다.

## 🎨 현재 디자인 시스템 분석

### 색상 체계 (Color Palette)
```css
/* 주요 색상 */
Primary Blue: #3b82f6 (rgb(59, 130, 246))
Primary Dark: #1d4ed8 (rgb(29, 78, 216))
Secondary Purple: #667eea, #764ba2 (gradient)

/* 배경 색상 */
Light Background: #f8fafc, #f5f5f5
Card Background: #ffffff
Input Background: #f8fafc

/* 텍스트 색상 */
Primary Text: #334155, #2c3e50
Secondary Text: #64748b, #475569
Muted Text: #94a3b8

/* 상태 색상 */
Success: #10b981, #28a745
Warning: #f59e0b
Error: #ef4444, #e74c3c
Info: #3b82f6
```

### 타이포그래피 (Typography)
```css
/* 폰트 패밀리 */
Font Family: system-ui, Avenir, Helvetica, Arial, sans-serif

/* 폰트 크기 */
Heading Large: 3.2em
Heading Medium: 1.5rem, 1.2rem
Heading Small: 1.1rem
Body: 1rem, 0.9rem
Caption: 0.8rem, 0.75rem

/* 폰트 두께 */
Light: 400
Medium: 500
Semibold: 600
```

### 간격 시스템 (Spacing System)
```css
/* 패딩/마진 */
xs: 0.25rem (4px)
sm: 0.5rem (8px)
md: 0.75rem (12px)
lg: 1rem (16px)
xl: 1.5rem (24px)
2xl: 2rem (32px)

/* 컴포넌트 간격 */
Component Gap: 1rem - 2rem
Section Gap: 2rem - 3rem
```

### 둥근 모서리 (Border Radius)
```css
/* 버튼 및 작은 요소 */
Small: 4px
Medium: 8px
Large: 12px
XLarge: 18px

/* 카드 및 컨테이너 */
Card: 8px - 12px
Modal: 12px - 16px
```

### 그림자 효과 (Shadow System)
```css
/* 카드 그림자 */
Card Shadow: 0 2px 4px rgba(0, 0, 0, 0.1)
Card Shadow Hover: 0 4px 12px rgba(0, 0, 0, 0.15)

/* 버튼 그림자 */
Button Shadow: 0 4px 12px rgba(59, 130, 246, 0.4)
Button Shadow Green: 0 4px 12px rgba(16, 185, 129, 0.4)

/* 포커스 링 */
Focus Ring: 0 0 0 3px rgba(59, 130, 246, 0.1)
```

## 🎯 디자인 원칙

### 1. 일관성 (Consistency)
- 모든 컴포넌트는 동일한 디자인 토큰을 사용해야 함
- 색상, 타이포그래피, 간격이 일관되어야 함
- 인터랙션 패턴이 예측 가능해야 함

### 2. 접근성 (Accessibility)
- 색상 대비는 WCAG 2.1 AA 기준을 만족해야 함
- 키보드 네비게이션이 가능해야 함
- 스크린 리더 지원을 고려해야 함

### 3. 반응형 (Responsive)
- 모바일 우선 디자인
- 768px, 1200px 브레이크포인트 활용
- 터치 친화적 인터페이스

### 4. 성능 (Performance)
- CSS 애니메이션은 transform과 opacity만 사용
- 불필요한 리플로우 방지
- 이미지 최적화 고려

## 📱 컴포넌트 디자인 규칙

### 버튼 (Buttons)
```css
/* 기본 버튼 스타일 */
.button {
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
}

/* 호버 효과 */
.button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(color, 0.4);
}

/* 비활성화 상태 */
.button:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  transform: none;
}
```

### 카드 (Cards)
```css
.card {
  background: white;
  border-radius: 8px-12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  border: 1px solid #e9ecef;
}
```

### 입력 필드 (Input Fields)
```css
.input {
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 0.9rem;
  transition: border-color 0.2s ease;
}

.input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}
```

### 메시지 (Messages)
```css
/* 사용자 메시지 */
.user-message {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  align-self: flex-end;
}

/* AI 메시지 */
.ai-message {
  background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
  color: #3730a3;
  align-self: flex-start;
}
```

## 🔧 기술적 구현 규칙

### CSS 구조
1. **파일 구조**: 컴포넌트별 CSS 파일 분리
2. **네이밍**: BEM 방법론 또는 모듈식 CSS 사용
3. **변수**: CSS 커스텀 프로퍼티 활용
4. **미디어 쿼리**: 모바일 우선 접근

### 애니메이션
```css
/* 페이드인 효과 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 바운스 효과 */
@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
```

### 반응형 브레이크포인트
```css
/* 태블릿 */
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

/* 모바일 */
@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }
}
```

## 🚀 새로운 디자인 컨셉 요구사항

### 필수 고려사항
1. **교육 환경에 적합한 디자인**
   - 집중도를 높이는 색상 선택
   - 읽기 쉬운 타이포그래피
   - 눈의 피로를 줄이는 배경색

2. **사용자 경험 개선**
   - 직관적인 네비게이션
   - 명확한 피드백 시스템
   - 로딩 상태 표시

3. **현대적 디자인 트렌드**
   - 미니멀리즘
   - 마이크로 인터랙션
   - 다크 모드 지원 (선택사항)

### 디자인 컨셉 제안 시 포함사항
1. **색상 팔레트** (최소 5가지 색상)
2. **타이포그래피 시스템**
3. **컴포넌트 디자인 예시**
4. **레이아웃 구조**
5. **인터랙션 패턴**

## 📋 검토 체크리스트

### 디자인 검토 항목
- [ ] 색상 대비 충분성 (4.5:1 이상)
- [ ] 모바일 반응형 지원
- [ ] 접근성 고려사항
- [ ] 브랜드 일관성
- [ ] 사용자 경험 개선점

### 기술적 검토 항목
- [ ] CSS 성능 최적화
- [ ] 브라우저 호환성
- [ ] 코드 구조 일관성
- [ ] 유지보수 용이성

## 📚 참고 자료

### 현재 프로젝트 파일
- `frontend/src/App.css` - 메인 애플리케이션 스타일
- `frontend/src/Auth.css` - 인증 관련 스타일
- `frontend/src/components/ChatInterface.css` - 채팅 인터페이스 스타일
- `frontend/src/index.css` - 전역 스타일

### 디자인 시스템 참고
- Material Design 3
- Tailwind CSS Design System
- Ant Design
- Chakra UI

---

**업데이트 날짜**: 2025-01-16  
**버전**: 1.0.0  
**작성자**: Design Team

> 💡 **Agent 참고사항**: 이 가이드라인을 기반으로 새로운 디자인 컨셉을 제안할 때는 기존 구조와의 호환성을 고려하되, 창의적이고 현대적인 접근을 시도해보세요.