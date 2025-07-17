"""
Chat feature models
Pydantic models for chat operations
"""
from pydantic import BaseModel
from typing import List, Dict, Any


class ChatRequest(BaseModel):
    """채팅 요청 데이터"""
    message: str
    user_id: int
    session_id: int
    user_name: str
    user_type: str  # 'teacher' or 'student'


class ChatResponse(BaseModel):
    """채팅 응답 데이터"""
    response: str
    thread_id: int
    user_message: Dict[str, Any]
    ai_message: Dict[str, Any]
    status: str = "success"


class ChatHistoryResponse(BaseModel):
    """채팅 기록 응답 데이터"""
    thread_id: int
    messages: List[Dict[str, Any]]
    status: str = "success"


class ChatHealthResponse(BaseModel):
    """채팅 서비스 상태 응답 데이터"""
    status: str
    service: str