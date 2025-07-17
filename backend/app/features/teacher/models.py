"""
Teacher feature models
Pydantic models for teacher-specific operations
"""
from pydantic import BaseModel
from typing import Optional


class CreateClassRequest(BaseModel):
    """클래스 생성 요청 데이터"""
    teacher_id: int


class ClassSessionResponse(BaseModel):
    """클래스 세션 응답 데이터"""
    id: int
    teacher_id: int
    class_code: str
    created_at: str
    expires_at: Optional[str] = None


class CreateClassResponse(BaseModel):
    """클래스 생성 응답 데이터"""
    class_code: str
    session: ClassSessionResponse