"""
Stability AI 이미지 생성 서비스
Reference 폴더의 예시 코드를 기반으로 교육 시스템에 맞게 최적화된 서비스 클래스
"""
import os
import requests
import io
from typing import Optional, Dict, Any, BinaryIO
from PIL import Image
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class StabilityServiceError(Exception):
    """Stability AI 서비스 관련 예외"""
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class StabilityService:
    """Stability AI 이미지 생성 서비스"""
    
    BASE_URL = "https://api.stability.ai"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: Stability AI API 키 (None일 경우 환경변수에서 가져옴)
        """
        self.api_key = api_key or os.getenv("STABILITY_API_KEY")
        if not self.api_key:
            raise StabilityServiceError("STABILITY_API_KEY가 설정되지 않았습니다.")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json"
        }
    
    def _get_enum_value(self, value: Any) -> Any:
        """Enum 멤버인 경우 .value를, 그렇지 않으면 원래 값을 반환"""
        return value.value if isinstance(value, Enum) else value

    def _make_request(self, endpoint: str, method: str = "POST", data: Optional[Dict] = None, 
                     files: Optional[Dict] = None) -> requests.Response:
        """API 요청을 보내고 응답을 처리"""
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            if method == "POST":
                response = requests.post(url, headers=self.headers, json=data, files=files, timeout=60)
            else:
                response = requests.get(url, headers=self.headers, timeout=60)
            
            if response.status_code != 200:
                error_data = None
                try:
                    error_data = response.json()
                except:
                    pass
                
                raise StabilityServiceError(
                    f"API 요청 실패: {response.status_code} - {response.text}",
                    status_code=response.status_code,
                    response_data=error_data
                )
            
            return response
            
        except requests.exceptions.RequestException as e:
            raise StabilityServiceError(f"네트워크 오류: {str(e)}")
    
    def generate_core_image(self, prompt: str, aspect_ratio: str = "1:1", 
                          output_format: str = "png", style_preset: Optional[str] = None,
                          negative_prompt: Optional[str] = None, seed: Optional[int] = None) -> bytes:
        """
        Stable Image Core로 이미지 생성
        """
        data = {
            "prompt": prompt,
            "aspect_ratio": self._get_enum_value(aspect_ratio),
            "output_format": self._get_enum_value(output_format)
        }
        
        if style_preset:
            data["style_preset"] = self._get_enum_value(style_preset)
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        if seed is not None:
            data["seed"] = str(seed)
        
        files = {"none": ""}
        
        logger.info(f"Core 이미지 생성 요청: {prompt[:50]}...")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*"
        }
        
        try:
            url = f"{self.BASE_URL}/v2beta/stable-image/generate/core"
            response = requests.post(url, headers=headers, data=data, files=files, timeout=60)
            
            if response.status_code != 200:
                error_data = None
                try:
                    error_data = response.json()
                except:
                    pass
                
                raise StabilityServiceError(
                    f"Core API 요청 실패: {response.status_code} - {response.text}",
                    status_code=response.status_code,
                    response_data=error_data
                )
            
            if response.headers.get('content-type', '').startswith('image/'):
                return response.content
            else:
                try:
                    json_data = response.json()
                    if 'artifacts' in json_data and len(json_data['artifacts']) > 0:
                        import base64
                        return base64.b64decode(json_data['artifacts'][0]['base64'])
                    else:
                        raise StabilityServiceError("이미지 데이터를 찾을 수 없습니다.")
                except Exception as e:
                    raise StabilityServiceError(f"응답 처리 오류: {str(e)}")
                    
        except requests.exceptions.RequestException as e:
            raise StabilityServiceError(f"네트워크 오류: {str(e)}")
    
    def generate_sd35_image(self, prompt: str, mode: str = "text-to-image",
                           model: str = "sd3.5-large", image: Optional[bytes] = None,
                           strength: Optional[float] = None, aspect_ratio: Optional[str] = "1:1",
                           output_format: str = "png", style_preset: Optional[str] = None,
                           negative_prompt: Optional[str] = None, seed: Optional[int] = None,
                           cfg_scale: Optional[float] = None) -> bytes:
        """
        Stable Diffusion 3.5로 이미지 생성
        """
        mode_value = self._get_enum_value(mode)
        model_value = self._get_enum_value(model)

        files = {}
        data = {
            "prompt": prompt,
            "mode": mode_value,
            "model": model_value,
            "output_format": self._get_enum_value(output_format)
        }
        
        if mode_value == "text-to-image" and aspect_ratio:
            data["aspect_ratio"] = self._get_enum_value(aspect_ratio)
        
        if mode_value == "image-to-image":
            if image is None:
                raise StabilityServiceError("image-to-image 모드에서는 이미지가 필요합니다.")
            if strength is None:
                raise StabilityServiceError("image-to-image 모드에서는 strength가 필요합니다.")
            
            files["image"] = ("image.png", io.BytesIO(image), "image/png")
            data["strength"] = strength
        
        if style_preset:
            data["style_preset"] = self._get_enum_value(style_preset)
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        if seed is not None:
            data["seed"] = str(seed)
        if cfg_scale is not None:
            data["cfg_scale"] = str(cfg_scale)
        
        logger.info(f"SD3.5 이미지 생성 요청: {mode_value} - {prompt[:50]}...")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*"
        }
        
        try:
            url = f"{self.BASE_URL}/v2beta/stable-image/generate/sd3"
            
            # SD3.5 API는 모든 모드에서 multipart/form-data를 요구
            # text-to-image 모드에서는 빈 files 딕셔너리를 전달
            if mode_value == "text-to-image":
                files["none"] = ""  # 문서 예시에 따른 빈 files 항목
            
            response = requests.post(url, headers=headers, data=data, files=files, timeout=60)
            
            if response.status_code != 200:
                error_data = None
                try:
                    error_data = response.json()
                except:
                    pass
                
                raise StabilityServiceError(
                    f"SD3.5 API 요청 실패: {response.status_code} - {response.text}",
                    status_code=response.status_code,
                    response_data=error_data
                )
            
            if response.headers.get('content-type', '').startswith('image/'):
                return response.content
            else:
                try:
                    json_data = response.json()
                    if 'artifacts' in json_data and len(json_data['artifacts']) > 0:
                        import base64
                        return base64.b64decode(json_data['artifacts'][0]['base64'])
                    else:
                        raise StabilityServiceError("이미지 데이터를 찾을 수 없습니다.")
                except Exception as e:
                    raise StabilityServiceError(f"응답 처리 오류: {str(e)}")
                    
        except requests.exceptions.RequestException as e:
            raise StabilityServiceError(f"네트워크 오류: {str(e)}")
    
    def generate_ultra_image(self, prompt: str, aspect_ratio: str = "1:1",
                           output_format: str = "png", image: Optional[bytes] = None,
                           strength: Optional[float] = None, style_preset: Optional[str] = None,
                           negative_prompt: Optional[str] = None, seed: Optional[int] = None) -> bytes:
        """
        Stable Image Ultra로 이미지 생성
        """
        files = {}
        data = {
            "prompt": prompt,
            "aspect_ratio": self._get_enum_value(aspect_ratio),
            "output_format": self._get_enum_value(output_format)
        }
        
        if image:
            files["image"] = ("image.png", io.BytesIO(image), "image/png")
            if strength is not None:
                data["strength"] = strength
        
        if style_preset:
            data["style_preset"] = self._get_enum_value(style_preset)
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        if seed is not None:
            data["seed"] = str(seed)
        
        logger.info(f"Ultra 이미지 생성 요청: {prompt[:50]}...")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*"
        }
        
        try:
            url = f"{self.BASE_URL}/v2beta/stable-image/generate/ultra"
            response = requests.post(url, headers=headers, data=data, files=files, timeout=60)
            
            if response.status_code != 200:
                error_data = None
                try:
                    error_data = response.json()
                except:
                    pass
                
                raise StabilityServiceError(
                    f"Ultra API 요청 실패: {response.status_code} - {response.text}",
                    status_code=response.status_code,
                    response_data=error_data
                )
            
            if response.headers.get('content-type', '').startswith('image/'):
                return response.content
            else:
                try:
                    json_data = response.json()
                    if 'artifacts' in json_data and len(json_data['artifacts']) > 0:
                        import base64
                        return base64.b64decode(json_data['artifacts'][0]['base64'])
                    else:
                        raise StabilityServiceError("이미지 데이터를 찾을 수 없습니다.")
                except Exception as e:
                    raise StabilityServiceError(f"응답 처리 오류: {str(e)}")
                    
        except requests.exceptions.RequestException as e:
            raise StabilityServiceError(f"네트워크 오류: {str(e)}")
    
    def sketch_to_image(self, prompt: str, image: bytes, control_strength: float = 0.7,
                       output_format: str = "png", style_preset: Optional[str] = None,
                       negative_prompt: Optional[str] = None, seed: Optional[int] = None) -> bytes:
        """
        스케치를 이미지로 변환
        """
        files = {
            "image": ("sketch.png", io.BytesIO(image), "image/png")
        }
        
        data = {
            "prompt": prompt,
            "control_strength": control_strength,
            "output_format": self._get_enum_value(output_format)
        }
        
        if style_preset:
            data["style_preset"] = self._get_enum_value(style_preset)
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        if seed is not None:
            data["seed"] = str(seed)
        
        logger.info(f"스케치→이미지 변환 요청: {prompt[:50]}...")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*"
        }
        
        try:
            url = f"{self.BASE_URL}/v2beta/stable-image/control/sketch"
            response = requests.post(url, headers=headers, data=data, files=files, timeout=60)
            
            if response.status_code != 200:
                error_data = None
                try:
                    error_data = response.json()
                except:
                    pass
                
                raise StabilityServiceError(
                    f"Sketch API 요청 실패: {response.status_code} - {response.text}",
                    status_code=response.status_code,
                    response_data=error_data
                )
            
            if response.headers.get('content-type', '').startswith('image/'):
                return response.content
            else:
                try:
                    json_data = response.json()
                    if 'artifacts' in json_data and len(json_data['artifacts']) > 0:
                        import base64
                        return base64.b64decode(json_data['artifacts'][0]['base64'])
                    else:
                        raise StabilityServiceError("이미지 데이터를 찾을 수 없습니다.")
                except Exception as e:
                    raise StabilityServiceError(f"응답 처리 오류: {str(e)}")
                    
        except requests.exceptions.RequestException as e:
            raise StabilityServiceError(f"네트워크 오류: {str(e)}")
    
    def validate_image_file(self, image_file: BinaryIO) -> Dict[str, Any]:
        """
        이미지 파일 검증
        """
        try:
            image = Image.open(image_file)
            
            width, height = image.size
            format_name = image.format
            mode = image.mode
            
            image_file.seek(0, 2)
            file_size = image_file.tell()
            image_file.seek(0)
            
            max_size = 50 * 1024 * 1024
            min_resolution = 64
            max_pixels = 9437184
            
            errors = []
            
            if file_size > max_size:
                errors.append(f"파일 크기가 {max_size // (1024*1024)}MB를 초과합니다.")
            
            if width < min_resolution or height < min_resolution:
                errors.append(f"이미지 해상도가 {min_resolution}x{min_resolution}보다 작습니다.")
            
            if width * height > max_pixels:
                errors.append(f"이미지 픽셀 수가 {max_pixels}를 초과합니다.")
            
            aspect_ratio = width / height
            if aspect_ratio < 0.4 or aspect_ratio > 2.5:
                errors.append("이미지 종횡비가 지원 범위(1:2.5 ~ 2.5:1)를 벗어납니다.")
            
            supported_formats = ['JPEG', 'PNG', 'WEBP']
            if format_name not in supported_formats:
                errors.append(f"지원되지 않는 이미지 형식입니다. 지원 형식: {', '.join(supported_formats)}")
            
            return {
                "valid": len(errors) == 0,
                "error": "; ".join(errors) if errors else None,
                "info": {
                    "width": width,
                    "height": height,
                    "format": format_name,
                    "mode": mode,
                    "file_size": file_size,
                    "aspect_ratio": round(aspect_ratio, 2)
                }
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"이미지 파일 처리 오류: {str(e)}",
                "info": None
            }
    
    def get_image_info(self, image_data: bytes) -> Dict[str, Any]:
        """
        이미지 바이너리 데이터의 정보 조회
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            return {
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode,
                "size": len(image_data)
            }
        except Exception as e:
            return {"error": str(e)}