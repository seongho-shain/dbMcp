"""
Teacher feature module
선생님 관련 기능을 담당하는 피처 모듈
"""

from .routes import router as teacher_router
from .service import TeacherService

__all__ = ["teacher_router", "TeacherService"]