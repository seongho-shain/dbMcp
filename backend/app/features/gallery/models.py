"""
Gallery feature models
Pydantic models for gallery operations
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class GalleryItemCreate(BaseModel):
    """갤러리 아이템 생성 요청"""
    session_id: int
    user_id: int
    user_name: str
    user_type: str
    prompt: str
    title: Optional[str] = None


class GalleryItemResponse(BaseModel):
    """갤러리 아이템 응답"""
    id: int
    session_id: int
    user_id: int
    user_name: str
    user_type: str
    image_url: str
    prompt: str
    title: Optional[str] = None
    created_at: str


class GallerySessionResponse(BaseModel):
    """세션 갤러리 응답"""
    success: bool
    items: List[GalleryItemResponse]
    session_id: int


class GalleryStatsResponse(BaseModel):
    """갤러리 통계 응답"""
    total_items: int
    student_items: int
    teacher_items: int
    unique_contributors: int
    session_id: int


class GalleryDeleteResponse(BaseModel):
    """갤러리 삭제 응답"""
    success: bool
    message: str


class GalleryUploadResponse(BaseModel):
    """갤러리 업로드 응답"""
    success: bool
    message: str
    item: Optional[GalleryItemResponse] = None