# 디자인 컨셉 템플릿 (Design Concept Template)

## 📚 사용 가이드
이 템플릿은 Agent들이 디자인 컨셉을 제안할 때 사용하는 표준 형식입니다. 각 Agent는 이 구조를 따라 일관된 형태로 디자인 컨셉을 제출해야 합니다.

---

# 디자인 컨셉: {컨셉명}
**Agent ID**: {agent-name}  
**제출 날짜**: {YYYY-MM-DD}  
**버전**: 1.0.0  

## 🎨 컨셉 개요
{2-3줄로 디자인 컨셉의 핵심 아이디어와 목표를 설명}

### 디자인 철학
- **핵심 키워드**: {3-5개 키워드}
- **타겟 사용자**: 교사, 학생
- **디자인 목표**: {구체적인 목표 3가지}

## 🌈 색상 팔레트

### 메인 색상
```css
:root {
  /* Primary Colors */
  --primary-50: #hexcode;
  --primary-100: #hexcode;
  --primary-500: #hexcode;
  --primary-600: #hexcode;
  --primary-900: #hexcode;
  
  /* Secondary Colors */
  --secondary-50: #hexcode;
  --secondary-500: #hexcode;
  --secondary-900: #hexcode;
  
  /* Accent Colors */
  --accent-success: #hexcode;
  --accent-warning: #hexcode;
  --accent-error: #hexcode;
  --accent-info: #hexcode;
}
```

### 색상 사용 용도
- **Primary**: 메인 버튼, 링크, 강조 요소
- **Secondary**: 보조 버튼, 아이콘, 보더
- **Accent**: 상태 표시, 알림, 피드백
- **Neutral**: 텍스트, 배경, 그림자

### 접근성 검증
- [ ] Primary/White 대비: {ratio}:1 (AA 준수)
- [ ] Secondary/Background 대비: {ratio}:1 (AA 준수)
- [ ] 색맹 테스트 통과 여부: {통과/실패}

## 📚 타이포그래피 시스템

### 폰트 패밀리
```css
:root {
  --font-primary: 'System Font', -apple-system, sans-serif;
  --font-secondary: 'Monospace Font', monospace;
  --font-heading: 'Heading Font', serif; /* 선택사항 */
}
```

### 폰트 스케일
```css
:root {
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */
  --font-size-3xl: 1.875rem;  /* 30px */
  --font-size-4xl: 2.25rem;   /* 36px */
}
```

### 사용 예시
- **H1**: --font-size-4xl, font-weight: 700
- **H2**: --font-size-3xl, font-weight: 600
- **H3**: --font-size-2xl, font-weight: 600
- **Body**: --font-size-base, font-weight: 400
- **Caption**: --font-size-sm, font-weight: 400

## 🧩 핵심 컴포넌트 디자인

### 버튼 (Buttons)
```css
.btn {
  /* 기본 스타일 */
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius-md);
  font-weight: 600;
  transition: all 0.2s ease;
  
  /* 호버 효과 */
  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
  }
}

.btn-primary {
  background: var(--primary-500);
  color: white;
}

.btn-secondary {
  background: var(--secondary-500);
  color: white;
}
```

### 카드 (Cards)
```css
.card {
  background: white;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--spacing-xl);
  border: 1px solid var(--gray-200);
}

.card-header {
  border-bottom: 1px solid var(--gray-100);
  padding-bottom: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}
```

### 입력 필드 (Input Fields)
```css
.input {
  padding: var(--spacing-md);
  border: 2px solid var(--gray-300);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  transition: border-color 0.2s ease;
}

.input:focus {
  border-color: var(--primary-500);
  box-shadow: 0 0 0 3px var(--primary-100);
}
```

### 메시지 (Messages)
```css
.message {
  padding: var(--spacing-md);
  border-radius: var(--border-radius-lg);
  max-width: 80%;
  margin-bottom: var(--spacing-sm);
}

.message-user {
  background: var(--primary-500);
  color: white;
  align-self: flex-end;
}

.message-ai {
  background: var(--gray-100);
  color: var(--gray-900);
  align-self: flex-start;
}
```

## 📱 레이아웃 시스템

### 그리드 시스템
```css
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
}

.grid {
  display: grid;
  gap: var(--spacing-lg);
}

.grid-cols-1 { grid-template-columns: 1fr; }
.grid-cols-2 { grid-template-columns: 1fr 1fr; }
.grid-cols-3 { grid-template-columns: 1fr 1fr 1fr; }
```

### 간격 시스템
```css
:root {
  --spacing-xs: 0.25rem;   /* 4px */
  --spacing-sm: 0.5rem;    /* 8px */
  --spacing-md: 1rem;      /* 16px */
  --spacing-lg: 1.5rem;    /* 24px */
  --spacing-xl: 2rem;      /* 32px */
  --spacing-2xl: 3rem;     /* 48px */
}
```

### 반응형 브레이크포인트
```css
/* 모바일 우선 */
@media (min-width: 640px) {
  /* 태블릿 */
}

@media (min-width: 1024px) {
  /* 데스크톱 */
}

@media (min-width: 1280px) {
  /* 대형 데스크톱 */
}
```

## ⚡ 애니메이션 및 인터랙션

### 트랜지션 시스템
```css
:root {
  --transition-fast: 0.15s ease-out;
  --transition-base: 0.2s ease-out;
  --transition-slow: 0.3s ease-out;
}
```

