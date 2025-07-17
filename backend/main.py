"""
메인 애플리케이션 파일
FastAPI 애플리케이션 초기화 및 설정
Feature-based 구조로 리팩토링된 구조에서 애플리케이션 진입점 역할

리팩토링 이유:
1. 관심사 분리 (Separation of Concerns)
   - 각 기능별로 완전히 분리된 모듈 구조
   - 코드 유지보수성과 가독성 향상

2. 단일 책임 원칙 (Single Responsibility Principle)
   - 각 feature가 하나의 기능만 담당
   - 변경 시 영향 범위 최소화

3. 의존성 역전 원칙 (Dependency Inversion Principle)
   - 고수준 모듈이 저수준 모듈에 의존하지 않도록 설계
   - 인터페이스를 통한 느슨한 결합

4. 재사용성 및 확장성
   - 각 feature가 독립적으로 수정 가능
   - 새로운 기능 추가 시 기존 코드 수정 최소화

5. 테스트 용이성
   - 각 feature별로 단위 테스트 작성 가능
   - 모킹(Mocking)을 통한 독립적 테스트 가능
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config.settings import CORS_ORIGINS, SERVER_HOST, SERVER_PORT

# Feature-based 라우터 import
from app.features.auth.routes import router as auth_router
from app.features.teacher.routes import router as teacher_router
from app.features.student.routes import router as student_router

# 기존 라우트 유지 (아직 리팩토링 안 된 것들)
from app.views.main_routes import router as main_router
from app.views.chat_routes import router as chat_router
from app.views.gallery_views import router as gallery_router
from app.views.image_routes import router as image_generation_router

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="Education System API",
    description="Feature-based 구조로 구성된 교육 시스템 API",
    version="2.0.0"
)

# CORS 미들웨어 설정
# 프론트엔드에서 API 호출을 위한 CORS 정책 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,  # 허용할 오리진 목록
    allow_credentials=True,      # 인증 정보 포함 요청 허용
    allow_methods=["*"],         # 모든 HTTP 메서드 허용
    allow_headers=["*"],         # 모든 헤더 허용
)

# Feature-based API 라우터 등록
# 각 기능별로 완전히 분리된 라우터를 메인 애플리케이션에 포함
app.include_router(main_router)                      # 메인 라우트 (/, /health)
app.include_router(auth_router)                      # 인증 관련 라우트 (/auth/*)
app.include_router(teacher_router)                   # 선생님 관련 라우트 (/teacher/*)
app.include_router(student_router)                   # 학생 관련 라우트 (/student/*)
app.include_router(chat_router)                      # 채팅 관련 라우트 (/chat/*)
app.include_router(gallery_router)                   # 갤러리 관련 라우트 (/gallery/*)
app.include_router(image_generation_router)          # 이미지 생성 관련 라우트 (/image/*)

# 하위 호환성을 위한 추가 라우트 등록
# 기존 API 경로와의 호환성을 위해 prefix 추가
app.include_router(gallery_router, prefix="/api")          # /api/gallery/*
app.include_router(image_generation_router, prefix="/api") # /api/image/*

if __name__ == "__main__":
    # 개발 서버 실행
    # 프로덕션 환경에서는 별도의 WSGI 서버 사용 권장
    uvicorn.run(
        app, 
        host=SERVER_HOST, 
        port=SERVER_PORT,
        reload=True  # 개발 시 코드 변경 감지 및 자동 재시작
    )