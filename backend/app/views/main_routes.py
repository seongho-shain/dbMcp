"""
메인 API 라우터
애플리케이션의 기본 엔드포인트 정의
헬스체크 및 루트 경로 처리
"""
from fastapi import APIRouter

# 메인 라우터 생성
router = APIRouter(tags=["main"])


@router.get("/")
async def read_root():
    """
    루트 경로 API
    애플리케이션의 기본 정보 반환
    
    Returns:
        애플리케이션 기본 메시지
    """
    return {"message": "Education System API"}


@router.get("/health")
async def health_check():
    """
    헬스체크 API
    애플리케이션 상태 확인용
    
    Returns:
        서버 상태 정보
    """
    return {"status": "healthy", "message": "Server is running"}