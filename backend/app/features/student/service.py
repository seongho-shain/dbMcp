"""
Student service
Business logic for student operations
"""
from app.core.services.database_service import DatabaseService
from app.core.models.schemas import StudentResponse


class StudentService:
    """
    학생 관련 비즈니스 로직을 처리하는 서비스
    세션 관리 및 학생 정보 조회 기능을 담당
    """
    
    def __init__(self):
        self.db_service = DatabaseService()

    def get_session_students(self, session_id: int) -> list:
        """
        세션에 참여한 학생 목록 조회
        
        Args:
            session_id: 세션 ID
            
        Returns:
            학생 목록
        """
        return self.db_service.get_session_students(session_id)

    def get_student_by_id(self, student_id: int) -> dict:
        """
        학생 ID로 학생 정보 조회
        
        Args:
            student_id: 학생 ID
            
        Returns:
            학생 정보
        """
        return self.db_service.get_student_by_id(student_id)