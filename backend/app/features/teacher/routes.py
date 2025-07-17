"""
선생님 관련 API 라우터
HTTP 요청을 받아 적절한 Service로 전달하고 응답을 반환
"""
from fastapi import APIRouter

from app.core.models.schemas import (
    CreateClassRequest,
    CreateClassResponse
)
from .service import TeacherService

router = APIRouter(prefix="/teacher", tags=["teacher"])
teacher_service = TeacherService()


@router.post("/create-class", response_model=CreateClassResponse)
async def create_class_session(request: CreateClassRequest):
    """
    클래스 세션 생성 API
    선생님이 새로운 클래스를 생성하고 학생들이 참여할 수 있는 코드를 발급
    
    Args:
        request: 클래스 생성 요청 데이터 (선생님 ID)
        
    Returns:
        생성된 클래스 코드와 세션 정보
        
    Raises:
        HTTPException: 세션 생성 실패 시 500 에러
    """
    return teacher_service.create_class_session(request)


@router.get("/{teacher_id}/sessions")
async def get_teacher_sessions(teacher_id: int):
    """
    선생님의 클래스 세션 목록 조회 API
    특정 선생님이 생성한 모든 클래스 세션을 조회
    
    Args:
        teacher_id: 선생님 ID
        
    Returns:
        클래스 세션 목록
        
    Raises:
        HTTPException: 데이터베이스 오류 시 500 에러
    """
    return teacher_service.get_teacher_sessions(teacher_id)


@router.delete("/session/{session_id}")
async def delete_session(session_id: int):
    """
    클래스 세션 삭제 API
    선생님이 생성한 클래스 세션을 삭제 (관련된 모든 데이터 포함)
    
    Args:
        session_id: 삭제할 세션 ID
        
    Returns:
        삭제 성공 메시지
        
    Raises:
        HTTPException: 세션을 찾을 수 없거나 삭제 실패 시 에러
    """
    return teacher_service.delete_session(session_id)