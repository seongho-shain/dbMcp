"""
Student feature module
학생 관련 기능을 담당하는 피처 모듈
"""

from .routes import router as student_router
from .service import StudentService

__all__ = ["student_router", "StudentService"]