# AI 교육 플랫폼 (AI Education Platform)

AI 기술을 활용한 교육용 플랫폼으로, 선생님과 학생들이 AI 채팅 및 이미지 생성 도구를 활용할 수 있는 웹 애플리케이션입니다.

## 🚀 주요 기능

### 👨‍🏫 선생님 기능
- **계정 관리**: 이메일 기반 회원가입/로그인
- **클래스 관리**: 클래스 생성 및 코드 제공
- **학생 관리**: 참여 학생 목록 확인
- **AI 채팅**: OpenAI GPT 모델을 통한 교육적 대화
- **이미지 생성**: Stability AI를 통한 다양한 이미지 생성
- **갤러리 관리**: 학생 작품 관리 및 모니터링

### 👩‍🎓 학생 기능
- **간편 참여**: 클래스 코드와 이름으로 간편 참여
- **AI 채팅**: 교육적 질문 및 답변
- **이미지 생성**: 창의적 이미지 생성
- **작품 공유**: 갤러리를 통한 작품 공유
- **파일 첨부**: 채팅 시 파일 첨부 지원

### 🎨 AI 이미지 생성
- **Stable Image Core**: 기본 이미지 생성 (3 크레딧)
- **Stable Diffusion 3.5**: 고급 이미지 생성 (4 크레딧)
- **Stable Image Ultra**: 최고급 이미지 생성 (8 크레딧)
- **스케치 변환**: 스케치를 완성된 이미지로 변환
- **다양한 스타일**: 애니메이션, 사진, 판타지 등 다양한 스타일 지원

## 🏗️ 기술 스택

### Backend
- **Framework**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **AI Services**: 
  - OpenAI GPT-4 (채팅)
  - Stability AI (이미지 생성)
- **Authentication**: JWT 기반 인증
- **File Storage**: 로컬 파일 시스템

### Frontend
- **Framework**: React 18 + Vite
- **Language**: JavaScript (ES6+)
- **Styling**: CSS3 (Custom Properties)
- **UI Components**: 커스텀 컴포넌트
- **State Management**: React Context API

## 📁 프로젝트 구조

### Backend (Feature-based Architecture)
```
backend/
├── app/
│   ├── core/                    # 핵심 서비스 및 설정
│   │   ├── config/
│   │   │   └── settings.py      # 애플리케이션 설정
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic 스키마
│   │   └── services/
│   │       └── database_service.py # 데이터베이스 서비스
│   ├── features/                # 기능별 모듈
│   │   ├── auth/               # 인증 기능
│   │   │   ├── router.py
│   │   │   └── service.py
│   │   ├── teacher/            # 선생님 기능
│   │   │   ├── router.py
│   │   │   └── service.py
│   │   └── student/            # 학생 기능
│   │       ├── router.py
│   │       └── service.py
│   └── views/                  # 기존 라우터 (레거시)
│       ├── chat_routes.py
│       ├── gallery_views.py
│       └── image_routes.py
├── main.py                     # 애플리케이션 진입점
└── requirements.txt
```

### Frontend (Feature-based Architecture)
```
frontend/
├── src/
│   ├── features/               # 기능별 모듈
│   │   ├── auth/              # 인증 관련
│   │   │   ├── components/
│   │   │   │   ├── StudentLogin.jsx
│   │   │   │   ├── TeacherLogin.jsx
│   │   │   │   └── TeacherSignup.jsx
│   │   │   └── index.js
│   │   ├── dashboard/         # 대시보드
│   │   │   ├── components/
│   │   │   │   ├── StudentDashboard.jsx
│   │   │   │   └── TeacherDashboard.jsx
│   │   │   └── index.js
│   │   ├── chat/              # 채팅 기능
│   │   │   ├── components/
│   │   │   │   └── ChatInterface.jsx
│   │   │   └── index.js
│   │   ├── gallery/           # 갤러리 기능
│   │   │   ├── components/
│   │   │   │   ├── Gallery.jsx
│   │   │   │   ├── GalleryItem.jsx
│   │   │   │   ├── GalleryUploadModal.jsx
│   │   │   │   └── Masonry.jsx
│   │   │   └── index.js
│   │   └── imageGeneration/   # 이미지 생성
│   │       ├── components/
│   │       │   └── ImageGenerator.jsx
│   │       └── index.js
│   ├── App.jsx                # 메인 앱 컴포넌트
│   ├── AuthContext.jsx        # 인증 컨텍스트
│   └── main.jsx              # 애플리케이션 진입점
├── index.html
└── package.json
```

## 🛠️ 설치 및 실행

### 사전 요구사항
- Python 3.10+
- Node.js 18+
- Conda (권장)

### 1. 백엔드 설정
```bash
# 저장소 클론
git clone <repository-url>
cd dbMcp

# Conda 환경 생성 및 활성화
conda create -n backend python=3.10
conda activate backend

# 의존성 설치
cd backend
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env 파일에 필요한 값들 설정:
# - SUPABASE_URL
# - SUPABASE_KEY
# - OPENAI_API_KEY
# - STABILITY_API_KEY

# 서버 실행
python main.py
```

