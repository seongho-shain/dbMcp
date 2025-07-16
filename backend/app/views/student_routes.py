"""
학생 관련 API 라우터
MVC 패턴에서 View 역할을 담당
학생 로그인 및 세션 관련 API 엔드포인트 정의
"""
from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import (
    StudentLoginRequest,
    StudentResponse,
    LoginResponse
)
from app.controllers.student_controller import StudentController

# 학생 관련 API 라우터 생성
# prefix를 통해 모든 경로에 '/student' 접두사 추가
router = APIRouter(prefix="/student", tags=["students"])

# 컨트롤러 인스턴스 생성
student_controller = StudentController()


@router.post("/login", response_model=LoginResponse)
async def login_student(request: StudentLoginRequest):
    """
    학생 로그인 API
    클래스 코드를 통해 학생이 클래스 세션에 참여
    
    Args:
        request: 학생 로그인 요청 데이터 (이름, 클래스 코드)
        
    Returns:
        로그인 성공 응답 (학생 정보, 메시지, 사용자 타입)
        
    Raises:
        HTTPException: 클래스 코드 무효하거나 만료된 경우 401 에러
    """
    return student_controller.login_student(request)


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
    return student_controller.get_session_students(session_id)