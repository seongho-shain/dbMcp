"""
이미지 생성 API 스키마 정의
Reference 폴더의 api_schemas.py를 기반으로 교육 시스템에 맞게 최적화된 스키마
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Literal, Union
from enum import Enum


# Enum 정의
class OutputFormat(str, Enum):
    PNG = "png"
    JPEG = "jpeg"
    WEBP = "webp"


class AspectRatio(str, Enum):
    ULTRA_WIDE = "21:9"
    LANDSCAPE_16_9 = "16:9"
    LANDSCAPE_3_2 = "3:2"
    LANDSCAPE_5_4 = "5:4"
    SQUARE = "1:1"
    PORTRAIT_4_5 = "4:5"
    PORTRAIT_2_3 = "2:3"
    PORTRAIT_9_16 = "9:16"
    ULTRA_PORTRAIT = "9:21"


class StylePreset(str, Enum):
    NONE = ""
    MODEL_3D = "3d-model"
    ANALOG_FILM = "analog-film"
    ANIME = "anime"
    CINEMATIC = "cinematic"
    COMIC_BOOK = "comic-book"
    DIGITAL_ART = "digital-art"
    ENHANCE = "enhance"
    FANTASY_ART = "fantasy-art"
    ISOMETRIC = "isometric"
    LINE_ART = "line-art"
    LOW_POLY = "low-poly"
    MODELING_COMPOUND = "modeling-compound"
    NEON_PUNK = "neon-punk"
    ORIGAMI = "origami"
    PHOTOGRAPHIC = "photographic"
    PIXEL_ART = "pixel-art"
    TILE_TEXTURE = "tile-texture"


class GenerationMode(str, Enum):
    TEXT_TO_IMAGE = "text-to-image"
    IMAGE_TO_IMAGE = "image-to-image"


class SD35Model(str, Enum):
    LARGE = "sd3.5-large"
    LARGE_TURBO = "sd3.5-large-turbo"
    MEDIUM = "sd3.5-medium"


# 기본 스키마
class BaseGenerationRequest(BaseModel):
    """기본 이미지 생성 요청 스키마"""
    prompt: str = Field(..., max_length=10000, description="생성할 이미지에 대한 설명")
    negative_prompt: Optional[str] = Field(None, max_length=10000, description="생성하지 않을 요소들")
    output_format: OutputFormat = Field(OutputFormat.PNG, description="출력 파일 형식")
    style_preset: Optional[StylePreset] = Field(StylePreset.NONE, description="스타일 프리셋")
    seed: Optional[int] = Field(None, ge=0, le=2147483647, description="랜덤 시드 (0 또는 None = 랜덤)")
    
    @validator('prompt')
    def prompt_not_empty(cls, v):
        if not v.strip():
            raise ValueError('프롬프트는 비어있을 수 없습니다')
        return v.strip()


# 이미지 생성 요청 스키마들
class CoreImageRequest(BaseGenerationRequest):
    """Stable Image Core 요청"""
    aspect_ratio: AspectRatio = Field(AspectRatio.SQUARE, description="이미지 종횡비")


class SD35ImageRequest(BaseGenerationRequest):
    """Stable Diffusion 3.5 요청"""
    mode: GenerationMode = Field(GenerationMode.TEXT_TO_IMAGE, description="생성 모드")
    model: SD35Model = Field(SD35Model.LARGE, description="사용할 SD3.5 모델")
    aspect_ratio: Optional[AspectRatio] = Field(AspectRatio.SQUARE, description="이미지 종횡비 (text-to-image 모드에서만)")
    strength: Optional[float] = Field(None, ge=0.0, le=1.0, description="변형 강도 (image-to-image 모드에서 필수)")
    cfg_scale: Optional[float] = Field(None, ge=1.0, le=10.0, description="프롬프트 준수도 (Large/Medium: 4, Turbo: 1)")
    
    @validator('aspect_ratio', always=True)
    def validate_aspect_ratio(cls, v, values):
        if values.get('mode') == GenerationMode.IMAGE_TO_IMAGE:
            return None  # image-to-image 모드에서는 aspect_ratio 사용 안함
        return v or AspectRatio.SQUARE
    
    @validator('strength', always=True)
    def validate_strength(cls, v, values):
        if values.get('mode') == GenerationMode.IMAGE_TO_IMAGE and v is None:
            raise ValueError('image-to-image 모드에서는 strength가 필수입니다')
        return v


class UltraImageRequest(BaseGenerationRequest):
    """Stable Image Ultra 요청"""
    aspect_ratio: AspectRatio = Field(AspectRatio.SQUARE, description="이미지 종횡비")
    strength: Optional[float] = Field(None, ge=0.0, le=1.0, description="참조 이미지 영향도")


# 이미지 제어 요청 스키마들
class BaseControlRequest(BaseGenerationRequest):
    """기본 이미지 제어 요청"""
    control_strength: float = Field(0.7, ge=0.0, le=1.0, description="제어 강도")


class SketchRequest(BaseControlRequest):
    """Sketch ControlNet 요청"""
    pass


# 응답 스키마들
class ImageGenerationResponse(BaseModel):
    """이미지 생성 성공 응답"""
    success: bool = True
    message: str = "이미지 생성 완료"
    filename: str
    file_size: int
    generation_time: float
    credits_used: int
    width: Optional[int] = None
    height: Optional[int] = None
    model_used: str


class ErrorResponse(BaseModel):
    """오류 응답"""
    success: bool = False
    error: str
    details: Optional[str] = None
    error_code: Optional[str] = None


class HealthCheckResponse(BaseModel):
    """헬스체크 응답"""
    status: str = "healthy"
    api_available: bool
    timestamp: str


class FileValidationResponse(BaseModel):
    """파일 검증 결과"""
    valid: bool
    message: str
    file_info: Optional[dict] = None


class ImageConstantsResponse(BaseModel):
    """프론트엔드에서 사용할 상수들"""
    output_formats: list[str]
    aspect_ratios: dict[str, str]
    style_presets: dict[str, str]
    sd35_models: dict[str, str]
    generation_modes: dict[str, str]


# 사용 예제를 위한 샘플 데이터
SAMPLE_REQUESTS = {
    "core": {
        "prompt": "A beautiful sunset over mountains, educational illustration style",
        "output_format": "png",
        "aspect_ratio": "16:9",
        "style_preset": "illustration",
        "seed": 12345
    },
    "sd35_text_to_image": {
        "prompt": "A futuristic classroom with students using holographic displays",
        "mode": "text-to-image",
        "model": "sd3.5-large",
        "aspect_ratio": "16:9",
        "output_format": "png",
        "style_preset": "digital-art"
    },
    "sd35_image_to_image": {
        "prompt": "Transform this into a colorful cartoon illustration",
        "mode": "image-to-image",
        "model": "sd3.5-large",
        "strength": 0.8,
        "output_format": "png",
        "style_preset": "anime"
    },
    "ultra": {
        "prompt": "A professional portrait of a teacher explaining complex concepts",
        "aspect_ratio": "3:4",
        "output_format": "jpeg",
        "style_preset": "photographic"
    },
    "sketch": {
        "prompt": "A detailed architectural drawing of a school building",
        "control_strength": 0.7,
        "output_format": "png",
        "style_preset": "illustration"
    }
}

# 교육용 프롬프트 예시 (제거됨 - 사용자 요청)
# EDUCATIONAL_PROMPT_EXAMPLES = {}

# 스타일 프리셋 설명
STYLE_PRESET_DESCRIPTIONS = {
    "": "기본 스타일",
    "3d-model": "3D 모델링 스타일",
    "analog-film": "아날로그 필름 스타일",
    "anime": "일본 애니메이션 스타일",
    "cinematic": "영화적 스타일",
    "comic-book": "만화책 스타일",
    "digital-art": "디지털 아트 스타일",
    "enhance": "품질 향상 스타일",
    "fantasy-art": "판타지 아트 스타일",
    "isometric": "아이소메트릭 스타일",
    "line-art": "선화 스타일",
    "low-poly": "로우 폴리 스타일",
    "modeling-compound": "모델링 컴파운드 스타일",
    "neon-punk": "네온펑크 스타일",
    "origami": "종이접기 스타일",
    "photographic": "사진과 같은 현실적 스타일",
    "pixel-art": "픽셀 아트 스타일",
    "tile-texture": "타일 텍스처 스타일"
}

# 종횡비 설명
ASPECT_RATIO_DESCRIPTIONS = {
    "21:9": "울트라 와이드 (시네마틱)",
    "16:9": "가로형 (프레젠테이션용)",
    "3:2": "가로형 (사진용)",
    "5:4": "가로형 (클래식)",
    "1:1": "정사각형 (소셜 미디어용)",
    "4:5": "세로형 (인스타그램)",
    "2:3": "세로형 (포스터용)",
    "9:16": "세로형 (모바일용)",
    "9:21": "울트라 포트레이트 (극세로)"
}

# 모델 설명
MODEL_DESCRIPTIONS = {
    "sd3.5-large": "최고 품질 (느림)",
    "sd3.5-large-turbo": "빠른 생성 (중간 품질)",
    "sd3.5-medium": "균형잡힌 품질과 속도"
}


# 유틸리티 함수들
def validate_request_for_model(model_type: str, request_data: dict) -> dict:
    """모델 타입에 따라 요청 데이터를 검증하고 정리"""
    if model_type == "core":
        return CoreImageRequest(**request_data).dict(exclude_none=True)
    elif model_type == "sd35":
        return SD35ImageRequest(**request_data).dict(exclude_none=True)
    elif model_type == "ultra":
        return UltraImageRequest(**request_data).dict(exclude_none=True)
    elif model_type == "sketch":
        return SketchRequest(**request_data).dict(exclude_none=True)
    else:
        raise ValueError(f"지원되지 않는 모델 타입: {model_type}")


def get_sample_request(model_type: str) -> dict:
    """모델 타입에 해당하는 샘플 요청 데이터 반환"""
    return SAMPLE_REQUESTS.get(model_type, {})


def get_educational_prompts(subject: str) -> list[str]:
    """교육 주제별 프롬프트 예시 반환 (제거됨)"""
    return []


def get_constants_for_frontend() -> dict:
    """프론트엔드에서 사용할 상수들 반환"""
    return {
        "output_formats": [e.value for e in OutputFormat],
        "aspect_ratios": {e.value: ASPECT_RATIO_DESCRIPTIONS[e.value] for e in AspectRatio},
        "style_presets": {e.value: STYLE_PRESET_DESCRIPTIONS[e.value] for e in StylePreset},
        "sd35_models": {e.value: MODEL_DESCRIPTIONS[e.value] for e in SD35Model},
        "generation_modes": {e.value: e.value.replace('-', ' ').title() for e in GenerationMode}
    }


def get_credits_required(model_type: str) -> int:
    """모델 타입별 필요 크레딧 반환"""
    credits_map = {
        "core": 3,
        "sd35": 4,  # 평균값 (3.5-6.5)
        "ultra": 8,
        "sketch": 3
    }
    return credits_map.get(model_type, 3)