# 교육용 AI 챗봇 플랫폼 (dbMcp)

## 📋 프로젝트 개요

**교육용 AI 챗봇 플랫폼**은 선생님과 학생들이 함께 사용할 수 있는 종합적인 AI 기반 교육 지원 시스템입니다. FastAPI 백엔드와 React 프론트엔드로 구성되어 있으며, OpenAI GPT 모델과 Stability AI를 활용하여 교육적 가치가 있는 응답과 창작 활동을 지원합니다.

### 🎯 주요 목표
- 교육 환경에서 AI 어시스턴트를 통한 학습 지원
- 선생님과 학생 역할 기반 차별화된 서비스
- 실시간 스트리밍 채팅 경험 제공
- 파일 첨부를 통한 다양한 형태의 질문 지원
- AI 이미지 생성을 통한 창작 활동 지원
- 갤러리 시스템을 통한 작품 공유 및 관리

## 🏗️ 시스템 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │   External APIs │
│                 │    │                 │    │                 │
│ • 사용자 인증    │◄──►│ • MVC 패턴 구조  │◄──►│ • OpenAI API    │
│ • 실시간 채팅    │    │ • 역할 기반 인증 │    │ • Supabase MCP  │
│ • 파일 첨부      │    │ • 스트리밍 응답  │    │                 │
│ • 드래그앤드롭   │    │ • 파일 처리     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## ✨ 주요 기능

### 🔐 인증 시스템
- **선생님 계정**: 회원가입 및 로그인 기능
- **학생 계정**: 세션 ID 기반 간편 로그인
- **역할 기반 서비스**: 사용자 유형에 따른 차별화된 AI 응답

### 💬 실시간 채팅
- **스트리밍 응답**: OpenAI GPT-4o를 통한 실시간 텍스트 생성
- **채팅 히스토리**: 세션별 대화 기록 저장 및 로드
- **Thread 관리**: 연속적인 대화 컨텍스트 유지

### 📎 파일 첨부 기능
- **지원 형식**: 이미지(jpg, png, gif, webp), 텍스트(txt, md, csv, html, css, js, json, xml), PDF
- **드래그 앤 드롭**: 직관적인 파일 업로드 인터페이스
- **파일 크기 제한**: 10MB 이하 파일 지원
- **실시간 미리보기**: 첨부된 파일 정보 표시

### 🎨 AI 이미지 생성
- **Stability AI 통합**: Core, SD3.5, Ultra 모델 지원
- **다양한 생성 모드**: 텍스트→이미지, 이미지→이미지, 스케치→이미지
- **고급 옵션**: 스타일 프리셋, 종횡비, 시드값 설정
- **갤러리 연동**: 생성된 이미지를 바로 갤러리에 업로드

### 🖼️ 갤러리 시스템
- **Masonry 레이아웃**: Pinterest 스타일의 동적 이미지 배치
- **GSAP 애니메이션**: 부드러운 이미지 로딩 및 인터랙션 효과
- **세션별 관리**: 클래스별 작품 관리 및 격리
- **권한 기반 관리**: 학생은 본인 작품, 선생님은 모든 작품 관리

### 🤖 AI 어시스턴트
- **교육 특화**: 학습에 도움이 되는 답변 제공
- **컨텍스트 인식**: 사용자 역할에 따른 맞춤형 응답
- **파일 분석**: 첨부된 파일 내용 분석 및 관련 답변

## 🛠️ 기술 스택

### Backend
- **FastAPI**: 고성능 비동기 웹 프레임워크
- **Python 3.8+**: 메인 개발 언어
- **OpenAI API**: GPT 모델 활용
- **Supabase**: 데이터베이스 및 MCP 연동
- **Uvicorn**: ASGI 서버

### Frontend
- **React 19.1.0**: 사용자 인터페이스 구축
- **Vite**: 빠른 개발 환경
- **GSAP 3.13.0**: 고급 애니메이션 라이브러리
- **OGL 1.0.11**: WebGL 기반 그래픽 라이브러리
- **CSS3**: 반응형 디자인 및 테마 시스템
- **ES6+**: 최신 JavaScript 기능

### 개발 도구
- **ESLint**: 코드 품질 관리
- **VSCode**: 개발 환경 설정
- **Git**: 버전 관리

## 📁 프로젝트 구조

```
dbMcp/
├── backend/                 # FastAPI 백엔드 애플리케이션
│   ├── app/
│   │   ├── config/         # 설정 관리
│   │   │   └── settings.py # 환경 변수 및 설정
│   │   ├── controllers/    # 컨트롤러 레이어
│   │   │   ├── student_controller.py
│   │   │   └── teacher_controller.py
│   │   ├── models/         # 데이터 모델
│   │   │   └── schemas.py  # Pydantic 스키마 정의
│   │   ├── services/       # 비즈니스 로직
│   │   │   ├── database_service.py
│   │   │   └── openai_service.py     # OpenAI API 통합
│   │   ├── utils/          # 유틸리티 함수
│   │   │   └── security.py # 보안 관련 기능
│   │   └── views/          # 라우터 레이어
│   │       ├── chat_routes.py        # 채팅 관련 API
│   │       ├── main_routes.py        # 메인 라우트
│   │       ├── student_routes.py     # 학생 관련 API
│   │       └── teacher_routes.py     # 선생님 관련 API
│   └── main.py             # 애플리케이션 진입점
├── frontend/               # React 프론트엔드 애플리케이션
│   ├── src/
│   │   ├── components/     # 재사용 가능한 컴포넌트
│   │   │   ├── ChatInterface.jsx     # 채팅 인터페이스
│   │   │   └── ChatInterface.css     # 채팅 스타일
│   │   ├── AuthContext.jsx          # 인증 컨텍스트
│   │   ├── StudentDashboard.jsx     # 학생 대시보드
│   │   ├── StudentLogin.jsx         # 학생 로그인
│   │   ├── TeacherDashboard.jsx     # 선생님 대시보드
│   │   ├── TeacherLogin.jsx         # 선생님 로그인
│   │   ├── TeacherSignup.jsx        # 선생님 회원가입
│   │   └── App.jsx                  # 메인 앱 컴포넌트
│   ├── package.json        # 의존성 관리
│   └── vite.config.js      # Vite 설정
├── .mcp.json              # MCP 서버 설정
├── .vscode/               # VSCode 설정
└── README.md              # 프로젝트 문서
```

