"""
Auth feature models
Pydantic models for authentication requests and responses
"""
from pydantic import BaseModel
from typing import Optional


class TeacherSignupRequest(BaseModel):
    """선생님 회원가입 요청 데이터"""
    name: str
    email: str
    password: str


class TeacherLoginRequest(BaseModel):
    """선생님 로그인 요청 데이터"""
    email: str
    password: str


class StudentLoginRequest(BaseModel):
    """학생 로그인 요청 데이터"""
    name: str
    class_code: str


class TeacherResponse(BaseModel):
    """선생님 정보 응답 데이터"""
    id: int
    name: str
    email: str
    created_at: str


class StudentResponse(BaseModel):
    """학생 정보 응답 데이터"""
    id: int
    name: str
    class_code: str
    session_id: int
    created_at: str


class LoginResponse(BaseModel):
    """로그인 응답 데이터"""
    user: dict
    message: str
    user_type: str