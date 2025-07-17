"""
Auth routes
API endpoints for authentication
"""
from fastapi import APIRouter

from .service import AuthService
from app.core.models.schemas import (
    TeacherSignupRequest,
    TeacherLoginRequest,
    StudentLoginRequest,
    TeacherResponse,
    LoginResponse
)

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/teacher/signup", response_model=TeacherResponse)
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
    return auth_service.signup_teacher(request)


@router.post("/teacher/login", response_model=LoginResponse)
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
    return auth_service.login_teacher(request)


@router.post("/student/login", response_model=LoginResponse)
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
    return auth_service.login_student(request)