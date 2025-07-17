"""
Image Generation routes
API endpoints for image generation operations
"""
import io
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import Optional

from .service import ImageGenerationService
from .models import (
    CoreImageRequest, SD35ImageRequest, UltraImageRequest, SketchRequest,
    FileValidationResponse, HealthCheckResponse, EducationalImageRequest, QuickImageRequest
)

router = APIRouter(prefix="/image", tags=["image-generation"])

# 이미지 생성 서비스 인스턴스
image_service = ImageGenerationService()

# 의존성 함수
async def get_image_service() -> ImageGenerationService:
    """이미지 생성 서비스 의존성"""
    return image_service


# 헬스체크 엔드포인트
@router.get("/health", response_model=HealthCheckResponse)
async def health_check(service: ImageGenerationService = Depends(get_image_service)):
    """이미지 생성 서비스 상태 확인"""
    health_info = await service.check_api_health()
    return HealthCheckResponse(**health_info)


# 상수 조회 엔드포인트
@router.get("/constants")
async def get_constants(service: ImageGenerationService = Depends(get_image_service)):
    """프론트엔드에서 사용할 상수들 반환"""
    return service.get_constants()


# 교육용 프롬프트 조회 엔드포인트
@router.get("/educational-prompts")
async def get_educational_prompts(
    subject: Optional[str] = None,
    service: ImageGenerationService = Depends(get_image_service)
):
    """교육용 프롬프트 예시 반환"""
    return service.get_educational_prompts(subject)


# 모델 정보 조회 엔드포인트
@router.get("/model-info/{model_type}")
async def get_model_info(
    model_type: str,
    service: ImageGenerationService = Depends(get_image_service)
):
    """모델 정보 반환"""
    return service.get_model_info(model_type)


# 파일 검증 엔드포인트
@router.post("/validate", response_model=FileValidationResponse)
async def validate_image(
    image: UploadFile = File(...),
    service: ImageGenerationService = Depends(get_image_service)
):
    """이미지 파일 검증"""
    return await service.validate_image_file(image)


# 이미지 생성 엔드포인트들

