"""
선생님 관련 API 라우터
MVC 패턴에서 View 역할을 담당
HTTP 요청을 받아 적절한 Controller로 전달하고 응답을 반환
URL 경로와 HTTP 메서드를 정의하고 요청/응답 데이터를 처리
"""
from fastapi import APIRouter, HTTPException
from typing import List

from app.core.models.schemas import (
    TeacherSignupRequest,
    TeacherLoginRequest, 
    TeacherResponse,
    LoginResponse,
    CreateClassRequest,
    CreateClassResponse
)
from app.controllers.teacher_controller import TeacherController

# 선생님 관련 API 라우터 생성
# prefix를 통해 모든 경로에 '/teacher' 접두사 추가
router = APIRouter(prefix="/teacher", tags=["teachers"])

# 컨트롤러 인스턴스 생성
teacher_controller = TeacherController()


@router.post("/signup", response_model=TeacherResponse)
async def signup_teacher(request: TeacherSignupRequest):
    """
    선생님 회원가입 API
    
    Args:
        request: 회원가입 요청 데이터 (이름, 이메일, 비밀번호)
        
    Returns:
        생성된 선생님 정보
        
    Raises:
        HTTPException: 이메일 중복 시 400 에러
    """
    return teacher_controller.signup_teacher(request)


@router.post("/login", response_model=LoginResponse)
async def login_teacher(request: TeacherLoginRequest):
    """
    선생님 로그인 API
    
    Args:
        request: 로그인 요청 데이터 (이메일, 비밀번호)
        
    Returns:
        로그인 성공 응답 (사용자 정보, 메시지, 사용자 타입)
        
    Raises:
        HTTPException: 인증 실패 시 401 에러
    """
    return teacher_controller.login_teacher(request)


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
    return teacher_controller.create_class_session(request)


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
    return teacher_controller.get_teacher_sessions(teacher_id)


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
    return teacher_controller.delete_session(session_id)