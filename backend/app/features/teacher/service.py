"""
선생님 관련 비즈니스 로직 서비스
클래스 세션 관리 등을 담당
"""
from fastapi import HTTPException
from datetime import datetime, timedelta

from app.core.models.schemas import (
    CreateClassRequest,
    CreateClassResponse,
    ClassSessionResponse
)
from app.core.services.database_service import DatabaseService
from app.core.utils.security import generate_class_code
from app.core.config.settings import SESSION_EXPIRE_HOURS


class TeacherService:
    """
    선생님 관련 비즈니스 로직을 처리하는 서비스
    클래스 세션 생성 및 관리 기능을 담당
    """
    
    def __init__(self):
        self.db_service = DatabaseService()

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