### 2. 프론트엔드 설정
```bash
# 새 터미널에서
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev

# 또는 프로덕션 빌드
npm run build
npm run preview
```

### 3. 접속
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API 문서: http://localhost:8000/docs

## 🔧 환경 변수 설정

### Backend (.env)
```env
# Database
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# AI Services
OPENAI_API_KEY=your_openai_api_key
STABILITY_API_KEY=your_stability_api_key

# Application
DEBUG=True
SECRET_KEY=your_secret_key
```

## 🗄️ 데이터베이스 스키마

### 주요 테이블
- `teachers`: 선생님 정보
- `class_sessions`: 클래스 세션 정보
- `students`: 학생 정보
- `gallery_items`: 갤러리 아이템
- `chat_messages`: 채팅 메시지 (선택적)

## 🔐 인증 시스템

### 선생님 인증
- 이메일/비밀번호 기반 JWT 인증
- 클래스 생성 및 관리 권한

### 학생 인증
- 클래스 코드 + 이름으로 간편 참여
- 세션 기반 인증

## 🎯 주요 API 엔드포인트

### 인증
- `POST /auth/teacher/signup` - 선생님 회원가입
- `POST /auth/teacher/login` - 선생님 로그인
- `POST /auth/student/login` - 학생 로그인

### 선생님 기능
- `POST /teacher/create-class` - 클래스 생성
- `GET /teacher/{id}/sessions` - 클래스 목록 조회

### 학생 기능
- `GET /session/{id}/students` - 세션 학생 목록

### AI 기능
- `POST /chat/ai/stream` - AI 채팅 (스트리밍)
- `GET /chat/history/{user_id}/{session_id}` - 채팅 기록

### 이미지 생성
- `POST /api/image/generate/core` - Core 이미지 생성
- `POST /api/image/generate/sd35` - SD3.5 이미지 생성
- `POST /api/image/generate/ultra` - Ultra 이미지 생성
- `POST /api/image/control/sketch` - 스케치 변환

### 갤러리
- `GET /api/gallery/session/{id}` - 세션 갤러리 조회
- `POST /api/gallery/upload` - 작품 업로드
- `DELETE /api/gallery/{id}` - 작품 삭제

## 📝 주요 특징

### 1. Feature-based Architecture
- 기능별로 명확히 분리된 모듈 구조
- 높은 응집도와 낮은 결합도
- 유지보수성과 확장성 향상

### 2. 실시간 AI 채팅
- 스트리밍 기반 실시간 응답
- 파일 첨부 지원 (이미지, 텍스트, PDF)
- 교육적 컨텍스트 유지

### 3. 다양한 이미지 생성 옵션
- 3가지 품질 레벨 (Core, SD3.5, Ultra)
- 텍스트→이미지, 이미지→이미지, 스케치→이미지
- 20+ 스타일 프리셋 지원

### 4. 갤러리 시스템
- Masonry 레이아웃으로 아름다운 갤러리
- 세션별 작품 관리
- 권한 기반 작품 삭제

## 🧪 테스트

### Backend
```bash
conda activate backend
cd backend
python -m pytest tests/
```

### Frontend
```bash
cd frontend
npm test
```

### 빌드 검증
```bash
# Frontend 빌드 테스트
cd frontend
npm run build

# Backend 구문 검사
cd backend
python -m py_compile main.py
```

## 📈 성능 최적화

### Frontend
- React 18의 concurrent features 활용
- 코드 분할 및 지연 로딩
- 이미지 최적화

### Backend
- 비동기 데이터베이스 처리
- 스트리밍 응답으로 체감 성능 향상
- 효율적인 파일 처리

## 🛡️ 보안

### 인증 보안
- JWT 토큰 기반 인증
- 비밀번호 해싱
- CORS 설정

### 파일 보안
- 파일 타입 검증
- 파일 크기 제한
- 안전한 파일 저장

## 📊 모니터링

### 로깅
- 구조화된 로그 시스템
- 에러 추적 및 알림
- 성능 모니터링

### 분석
- 사용자 행동 분석
- AI 사용량 추적
- 성능 지표 수집

## 🚀 배포

### 개발 환경
```bash
# Backend
conda activate backend
cd backend
python main.py

# Frontend
cd frontend
npm run dev
```

### 프로덕션 환경
```bash
# Backend
conda activate backend
cd backend
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Frontend
cd frontend
npm run build
# 빌드된 파일을 웹서버에 배포
```

## 🤝 기여하기

1. 이 저장소를 포크합니다
2. 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

## 📜 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.

## 🆘 문제 해결

### 일반적인 문제들

1. **Conda 환경 문제**
   ```bash
   conda init
   conda activate backend
   ```

2. **포트 충돌**
   - Backend: 8000 포트 확인
   - Frontend: 5173 포트 확인

3. **API 키 오류**
   - .env 파일의 API 키 확인
   - 환경 변수 로드 확인

4. **빌드 오류**
   - 노드 모듈 재설치: `npm install`
   - 캐시 정리: `npm run clean`

### 연락처
프로젝트에 대한 질문이나 제안사항이 있으시면 이슈를 생성해주세요.

---

**Happy Coding! 🎉**