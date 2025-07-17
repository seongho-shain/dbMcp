"""
Auth service
Business logic for authentication operations
"""
from fastapi import HTTPException
from datetime import datetime

from app.core.services.database_service import DatabaseService
from app.core.utils.security import hash_password
from app.core.models.schemas import (
    TeacherSignupRequest, 
    TeacherLoginRequest, 
    StudentLoginRequest,
    TeacherResponse, 
    LoginResponse
)


class AuthService:
    """
    인증 관련 비즈니스 로직을 처리하는 서비스
    선생님과 학생의 회원가입 및 로그인 기능을 담당
    """
    
    def __init__(self):
        self.db_service = DatabaseService()

    def signup_teacher(self, request: TeacherSignupRequest) -> TeacherResponse:
        """
        선생님 회원가입 처리
        이메일 중복 확인 후 계정 생성
        
        Args:
            request: 회원가입 요청 데이터
            
        Returns:
            생성된 선생님 정보
            
        Raises:
            HTTPException: 이메일 중복 시 400 에러
        """
        # 이메일 중복 확인
        existing_teacher = self.db_service.get_teacher_by_email(request.email)
        if existing_teacher:
            raise HTTPException(status_code=400, detail="Teacher already exists")
        
        # 비밀번호 해싱 후 계정 생성
        teacher_data = {
            "name": request.name,
            "email": request.email,
            "password": hash_password(request.password)
        }
        
        created_teacher = self.db_service.create_teacher(teacher_data)
        return TeacherResponse(**created_teacher)

    def login_teacher(self, request: TeacherLoginRequest) -> LoginResponse:
        """
        선생님 로그인 처리
        이메일과 비밀번호 검증
        
        Args:
            request: 로그인 요청 데이터
            
        Returns:
            로그인 성공 응답
            
        Raises:
            HTTPException: 인증 실패 시 401 에러
        """
        # 이메일로 선생님 정보 조회
        teacher = self.db_service.get_teacher_by_email(request.email)
        if not teacher:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # 비밀번호 검증
        if teacher.get("password") != hash_password(request.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # 비밀번호 제거한 사용자 정보 반환
        teacher_response = {k: v for k, v in teacher.items() if k != "password"}
        
        return LoginResponse(
            user=teacher_response,
            message=f"{teacher['name']} 선생님 반갑습니다!",
            user_type="teacher"
        )

    def login_student(self, request: StudentLoginRequest) -> LoginResponse:
        """
        학생 로그인 처리
        클래스 코드 검증 후 세션 참여 또는 기존 학생 정보 반환
        
        Args:
            request: 학생 로그인 요청 데이터
            
        Returns:
            로그인 성공 응답
            
        Raises:
            HTTPException: 클래스 코드 무효하거나 만료된 경우 401 에러
        """
        # 클래스 코드로 세션 조회
        session = self.db_service.get_session_by_class_code(request.class_code)
        if not session:
            raise HTTPException(status_code=401, detail="Invalid class code")
        
        # 세션 만료 확인
        if session.get("expires_at"):
            expires_at = datetime.fromisoformat(session["expires_at"].replace('Z', '+00:00'))
            if expires_at < datetime.now():
                raise HTTPException(status_code=401, detail="Class code has expired")
        
        # 기존 학생 정보 확인
        existing_student = self.db_service.get_student_by_name_and_code(
            request.name, 
            request.class_code
        )
        
        if existing_student:
            # 기존 학생이면 기존 정보 반환
            student_response = existing_student
        else:
            # 새 학생이면 등록 후 정보 반환
            student_data = {
                "name": request.name,
                "class_code": request.class_code,
                "session_id": session["id"]
            }
            student_response = self.db_service.create_student(student_data)
        
        return LoginResponse(
            user=student_response,
            message=f"{request.name}님 반갑습니다!",
            user_type="student"
        )