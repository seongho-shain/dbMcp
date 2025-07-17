"""
Image Generation feature models
Pydantic models for image generation operations
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any


class CoreImageRequest(BaseModel):
    """Core 이미지 생성 요청"""
    prompt: str
    aspect_ratio: str = "1:1"
    output_format: str = "png"
    style_preset: Optional[str] = None
    negative_prompt: Optional[str] = None
    seed: Optional[int] = None


class SD35ImageRequest(BaseModel):
    """SD3.5 이미지 생성 요청"""
    prompt: str
    mode: str = "text-to-image"
    model: str = "sd3.5-large"
    aspect_ratio: Optional[str] = "1:1"
    strength: Optional[float] = None
    output_format: str = "png"
    style_preset: Optional[str] = None
    negative_prompt: Optional[str] = None
    seed: Optional[int] = None
    cfg_scale: Optional[float] = None


class UltraImageRequest(BaseModel):
    """Ultra 이미지 생성 요청"""
    prompt: str
    aspect_ratio: str = "1:1"
    strength: Optional[float] = None
    output_format: str = "png"
    style_preset: Optional[str] = None
    negative_prompt: Optional[str] = None
    seed: Optional[int] = None


class SketchRequest(BaseModel):
    """스케치→이미지 변환 요청"""
    prompt: str
    control_strength: float = 0.7
    output_format: str = "png"
    style_preset: Optional[str] = None
    negative_prompt: Optional[str] = None
    seed: Optional[int] = None


class ImageGenerationResponse(BaseModel):
    """이미지 생성 응답"""
    filename: str
    file_size: int
    generation_time: float
    credits_used: int
    width: Optional[int] = None
    height: Optional[int] = None
    model_used: str


class FileValidationResponse(BaseModel):
    """파일 검증 응답"""
    valid: bool
    message: str
    file_info: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """오류 응답"""
    error: str
    status_code: int


class HealthCheckResponse(BaseModel):
    """헬스체크 응답"""
    status: str
    api_available: bool
    timestamp: str
    service: str = "stability-ai"
    error: Optional[str] = None


class ModelInfoResponse(BaseModel):
    """모델 정보 응답"""
    name: str
    description: str
    credits_required: int
    supported_modes: list
    max_resolution: str


class EducationalImageRequest(BaseModel):
    """교육용 이미지 생성 요청"""
    prompt: str
    subject: str
    grade_level: Optional[str] = None
    style: str = "illustration"
    aspect_ratio: str = "16:9"
    output_format: str = "png"


class QuickImageRequest(BaseModel):
    """빠른 이미지 생성 요청"""
    prompt: str
    style: str = "illustration"