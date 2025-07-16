"""
Pydantic 모델 정의
API 요청/응답 데이터 검증 및 직렬화를 위한 스키마 정의
MVC 패턴에서 데이터 전송 객체(DTO) 역할을 담당
"""
from pydantic import BaseModel
from typing import Optional


# 선생님 관련 스키마
class TeacherSignupRequest(BaseModel):
    """선생님 회원가입 요청 데이터"""
    name: str
    email: str
    password: str


class TeacherLoginRequest(BaseModel):
    """선생님 로그인 요청 데이터"""
    email: str
    password: str


class TeacherResponse(BaseModel):
    """선생님 정보 응답 데이터"""
    id: int
    name: str
    email: str
    created_at: str


# 학생 관련 스키마
class StudentLoginRequest(BaseModel):
    """학생 로그인 요청 데이터"""
    name: str
    class_code: str


class StudentResponse(BaseModel):
    """학생 정보 응답 데이터"""
    id: int
    name: str
    class_code: str
    session_id: int
    created_at: str


# 클래스 세션 관련 스키마
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


# 공통 응답 스키마
class LoginResponse(BaseModel):
    """로그인 응답 데이터"""
    user: dict
    message: str
    user_type: str


class CreateClassResponse(BaseModel):
    """클래스 생성 응답 데이터"""
    class_code: str
    session: ClassSessionResponse