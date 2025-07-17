"""
이미지 생성 라우트 정의
FastAPI 라우터를 통해 이미지 생성 API 엔드포인트 제공
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from typing import Optional
import io
from datetime import datetime

from app.controllers.image_controller import ImageController
from app.core.models.image_schemas import (
    CoreImageRequest, ImageGenerationResponse, ErrorResponse,
    FileValidationResponse, HealthCheckResponse
)

# 라우터 생성
router = APIRouter(
    prefix="/api/image",
    tags=["image-generation"],
    responses={404: {"description": "Not found"}}
)

# 이미지 컨트롤러 인스턴스
image_controller = ImageController()

# 의존성 함수
async def get_image_controller() -> ImageController:
    """이미지 컨트롤러 의존성"""
    return image_controller

# 헬스체크 엔드포인트
@router.get("/health", response_model=HealthCheckResponse)
async def health_check(controller: ImageController = Depends(get_image_controller)):
    """이미지 생성 서비스 상태 확인"""
    health_info = await controller.check_api_health()
    return HealthCheckResponse(**health_info)

# 상수 조회 엔드포인트
@router.get("/constants")
async def get_constants(controller: ImageController = Depends(get_image_controller)):
    """프론트엔드에서 사용할 상수들 반환"""
    return controller.get_constants()

# 교육용 프롬프트 조회 엔드포인트
@router.get("/educational-prompts")
async def get_educational_prompts(
    subject: Optional[str] = None,
    controller: ImageController = Depends(get_image_controller)
):
    """교육용 프롬프트 예시 반환"""
    return controller.get_educational_prompts(subject)

# 모델 정보 조회 엔드포인트
@router.get("/model-info/{model_type}")
async def get_model_info(
    model_type: str,
    controller: ImageController = Depends(get_image_controller)
):
    """모델 정보 반환"""
    return controller.get_model_info(model_type)

# 파일 검증 엔드포인트
@router.post("/validate", response_model=FileValidationResponse)
async def validate_image(
    image: UploadFile = File(...),
    controller: ImageController = Depends(get_image_controller)
):
    """이미지 파일 검증"""
    return await controller.validate_image_file(image)

# 이미지 생성 엔드포인트들

@router.post("/generate/core")
async def generate_core_image(
    request: Request,
    controller: ImageController = Depends(get_image_controller)
):
    """Stable Image Core로 이미지 생성"""
    
    # 폼 데이터 파싱 (채팅 API와 동일한 방식)
    form = await request.form()
    
    # 기본 파라미터 추출
    prompt = form.get('prompt', '')
    aspect_ratio = form.get('aspect_ratio', '1:1')
    output_format = form.get('output_format', 'png')
    style_preset = form.get('style_preset', None)
    negative_prompt = form.get('negative_prompt', None)
    
    # 안전한 정수 변환
    try:
        seed_str = form.get('seed', '')
        seed = int(seed_str) if seed_str and seed_str != 'undefined' and seed_str != '' else None
    except (ValueError, TypeError):
        seed = None
    
    # 사용자 정보 안전하게 추출
    try:
        user_id_str = form.get('user_id', '0')
        user_id = int(user_id_str) if user_id_str and user_id_str != 'undefined' else 0
    except (ValueError, TypeError):
        user_id = 0
    
    try:
        session_id_str = form.get('session_id', '0')
        session_id = int(session_id_str) if session_id_str and session_id_str != 'undefined' else 0
    except (ValueError, TypeError):
        session_id = 0
    
    user_name = form.get('user_name', '')
    user_type = form.get('user_type', '')
    
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
    image_data = await controller.generate_core_image_data(request_data)
    
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
    request: Request,
    controller: ImageController = Depends(get_image_controller)
):
    """Stable Diffusion 3.5로 이미지 생성"""
    
    # 폼 데이터 파싱 (채팅 API와 동일한 방식)
    form = await request.form()
    
    # 기본 파라미터 추출
    prompt = form.get('prompt', '')
    mode = form.get('mode', 'text-to-image')
    model = form.get('model', 'sd3.5-large')
    aspect_ratio = form.get('aspect_ratio', '1:1')
    output_format = form.get('output_format', 'png')
    style_preset = form.get('style_preset', None)
    negative_prompt = form.get('negative_prompt', None)
    
    # 안전한 숫자 변환
    try:
        strength_str = form.get('strength', '')
        strength = float(strength_str) if strength_str and strength_str != 'undefined' and strength_str != '' else None
    except (ValueError, TypeError):
        strength = None
    
    try:
        seed_str = form.get('seed', '')
        seed = int(seed_str) if seed_str and seed_str != 'undefined' and seed_str != '' else None
    except (ValueError, TypeError):
        seed = None
    
    try:
        cfg_scale_str = form.get('cfg_scale', '')
        cfg_scale = float(cfg_scale_str) if cfg_scale_str and cfg_scale_str != 'undefined' and cfg_scale_str != '' else None
    except (ValueError, TypeError):
        cfg_scale = None
    
    # 사용자 정보 안전하게 추출
    try:
        user_id_str = form.get('user_id', '0')
        user_id = int(user_id_str) if user_id_str and user_id_str != 'undefined' else 0
    except (ValueError, TypeError):
        user_id = 0
    
    try:
        session_id_str = form.get('session_id', '0')
        session_id = int(session_id_str) if session_id_str and session_id_str != 'undefined' else 0
    except (ValueError, TypeError):
        session_id = 0
    
    user_name = form.get('user_name', '')
    user_type = form.get('user_type', '')
    
    # 파일 파라미터 추출
    image = None
    for key, value in form.items():
        if key == 'image' and hasattr(value, 'filename') and value.filename:
            image = value
            break
    
    # 디버깅: 받은 파라미터 값 확인
    print(f"SD3.5 Route received - mode: '{mode}' (type: {type(mode)}), model: '{model}' (type: {type(model)})")
    
    # 요청 데이터 구성
    request_data = {
        "prompt": prompt,
        "mode": mode,
        "model": model,
        "output_format": output_format
    }
    
    print(f"SD3.5 Route request_data: {request_data}")
    
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
    image_data = await controller.generate_sd35_image(request_data, image)
    
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
    request: Request,
    controller: ImageController = Depends(get_image_controller)
):
    """Stable Image Ultra로 이미지 생성"""
    
    # 폼 데이터 파싱 (채팅 API와 동일한 방식)
    form = await request.form()
    
    # 기본 파라미터 추출
    prompt = form.get('prompt', '')
    aspect_ratio = form.get('aspect_ratio', '1:1')
    output_format = form.get('output_format', 'png')
    style_preset = form.get('style_preset', None)
    negative_prompt = form.get('negative_prompt', None)
    
    # 안전한 숫자 변환
    try:
        strength_str = form.get('strength', '')
        strength = float(strength_str) if strength_str and strength_str != 'undefined' and strength_str != '' else None
    except (ValueError, TypeError):
        strength = None
    
    try:
        seed_str = form.get('seed', '')
        seed = int(seed_str) if seed_str and seed_str != 'undefined' and seed_str != '' else None
    except (ValueError, TypeError):
        seed = None
    
    # 사용자 정보 안전하게 추출
    try:
        user_id_str = form.get('user_id', '0')
        user_id = int(user_id_str) if user_id_str and user_id_str != 'undefined' else 0
    except (ValueError, TypeError):
        user_id = 0
    
    try:
        session_id_str = form.get('session_id', '0')
        session_id = int(session_id_str) if session_id_str and session_id_str != 'undefined' else 0
    except (ValueError, TypeError):
        session_id = 0
    
    user_name = form.get('user_name', '')
    user_type = form.get('user_type', '')
    
    # 파일 파라미터 추출
    image = None
    for key, value in form.items():
        if key == 'image' and hasattr(value, 'filename') and value.filename:
            image = value
            break
    
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
    image_data = await controller.generate_ultra_image(request_data, image)
    
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
    request: Request,
    controller: ImageController = Depends(get_image_controller)
):
    """스케치를 이미지로 변환"""
    
    # 폼 데이터 파싱 (채팅 API와 동일한 방식)
    form = await request.form()
    
    # 기본 파라미터 추출
    prompt = form.get('prompt', '')
    output_format = form.get('output_format', 'png')
    style_preset = form.get('style_preset', None)
    negative_prompt = form.get('negative_prompt', None)
    
    # 안전한 숫자 변환
    try:
        control_strength_str = form.get('control_strength', '0.7')
        control_strength = float(control_strength_str) if control_strength_str and control_strength_str != 'undefined' else 0.7
    except (ValueError, TypeError):
        control_strength = 0.7
    
    try:
        seed_str = form.get('seed', '')
        seed = int(seed_str) if seed_str and seed_str != 'undefined' and seed_str != '' else None
    except (ValueError, TypeError):
        seed = None
    
    # 사용자 정보 안전하게 추출
    try:
        user_id_str = form.get('user_id', '0')
        user_id = int(user_id_str) if user_id_str and user_id_str != 'undefined' else 0
    except (ValueError, TypeError):
        user_id = 0
    
    try:
        session_id_str = form.get('session_id', '0')
        session_id = int(session_id_str) if session_id_str and session_id_str != 'undefined' else 0
    except (ValueError, TypeError):
        session_id = 0
    
    user_name = form.get('user_name', '')
    user_type = form.get('user_type', '')
    
    # 파일 파라미터 추출
    image = None
    for key, value in form.items():
        if key == 'image' and hasattr(value, 'filename') and value.filename:
            image = value
            break
    
    if not image:
        raise HTTPException(status_code=400, detail="스케치 이미지가 필요합니다.")
    
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
    image_data = await controller.sketch_to_image(request_data, image)
    
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
    controller: ImageController = Depends(get_image_controller)
):
    """교육용 이미지 생성 (Core 모델 사용)"""
    
    # 교육용 프롬프트 보강
    educational_prompt = f"Educational illustration for {subject}"
    if grade_level:
        educational_prompt += f" suitable for grade {grade_level}"
    educational_prompt += f": {prompt}"
    educational_prompt += ", clear and simple, educational style, colorful, engaging"
    
    # 요청 데이터 구성
    request_data = {
        "prompt": educational_prompt,
        "aspect_ratio": aspect_ratio,
        "output_format": output_format,
        "style_preset": style,
        "negative_prompt": "complex, confusing, inappropriate, violent, dark"
    }
    
    # Core 모델로 이미지 생성
    from app.core.models.image_schemas import CoreImageRequest
    request = CoreImageRequest(**request_data)
    result = await controller.generate_core_image(request)
    
    return result

@router.post("/generate/quick")
async def generate_quick_image(
    prompt: str = Form(..., description="간단한 프롬프트"),
    style: str = Form("illustration", description="스타일"),
    controller: ImageController = Depends(get_image_controller)
):
    """빠른 이미지 생성 (기본 설정 사용)"""
    
    # 기본 설정으로 Core 이미지 생성
    from app.core.models.image_schemas import CoreImageRequest
    request = CoreImageRequest(
        prompt=prompt,
        style_preset=style,
        aspect_ratio="1:1",
        output_format="png"
    )
    
    result = await controller.generate_core_image(request)
    return result

# 예외 처리는 메인 애플리케이션에서 처리하므로 여기서는 제거