### 마이크로 인터랙션
```css
/* 페이드 인 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 스케일 호버 */
.scale-hover:hover {
  transform: scale(1.05);
}

/* 로딩 애니메이션 */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

### 상태 피드백
- **로딩**: 스피너 애니메이션
- **성공**: 녹색 체크마크 + 페이드인
- **오류**: 빨간 경고 + 셰이크 애니메이션
- **정보**: 파란 아이콘 + 슬라이드인

## 📱 반응형 디자인 전략

### 모바일 (< 640px)
- 단일 컬럼 레이아웃
- 터치 친화적 버튼 크기 (최소 44px)
- 네비게이션 햄버거 메뉴
- 폰트 크기 최적화

### 태블릿 (640px - 1024px)
- 2컬럼 레이아웃
- 적응형 그리드 시스템
- 호버 효과 제한적 적용

### 데스크톱 (> 1024px)
- 3컬럼 레이아웃
- 완전한 호버 효과
- 키보드 네비게이션 지원

## 🎯 특별한 교육 환경 고려사항

### 집중력 향상 요소
- **색상**: 집중을 돕는 파란색 계열 활용
- **타이포그래피**: 가독성 높은 폰트 선택
- **레이아웃**: 깔끔하고 정리된 구조

### 사용자 경험 개선
- **교사용**: 효율적인 관리 도구 제공
- **학생용**: 직관적이고 친근한 인터페이스
- **공통**: 명확한 피드백 시스템

## 🚀 구현 계획

### 1단계: 기본 시스템 구축 (예상 시간: {X}시간)
- [ ] CSS 변수 시스템 구축
- [ ] 기본 컴포넌트 스타일 적용
- [ ] 타이포그래피 시스템 구현

### 2단계: 컴포넌트 개발 (예상 시간: {X}시간)
- [ ] 버튼 컴포넌트 스타일링
- [ ] 카드 컴포넌트 스타일링
- [ ] 입력 필드 컴포넌트 스타일링
- [ ] 메시지 컴포넌트 스타일링

### 3단계: 레이아웃 및 반응형 (예상 시간: {X}시간)
- [ ] 그리드 시스템 구현
- [ ] 반응형 레이아웃 적용
- [ ] 모바일 최적화

### 4단계: 애니메이션 및 최적화 (예상 시간: {X}시간)
- [ ] 트랜지션 효과 추가
- [ ] 마이크로 인터랙션 구현
- [ ] 성능 최적화

## 📊 장단점 분석

### 장점
1. **{장점 1}**: {구체적인 설명}
2. **{장점 2}**: {구체적인 설명}
3. **{장점 3}**: {구체적인 설명}

### 단점
1. **{단점 1}**: {구체적인 설명과 해결 방안}
2. **{단점 2}**: {구체적인 설명과 해결 방안}
3. **{단점 3}**: {구체적인 설명과 해결 방안}

### 리스크 요소
- **기술적 리스크**: {설명과 대응 방안}
- **시간적 리스크**: {설명과 대응 방안}
- **사용자 경험 리스크**: {설명과 대응 방안}

## ⏱️ 예상 작업 시간

| 작업 단계 | 예상 시간 | 난이도 |
|-----------|-----------|--------|
| 디자인 시스템 구축 | {X}시간 | 중간 |
| 컴포넌트 구현 | {X}시간 | 중간 |
| 반응형 최적화 | {X}시간 | 높음 |
| 애니메이션 구현 | {X}시간 | 낮음 |
| 테스트 및 디버깅 | {X}시간 | 중간 |
| **총 예상 시간** | **{X}시간** | **-** |

## 🔧 기술적 구현 세부사항

### 호환성 고려사항
- **브라우저**: Chrome, Firefox, Safari, Edge
- **모바일**: iOS Safari, Android Chrome
- **접근성**: WCAG 2.1 AA 준수

### 성능 최적화
- CSS 번들 크기: 현재 대비 {증가/감소} {X}%
- 렌더링 성능: 60fps 유지
- 로딩 시간: 초기 렌더링 {X}ms 이하

### 코드 품질
- CSS 유효성 검사 통과
- 린터 규칙 준수
- 일관된 네이밍 컨벤션

## 📋 테스트 계획

### 시각적 테스트
- [ ] 모든 브라우저에서 동일한 렌더링
- [ ] 반응형 디자인 정상 작동
- [ ] 접근성 도구 테스트 통과

### 사용자 테스트
- [ ] 교사 사용자 피드백
- [ ] 학생 사용자 피드백
- [ ] 사용성 테스트 수행

### 기술적 테스트
- [ ] 성능 벤치마크 통과
- [ ] 코드 품질 검사 통과
- [ ] 브라우저 호환성 검증

## 🔄 유지보수 계획

### 업데이트 전략
- 컴포넌트 기반 모듈화
- 버전 관리 시스템 적용
- 문서화 지속 관리

### 확장 가능성
- 새로운 컴포넌트 추가 용이성
- 테마 시스템 확장 가능성
- 다국어 지원 고려사항

---

**제출자**: {Agent Name}  
**검토자**: Design Team  
**승인일**: {YYYY-MM-DD}  

> 💡 **참고**: 이 템플릿을 사용하여 컨셉을 제출할 때는 모든 섹션을 완전히 작성하고, 코드 예시와 구체적인 시간 산정을 포함해야 합니다.