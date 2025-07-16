"""
학생 관련 비즈니스 로직 컨트롤러
MVC 패턴에서 Controller 역할을 담당
학생 로그인 및 클래스 참여 로직 처리
"""
from fastapi import HTTPException
from datetime import datetime

from app.models.schemas import (
    StudentLoginRequest,
    StudentResponse,
    LoginResponse
)
from app.services.database_service import DatabaseService


class StudentController:
    """
    학생 관련 비즈니스 로직을 처리하는 컨트롤러
    단일 책임 원칙에 따라 학생 관련 기능만 담당
    """
    
    def __init__(self):
        self.db_service = DatabaseService()

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

    def get_session_students(self, session_id: int) -> list:
        """
        세션에 참여한 학생 목록 조회
        
        Args:
            session_id: 세션 ID
            
        Returns:
            학생 목록
        """
        return self.db_service.get_session_students(session_id)