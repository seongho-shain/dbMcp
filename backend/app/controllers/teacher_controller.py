"""
선생님 관련 비즈니스 로직 컨트롤러
MVC 패턴에서 Controller 역할을 담당
View(API 라우터)와 Service(데이터 접근) 사이의 중간 계층
비즈니스 로직 처리 및 데이터 검증을 담당
"""
from fastapi import HTTPException
from datetime import datetime, timedelta

from app.core.models.schemas import (
    TeacherSignupRequest, 
    TeacherLoginRequest, 
    TeacherResponse, 
    LoginResponse,
    CreateClassRequest,
    CreateClassResponse,
    ClassSessionResponse
)
from app.core.services.database_service import DatabaseService
from app.core.utils.security import hash_password, generate_class_code
from app.core.config.settings import SESSION_EXPIRE_HOURS


class TeacherController:
    """
    선생님 관련 비즈니스 로직을 처리하는 컨트롤러
    단일 책임 원칙에 따라 선생님 관련 기능만 담당
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

    def create_class_session(self, request: CreateClassRequest) -> CreateClassResponse:
        """
        클래스 세션 생성
        중복되지 않는 클래스 코드 생성 및 세션 생성
        
        Args:
            request: 클래스 생성 요청 데이터
            
        Returns:
            생성된 클래스 세션 정보
            
        Raises:
            HTTPException: 세션 생성 실패 시 500 에러
        """
        # 중복되지 않는 클래스 코드 생성
        class_code = self._generate_unique_class_code()
        
        # 세션 데이터 생성 (24시간 후 만료)
        session_data = {
            "teacher_id": request.teacher_id,
            "class_code": class_code,
            "expires_at": (datetime.now() + timedelta(hours=SESSION_EXPIRE_HOURS)).isoformat()
        }
        
        # 세션 생성
        created_session = self.db_service.create_class_session(session_data)
        
        return CreateClassResponse(
            class_code=class_code,
            session=ClassSessionResponse(**created_session)
        )

    def get_teacher_sessions(self, teacher_id: int) -> list:
        """
        선생님의 클래스 세션 목록 조회
        
        Args:
            teacher_id: 선생님 ID
            
        Returns:
            클래스 세션 목록
        """
        return self.db_service.get_teacher_sessions(teacher_id)

    def delete_session(self, session_id: int) -> dict:
        """
        클래스 세션 삭제
        세션과 관련된 모든 데이터 삭제 (학생, 채팅, 이미지 등)
        
        Args:
            session_id: 삭제할 세션 ID
            
        Returns:
            삭제 성공 메시지
            
        Raises:
            HTTPException: 세션을 찾을 수 없거나 삭제 실패 시 에러
        """
        # 세션 존재 확인
        session = self.db_service.get_session_by_id(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        try:
            # 세션 삭제 (cascade로 관련 데이터도 함께 삭제됨)
            self.db_service.delete_session(session_id)
            return {"message": "Session deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")

    def _generate_unique_class_code(self) -> str:
        """
        중복되지 않는 클래스 코드 생성
        데이터베이스에서 중복 확인 후 고유한 코드 반환
        
        Returns:
            고유한 클래스 코드
        """
        while True:
            class_code = generate_class_code()
            existing_session = self.db_service.get_session_by_class_code(class_code)
            if not existing_session:
                return class_code