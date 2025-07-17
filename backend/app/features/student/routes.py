"""
Student routes
API endpoints for student operations
"""
from fastapi import APIRouter

from .service import StudentService

router = APIRouter(prefix="/student", tags=["student"])
student_service = StudentService()


@router.get("/session/{session_id}/students")
async def get_session_students(session_id: int):
    """
    세션에 참여한 학생 목록 조회 API
    특정 클래스 세션에 참여한 모든 학생 정보를 조회
    
    Args:
        session_id: 세션 ID
        
    Returns:
        학생 목록
        
    Raises:
        HTTPException: 데이터베이스 오류 시 500 에러
    """
    return student_service.get_session_students(session_id)


@router.get("/{student_id}")
async def get_student_by_id(student_id: int):
    """
    학생 ID로 학생 정보 조회 API
    
    Args:
        student_id: 학생 ID
        
    Returns:
        학생 정보
        
    Raises:
        HTTPException: 데이터베이스 오류 시 500 에러
    """
    return student_service.get_student_by_id(student_id)