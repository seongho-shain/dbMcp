"""
Student feature models
Pydantic models for student-specific operations
"""
from pydantic import BaseModel
from typing import List


class StudentResponse(BaseModel):
    """학생 정보 응답 데이터"""
    id: int
    name: str
    class_code: str
    session_id: int
    created_at: str


class SessionStudentsResponse(BaseModel):
    """세션 학생 목록 응답 데이터"""
    session_id: int
    students: List[StudentResponse]