## 🔄 개발 진행 상황

### 최신 커밋 히스토리
- **518b50f**: 파일 첨부 기능 구현 (드래그 앤 드롭 포함)
- **b2470f5**: 실시간 스트리밍 채팅 기능 구현
- **28c97bc**: 채팅 인터페이스 향상 (사용자 메시지 즉시 렌더링)
- **8d1c252**: OpenAI 통합 AI 채팅 서비스 구현
- **8b1f92a**: MVC 패턴으로 리팩토링
- **258d95d**: Git 설정 및 VSCode 설정 업데이트

### 구현 완료 기능
✅ **인증 시스템**: 선생님/학생 구분 로그인  
✅ **실시간 채팅**: OpenAI GPT-4o 스트리밍 응답 지원  
✅ **파일 첨부**: 다양한 형식 지원 및 드래그 앤 드롭  
✅ **AI 이미지 생성**: Stability AI 통합 (Core, SD3.5, Ultra)  
✅ **갤러리 시스템**: Masonry 레이아웃과 GSAP 애니메이션  
✅ **MVC 아키텍처**: 코드 구조 개선  
✅ **채팅 히스토리**: 세션별 대화 기록  
✅ **데이터베이스 연동**: Supabase MCP 완전 통합  

### 최근 추가된 기능
🆕 **이미지 생성→갤러리 연동**: 생성된 이미지를 바로 갤러리에 업로드  
🆕 **권한 기반 갤러리 관리**: 사용자 역할별 작품 관리 권한  
🆕 **반응형 Masonry 레이아웃**: 화면 크기별 동적 컬럼 조정  

### 개발 중 또는 계획 중 기능
🔄 **고급 파일 처리**: PDF 및 문서 파일 분석 향상  
🔄 **실시간 알림**: 새 메시지 알림 시스템  
🔄 **관리자 패널**: 선생님용 학생 관리 기능  

## 🚀 설치 및 실행

### 백엔드 설정
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 프론트엔드 설정
```bash
cd frontend
npm install
npm run dev
```

### 환경 변수 설정
```bash
# backend/.env
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## 📖 API 문서

### 주요 엔드포인트

#### 인증 관련
- `POST /teacher/signup` - 선생님 회원가입
- `POST /teacher/login` - 선생님 로그인
- `POST /student/login` - 학생 로그인

#### 채팅 관련
- `GET /chat/history/{user_id}/{session_id}` - 채팅 히스토리 조회
- `POST /chat/ai/stream` - 스트리밍 AI 응답 (파일 첨부 지원)
- `POST /chat/message` - 일반 메시지 전송

#### 세션 관리
- `GET /session/{session_id}/students` - 세션 학생 목록

## ⚙️ 설정 파일

### MCP 설정 (.mcp.json)
```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase@latest"],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "your_token"
      }
    }
  }
}
```

### Vite 설정 (frontend/vite.config.js)
```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000'
    }
  }
})
```

## 🗺️ 개발 로드맵

### Phase 1: 기본 기능 (완료)
- ✅ 사용자 인증 시스템
- ✅ 기본 채팅 기능
- ✅ OpenAI API 연동

### Phase 2: 향상된 기능 (완료)
- ✅ 실시간 스트리밍 응답
- ✅ 파일 첨부 시스템
- ✅ 드래그 앤 드롭 UI

### Phase 3: 고급 기능 (진행 중)
- 🔄 완전한 데이터베이스 연동
- 🔄 고급 파일 분석 (PDF, 문서)
- 🔄 실시간 알림 시스템

### Phase 4: 확장 기능 (계획)
- 📋 학급 관리 기능
- 📋 학습 진도 추적
- 📋 AI 학습 분석 리포트
- 📋 모바일 앱 개발

## 🤝 기여 방법

1. 이슈 확인 및 생성
2. 기능 브랜치 생성
3. 코드 작성 및 테스트
4. Pull Request 제출

## 📜 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**최종 업데이트**: 2025년 1월 16일  
**버전**: 1.0.0  
**개발자**: Team dbMcp  

> 💡 **LLM을 위한 참고사항**: 이 프로젝트는 MVC 패턴으로 구조화된 교육용 AI 챗봇입니다. 백엔드는 FastAPI, 프론트엔드는 React로 구성되어 있으며, OpenAI API를 활용한 실시간 스트리밍 채팅과 파일 첨부 기능이 핵심입니다. 최신 개발 상황은 커밋 히스토리를 참조하세요.