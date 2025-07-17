"""
Image Generation service
Business logic for image generation operations
"""
import time
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import UploadFile, HTTPException
import io

from app.core.services.stability_service import StabilityService, StabilityServiceError
from app.core.models.image_schemas import get_credits_required
from .models import (
    CoreImageRequest, SD35ImageRequest, UltraImageRequest, SketchRequest,
    ImageGenerationResponse, FileValidationResponse, HealthCheckResponse,
    EducationalImageRequest, QuickImageRequest
)

logger = logging.getLogger(__name__)


class ImageGenerationService:
    """
    이미지 생성 관련 비즈니스 로직을 처리하는 서비스
    Stability AI API 연동을 담당
    """
    
    def __init__(self):
        self.stability_service = StabilityService()
    
    def validate_file_upload(self, file: UploadFile) -> None:
        """
        파일 업로드 검증
        
        Args:
            file: 업로드된 파일
            
        Raises:
            HTTPException: 파일이 유효하지 않을 경우
        """
        # MIME 타입 검증
        allowed_types = ["image/jpeg", "image/png", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"지원되지 않는 파일 형식입니다. 허용된 형식: {', '.join(allowed_types)}"
            )
        
        # 파일 크기 검증 (50MB)
        if hasattr(file, 'size') and file.size > 50 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="파일 크기가 50MB를 초과합니다"
            )
    
    async def validate_image_file(self, file: UploadFile) -> FileValidationResponse:
        """
        이미지 파일 상세 검증
        
        Args:
            file: 업로드된 파일
            
        Returns:
            FileValidationResponse: 검증 결과
        """
        try:
            self.validate_file_upload(file)
            file_content = await file.read()
            
            # 파일 포인터를 처음으로 되돌림
            await file.seek(0)
            
            # Stability 서비스를 통한 상세 검증
            validation_result = self.stability_service.validate_image_file(io.BytesIO(file_content))
            
            return FileValidationResponse(
                valid=validation_result["valid"],
                message=validation_result.get("error", "유효한 이미지 파일입니다"),
                file_info=validation_result.get("info")
            )
            
        except HTTPException as e:
            return FileValidationResponse(
                valid=False,
                message=e.detail
            )
        except Exception as e:
            logger.error(f"파일 검증 중 오류 발생: {str(e)}")
            return FileValidationResponse(
                valid=False,
                message=f"검증 중 오류 발생: {str(e)}"
            )
    
    async def generate_core_image_data(self, request_data: Dict[str, Any]) -> bytes:
        """
        Core 모델로 이미지 생성 (바이너리 데이터 반환)
        
        Args:
            request_data: 요청 데이터
            
        Returns:
            bytes: 생성된 이미지 바이너리 데이터
        """
        try:
            # 요청 데이터 검증
            request = CoreImageRequest(**request_data)
            
            logger.info(f"Core 이미지 생성 시작: {request.prompt[:50]}...")
            
            # Stability AI API 호출
            image_data = self.stability_service.generate_core_image(
                prompt=request.prompt,
                aspect_ratio=request.aspect_ratio,
                output_format=request.output_format,
                style_preset=request.style_preset,
                negative_prompt=request.negative_prompt,
                seed=request.seed
            )
            
            logger.info("Core 이미지 생성 완료")
            
            return image_data
            
        except StabilityServiceError as e:
            logger.error(f"Core 이미지 생성 오류: {str(e)}")
            raise HTTPException(
                status_code=e.status_code or 500,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Core 이미지 생성 중 예상치 못한 오류: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="이미지 생성 중 오류가 발생했습니다"
            )

    async def generate_core_image(self, request: CoreImageRequest) -> ImageGenerationResponse:
        """
        Core 모델로 이미지 생성
        
        Args:
            request: Core 이미지 생성 요청
            
        Returns:
            ImageGenerationResponse: 생성 결과
        """
        try:
            start_time = time.time()
            
            logger.info(f"Core 이미지 생성 시작: {request.prompt[:50]}...")
            
            # Stability AI API 호출
            image_data = self.stability_service.generate_core_image(
                prompt=request.prompt,
                aspect_ratio=request.aspect_ratio,
                output_format=request.output_format,
                style_preset=request.style_preset,
                negative_prompt=request.negative_prompt,
                seed=request.seed
            )
            
            generation_time = time.time() - start_time
            
            # 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"core_image_{timestamp}.{request.output_format}"
            
            # 이미지 정보 조회
            image_info = self.stability_service.get_image_info(image_data)
            
            logger.info(f"Core 이미지 생성 완료: {filename}, 시간: {generation_time:.2f}s")
            
            return ImageGenerationResponse(
                filename=filename,
                file_size=len(image_data),
                generation_time=generation_time,
                credits_used=get_credits_required("core"),
                width=image_info.get("width"),
                height=image_info.get("height"),
                model_used="stable-image-core"
            )
            
        except StabilityServiceError as e:
            logger.error(f"Core 이미지 생성 오류: {str(e)}")
            raise HTTPException(
                status_code=e.status_code or 500,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Core 이미지 생성 중 예상치 못한 오류: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="이미지 생성 중 오류가 발생했습니다"
            )
    
    async def generate_sd35_image(self, request_data: Dict[str, Any], 
                                 image_file: Optional[UploadFile] = None) -> bytes:
        """
        SD3.5 모델로 이미지 생성
        
        Args:
            request_data: 요청 데이터
            image_file: 업로드된 이미지 파일 (image-to-image 모드에서 필요)
            
        Returns:
            bytes: 생성된 이미지 바이너리 데이터
        """
        try:
            # 요청 데이터 검증
            request = SD35ImageRequest(**request_data)
            
            # 파일 검증 및 처리
            image_data = None
            if image_file and request.mode == "image-to-image":
                self.validate_file_upload(image_file)
                image_data = await image_file.read()
            
            logger.info(f"SD3.5 이미지 생성 시작: {request.mode} - {request.prompt[:50]}...")
            
            # Stability AI API 호출
            generated_image = self.stability_service.generate_sd35_image(
                prompt=request.prompt,
                mode=request.mode,
                model=request.model,
                image=image_data,
                strength=request.strength,
                aspect_ratio=request.aspect_ratio,
                output_format=request.output_format,
                style_preset=request.style_preset,
                negative_prompt=request.negative_prompt,
                seed=request.seed,
                cfg_scale=request.cfg_scale
            )
            
            logger.info(f"SD3.5 이미지 생성 완료: {request.mode}")
            
            return generated_image
            
        except StabilityServiceError as e:
            logger.error(f"SD3.5 이미지 생성 오류: {str(e)}")
            raise HTTPException(
                status_code=e.status_code or 500,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"SD3.5 이미지 생성 중 예상치 못한 오류: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="이미지 생성 중 오류가 발생했습니다"
            )
    
    async def generate_ultra_image(self, request_data: Dict[str, Any], 
                                  image_file: Optional[UploadFile] = None) -> bytes:
        """
        Ultra 모델로 이미지 생성
        
        Args:
            request_data: 요청 데이터
            image_file: 업로드된 참조 이미지 파일 (선택사항)
            
        Returns:
            bytes: 생성된 이미지 바이너리 데이터
        """
        try:
            # 요청 데이터 검증
            request = UltraImageRequest(**request_data)
            
            # 파일 검증 및 처리
            image_data = None
            if image_file:
                self.validate_file_upload(image_file)
                image_data = await image_file.read()
            
            logger.info(f"Ultra 이미지 생성 시작: {request.prompt[:50]}...")
            
            # Stability AI API 호출
            generated_image = self.stability_service.generate_ultra_image(
                prompt=request.prompt,
                aspect_ratio=request.aspect_ratio,
                output_format=request.output_format,
                image=image_data,
                strength=request.strength,
                style_preset=request.style_preset,
                negative_prompt=request.negative_prompt,
                seed=request.seed
            )
            
            logger.info("Ultra 이미지 생성 완료")
            
            return generated_image
            
        except StabilityServiceError as e:
            logger.error(f"Ultra 이미지 생성 오류: {str(e)}")
            raise HTTPException(
                status_code=e.status_code or 500,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Ultra 이미지 생성 중 예상치 못한 오류: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="이미지 생성 중 오류가 발생했습니다"
            )
    
    async def sketch_to_image(self, request_data: Dict[str, Any], 
                             image_file: UploadFile) -> bytes:
        """
        스케치를 이미지로 변환
        
        Args:
            request_data: 요청 데이터
            image_file: 업로드된 스케치 이미지 파일
            
        Returns:
            bytes: 생성된 이미지 바이너리 데이터
        """
        try:
            # 요청 데이터 검증
            request = SketchRequest(**request_data)
            
            # 파일 검증 및 처리
            self.validate_file_upload(image_file)
            image_data = await image_file.read()
            
            logger.info(f"스케치→이미지 변환 시작: {request.prompt[:50]}...")
            
            # Stability AI API 호출
            generated_image = self.stability_service.sketch_to_image(
                prompt=request.prompt,
                image=image_data,
                control_strength=request.control_strength,
                output_format=request.output_format,
                style_preset=request.style_preset,
                negative_prompt=request.negative_prompt,
                seed=request.seed
            )
            
            logger.info("스케치→이미지 변환 완료")
            
            return generated_image
            
        except StabilityServiceError as e:
            logger.error(f"스케치→이미지 변환 오류: {str(e)}")
            raise HTTPException(
                status_code=e.status_code or 500,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"스케치→이미지 변환 중 예상치 못한 오류: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="이미지 변환 중 오류가 발생했습니다"
            )
    
    def get_constants(self) -> Dict[str, Any]:
        """
        프론트엔드에서 사용할 상수들 반환
        
        Returns:
            Dict[str, Any]: 상수 딕셔너리
        """
        from app.core.models.image_schemas import get_constants_for_frontend
        return get_constants_for_frontend()
    
    def get_educational_prompts(self, subject: Optional[str] = None) -> Dict[str, Any]:
        """
        교육용 프롬프트 예시 반환
        
        Args:
            subject: 교육 주제 (선택사항)
            
        Returns:
            Dict[str, Any]: 교육용 프롬프트 예시
        """
        # 현재는 빈 응답 반환 (향후 확장 가능)
        return {
            "all_subjects": {}
        }
    
    async def check_api_health(self) -> Dict[str, Any]:
        """
        Stability AI API 상태 확인
        
        Returns:
            Dict[str, Any]: API 상태 정보
        """
        try:
            # 간단한 API 테스트 (실제로는 헬스체크 엔드포인트 호출)
            # 여기서는 서비스 초기화가 가능한지 확인
            test_service = StabilityService()
            api_available = bool(test_service.api_key)
            
            return {
                "status": "healthy" if api_available else "unhealthy",
                "api_available": api_available,
                "timestamp": datetime.now().isoformat(),
                "service": "stability-ai"
            }
            
        except Exception as e:
            logger.error(f"API 헬스체크 중 오류: {str(e)}")
            return {
                "status": "unhealthy",
                "api_available": False,
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def get_model_info(self, model_type: str) -> Dict[str, Any]:
        """
        모델 정보 반환
        
        Args:
            model_type: 모델 타입
            
        Returns:
            Dict[str, Any]: 모델 정보
        """
        model_info = {
            "core": {
                "name": "Stable Image Core",
                "description": "기본 텍스트→이미지 생성 모델",
                "credits_required": 3,
                "supported_modes": ["text-to-image"],
                "max_resolution": "1024x1024"
            },
            "sd35": {
                "name": "Stable Diffusion 3.5",
                "description": "고급 이미지 생성 모델 (텍스트/이미지→이미지)",
                "credits_required": 4,
                "supported_modes": ["text-to-image", "image-to-image"],
                "max_resolution": "1536x1536"
            },
            "ultra": {
                "name": "Stable Image Ultra",
                "description": "최고급 이미지 생성 모델",
                "credits_required": 8,
                "supported_modes": ["text-to-image", "reference-image"],
                "max_resolution": "2048x2048"
            },
            "sketch": {
                "name": "Sketch Control",
                "description": "스케치→이미지 변환 모델",
                "credits_required": 3,
                "supported_modes": ["sketch-to-image"],
                "max_resolution": "1024x1024"
            }
        }
        
        return model_info.get(model_type, {
            "error": f"지원되지 않는 모델 타입: {model_type}"
        })

    async def generate_educational_image(self, request: EducationalImageRequest) -> ImageGenerationResponse:
        """
        교육용 이미지 생성
        
        Args:
            request: 교육용 이미지 생성 요청
            
        Returns:
            ImageGenerationResponse: 생성 결과
        """
        # 교육용 프롬프트 보강
        educational_prompt = f"Educational illustration for {request.subject}"
        if request.grade_level:
            educational_prompt += f" suitable for grade {request.grade_level}"
        educational_prompt += f": {request.prompt}"
        educational_prompt += ", clear and simple, educational style, colorful, engaging"
        
        # Core 모델 요청으로 변환
        core_request = CoreImageRequest(
            prompt=educational_prompt,
            aspect_ratio=request.aspect_ratio,
            output_format=request.output_format,
            style_preset=request.style,
            negative_prompt="complex, confusing, inappropriate, violent, dark"
        )
        
        return await self.generate_core_image(core_request)

    async def generate_quick_image(self, request: QuickImageRequest) -> ImageGenerationResponse:
        """
        빠른 이미지 생성
        
        Args:
            request: 빠른 이미지 생성 요청
            
        Returns:
            ImageGenerationResponse: 생성 결과
        """
        # 기본 설정으로 Core 이미지 생성
        core_request = CoreImageRequest(
            prompt=request.prompt,
            style_preset=request.style,
            aspect_ratio="1:1",
            output_format="png"
        )
        
        return await self.generate_core_image(core_request)