@router.post("/generate/core")
async def generate_core_image(
    # 폼 데이터로 받기
    prompt: str = Form(..., description="이미지 생성 프롬프트"),
    aspect_ratio: str = Form("1:1", description="이미지 비율"),
    output_format: str = Form("png", description="출력 형식"),
    style_preset: Optional[str] = Form(None, description="스타일 프리셋"),
    negative_prompt: Optional[str] = Form(None, description="네거티브 프롬프트"),
    seed: Optional[int] = Form(None, description="시드 값"),
    service: ImageGenerationService = Depends(get_image_service)
):
    """Stable Image Core로 이미지 생성"""
    
    # 요청 데이터 구성
    request_data = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "output_format": output_format
    }
    
    # 선택적 파라미터 추가
    if style_preset:
        request_data["style_preset"] = style_preset
    if negative_prompt:
        request_data["negative_prompt"] = negative_prompt
    if seed is not None:
        request_data["seed"] = seed
    
    # 이미지 생성
    image_data = await service.generate_core_image_data(request_data)
    
    # 파일명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"core_image_{timestamp}.{output_format}"
    
    # 스트리밍 응답으로 반환
    return StreamingResponse(
        io.BytesIO(image_data),
        media_type=f"image/{output_format}",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/generate/sd35")
async def generate_sd35_image(
    # 폼 데이터로 받기
    prompt: str = Form(..., description="이미지 생성 프롬프트"),
    mode: str = Form("text-to-image", description="생성 모드"),
    model: str = Form("sd3.5-large", description="사용할 모델"),
    aspect_ratio: Optional[str] = Form("1:1", description="이미지 비율"),
    strength: Optional[float] = Form(None, description="변형 강도"),
    output_format: str = Form("png", description="출력 형식"),
    style_preset: Optional[str] = Form(None, description="스타일 프리셋"),
    negative_prompt: Optional[str] = Form(None, description="네거티브 프롬프트"),
    seed: Optional[int] = Form(None, description="시드 값"),
    cfg_scale: Optional[float] = Form(None, description="CFG 스케일"),
    image: Optional[UploadFile] = File(None, description="입력 이미지"),
    service: ImageGenerationService = Depends(get_image_service)
):
    """Stable Diffusion 3.5로 이미지 생성"""
    
    # 요청 데이터 구성
    request_data = {
        "prompt": prompt,
        "mode": mode,
        "model": model,
        "output_format": output_format
    }
    
    # 선택적 파라미터 추가
    if aspect_ratio and mode == "text-to-image":
        request_data["aspect_ratio"] = aspect_ratio
    if strength is not None:
        request_data["strength"] = strength
    if style_preset:
        request_data["style_preset"] = style_preset
    if negative_prompt:
        request_data["negative_prompt"] = negative_prompt
    if seed is not None:
        request_data["seed"] = seed
    if cfg_scale is not None:
        request_data["cfg_scale"] = cfg_scale
    
    # 이미지 생성
    image_data = await service.generate_sd35_image(request_data, image)
    
    # 파일명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    mode_suffix = "i2i" if mode == "image-to-image" else "t2i"
    filename = f"sd35_{mode_suffix}_{timestamp}.{output_format}"
    
    # 스트리밍 응답으로 반환
    return StreamingResponse(
        io.BytesIO(image_data),
        media_type=f"image/{output_format}",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/generate/ultra")
async def generate_ultra_image(
    prompt: str = Form(..., description="이미지 생성 프롬프트"),
    aspect_ratio: str = Form("1:1", description="이미지 비율"),
    strength: Optional[float] = Form(None, description="참조 이미지 영향도"),
    output_format: str = Form("png", description="출력 형식"),
    style_preset: Optional[str] = Form(None, description="스타일 프리셋"),
    negative_prompt: Optional[str] = Form(None, description="네거티브 프롬프트"),
    seed: Optional[int] = Form(None, description="시드 값"),
    image: Optional[UploadFile] = File(None, description="참조 이미지"),
    service: ImageGenerationService = Depends(get_image_service)
):
    """Stable Image Ultra로 이미지 생성"""
    
    # 요청 데이터 구성
    request_data = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "output_format": output_format
    }
    
    # 선택적 파라미터 추가
    if strength is not None:
        request_data["strength"] = strength
    if style_preset:
        request_data["style_preset"] = style_preset
    if negative_prompt:
        request_data["negative_prompt"] = negative_prompt
    if seed is not None:
        request_data["seed"] = seed
    
    # 이미지 생성
    image_data = await service.generate_ultra_image(request_data, image)
    
    # 파일명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ultra_image_{timestamp}.{output_format}"
    
    # 스트리밍 응답으로 반환
    return StreamingResponse(
        io.BytesIO(image_data),
        media_type=f"image/{output_format}",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.post("/control/sketch")
async def sketch_to_image(
    prompt: str = Form(..., description="이미지 생성 프롬프트"),
    control_strength: float = Form(0.7, description="제어 강도"),
    output_format: str = Form("png", description="출력 형식"),
    style_preset: Optional[str] = Form(None, description="스타일 프리셋"),
    negative_prompt: Optional[str] = Form(None, description="네거티브 프롬프트"),
    seed: Optional[int] = Form(None, description="시드 값"),
    image: UploadFile = File(..., description="스케치 이미지"),
    service: ImageGenerationService = Depends(get_image_service)
):
    """스케치를 이미지로 변환"""
    
    # 요청 데이터 구성
    request_data = {
        "prompt": prompt,
        "control_strength": control_strength,
        "output_format": output_format
    }
    
    # 선택적 파라미터 추가
    if style_preset:
        request_data["style_preset"] = style_preset
    if negative_prompt:
        request_data["negative_prompt"] = negative_prompt
    if seed is not None:
        request_data["seed"] = seed
    
    # 이미지 생성
    image_data = await service.sketch_to_image(request_data, image)
    
    # 파일명 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sketch_result_{timestamp}.{output_format}"
    
    # 스트리밍 응답으로 반환
    return StreamingResponse(
        io.BytesIO(image_data),
        media_type=f"image/{output_format}",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# 교육용 특화 엔드포인트들

@router.post("/generate/educational")
async def generate_educational_image(
    prompt: str = Form(..., description="교육용 이미지 생성 프롬프트"),
    subject: str = Form(..., description="교육 주제"),
    grade_level: Optional[str] = Form(None, description="학년 수준"),
    style: str = Form("illustration", description="교육용 스타일"),
    aspect_ratio: str = Form("16:9", description="이미지 비율"),
    output_format: str = Form("png", description="출력 형식"),
    service: ImageGenerationService = Depends(get_image_service)
):
    """교육용 이미지 생성 (Core 모델 사용)"""
    
    # 요청 데이터 구성
    request = EducationalImageRequest(
        prompt=prompt,
        subject=subject,
        grade_level=grade_level,
        style=style,
        aspect_ratio=aspect_ratio,
        output_format=output_format
    )
    
    # 교육용 이미지 생성
    result = await service.generate_educational_image(request)
    
    return result


@router.post("/generate/quick")
async def generate_quick_image(
    prompt: str = Form(..., description="간단한 프롬프트"),
    style: str = Form("illustration", description="스타일"),
    service: ImageGenerationService = Depends(get_image_service)
):
    """빠른 이미지 생성 (기본 설정 사용)"""
    
    # 요청 데이터 구성
    request = QuickImageRequest(
        prompt=prompt,
        style=style
    )
    
    # 빠른 이미지 생성
    result = await service.generate_quick_image(request)
    
    return result