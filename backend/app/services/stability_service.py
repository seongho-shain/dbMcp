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
import re

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
    
    @staticmethod
    def normalize_enum_value(value: str) -> str:
        """
        Enum 값을 정규화하여 API에 맞는 형식으로 변환
        
        Examples:
            'generationmode.image_to_image' -> 'image-to-image'
            'SD35Model.LARGE' -> 'sd3.5-large'
            'OutputFormat.PNG' -> 'png'
            'StylePreset.PHOTOGRAPHIC' -> 'photographic'
        """
        if not isinstance(value, str):
            return str(value)
        
        # 이미 정규화된 일반적인 값들은 그대로 반환 (더 구체적인 검사)
        if ('.' not in value and not value.isupper() and 
            not value.startswith('sd3.') and  # sd3.5-large 같은 값 제외
            ':' not in value):  # 16:9 같은 aspect ratio 제외
            return value
        
        # 이미 정규화된 특수 값들 체크
        if value in ['sd3.5-large', 'sd3.5-large-turbo', 'sd3.5-medium', 
                    'text-to-image', 'image-to-image', 'digital-art', 
                    '3d-model', 'pixel-art', 'fantasy-art']:
            return value
        
        # 종횡비 값들은 그대로 반환
        if ':' in value and value.replace(':', '').replace('.', '').isdigit():
            return value
        
        # Enum 클래스명.값 형태를 처리
        if '.' in value:
            # 클래스명과 값을 분리
            parts = value.split('.')
            if len(parts) == 2:
                class_name, enum_value = parts
                
                # SD35Model 처리
                if class_name.lower() == 'sd35model':
                    if enum_value.upper() == 'LARGE':
                        return 'sd3.5-large'
                    elif enum_value.upper() == 'LARGE_TURBO':
                        return 'sd3.5-large-turbo'
                    elif enum_value.upper() == 'MEDIUM':
                        return 'sd3.5-medium'
                
                # GenerationMode 처리
                elif class_name.lower() == 'generationmode':
                    if enum_value.upper() == 'TEXT_TO_IMAGE':
                        return 'text-to-image'
                    elif enum_value.upper() == 'IMAGE_TO_IMAGE':
                        return 'image-to-image'
                
                # OutputFormat 처리
                elif class_name.lower() == 'outputformat':
                    return enum_value.lower()
                
                # StylePreset 처리
                elif class_name.lower() == 'stylepreset':
                    if enum_value.upper() == 'NONE':
                        return ''
                    elif enum_value.upper() == 'MODEL_3D':
                        return '3d-model'
                    elif enum_value.upper() == 'DIGITAL_ART':
                        return 'digital-art'
                    elif enum_value.upper() == 'PIXEL_ART':
                        return 'pixel-art'
                    elif enum_value.upper() == 'FANTASY_ART':
                        return 'fantasy-art'
                    else:
                        return enum_value.lower().replace('_', '-')
                
                # AspectRatio 처리
                elif class_name.lower() == 'aspectratio':
                    # LANDSCAPE_16_9 -> 16:9
                    if '_' in enum_value:
                        ratio_part = enum_value.split('_')[-2:]
                        if len(ratio_part) == 2:
                            return f"{ratio_part[0]}:{ratio_part[1]}"
                    elif enum_value.upper() == 'SQUARE':
                        return '1:1'
                    elif enum_value.upper() == 'ULTRA_WIDE':
                        return '21:9'
                    elif enum_value.upper() == 'ULTRA_PORTRAIT':
                        return '9:21'
                    
                # 기본적으로 소문자로 변환하고 언더스코어를 하이픈으로 변경
                return enum_value.lower().replace('_', '-')
        
        # 대문자로만 된 값들 처리 (예: 'LARGE' -> 'sd3.5-large')
        if value.isupper():
            if value == 'LARGE':
                return 'sd3.5-large'
            elif value == 'LARGE_TURBO':
                return 'sd3.5-large-turbo'
            elif value == 'MEDIUM':
                return 'sd3.5-medium'
            elif value == 'TEXT_TO_IMAGE':
                return 'text-to-image'
            elif value == 'IMAGE_TO_IMAGE':
                return 'image-to-image'
            else:
                return value.lower().replace('_', '-')
        
        return value
    
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
        
        Args:
            prompt: 이미지 생성 프롬프트
            aspect_ratio: 이미지 비율 (1:1, 16:9, 9:16, 3:2, 2:3, 4:3, 3:4)
            output_format: 출력 형식 (png, jpeg, webp)
            style_preset: 스타일 프리셋
            negative_prompt: 네거티브 프롬프트
            seed: 시드 값
        
        Returns:
            생성된 이미지 바이너리 데이터
        """
        # Core API는 multipart/form-data 형식을 사용해야 함
        # Enum 값을 실제 문자열로 변환
        data = {
            "prompt": prompt,
            "aspect_ratio": self.normalize_enum_value(aspect_ratio.value if hasattr(aspect_ratio, 'value') else aspect_ratio),
            "output_format": self.normalize_enum_value(output_format.value if hasattr(output_format, 'value') else output_format)
        }
        
        if style_preset:
            data["style_preset"] = self.normalize_enum_value(style_preset.value if hasattr(style_preset, 'value') else style_preset)
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        if seed is not None:
            data["seed"] = str(seed)
        
        # 빈 파일 추가 (API 문서 예시에 따라)
        files = {"none": ""}
        
        logger.info(f"Core 이미지 생성 요청: {prompt[:50]}...")
        
        # multipart/form-data 요청을 위해 headers 수정
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
            
            # 응답이 이미지인지 확인
            if response.headers.get('content-type', '').startswith('image/'):
                return response.content
            else:
                # JSON 응답인 경우 base64 디코딩 등 처리
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
        
        Args:
            prompt: 이미지 생성 프롬프트
            mode: 생성 모드 (text-to-image, image-to-image)
            model: 사용할 모델 (sd3.5-large, sd3.5-large-turbo, sd3.5-medium)
            image: 입력 이미지 (image-to-image 모드에서 필요)
            strength: 변형 강도 (0.0-1.0)
            aspect_ratio: 이미지 비율 (text-to-image 모드에서만)
            output_format: 출력 형식
            style_preset: 스타일 프리셋
            negative_prompt: 네거티브 프롬프트
            seed: 시드 값
        
        Returns:
            생성된 이미지 바이너리 데이터
        """
        files = {}
        data = {
            "prompt": prompt,
            "mode": self.normalize_enum_value(mode),
            "model": self.normalize_enum_value(model),
            "output_format": self.normalize_enum_value(output_format.value if hasattr(output_format, 'value') else output_format)
        }
        
        # text-to-image 모드에서만 aspect_ratio 허용
        if self.normalize_enum_value(mode) == "text-to-image" and aspect_ratio:
            data["aspect_ratio"] = self.normalize_enum_value(aspect_ratio.value if hasattr(aspect_ratio, 'value') else aspect_ratio)
        
        # image-to-image 모드 처리
        if self.normalize_enum_value(mode) == "image-to-image":
            if image is None:
                raise StabilityServiceError("image-to-image 모드에서는 이미지가 필요합니다.")
            if strength is None:
                raise StabilityServiceError("image-to-image 모드에서는 strength가 필요합니다.")
            
            files["image"] = ("image.png", io.BytesIO(image), "image/png")
            data["strength"] = strength
        
        if style_preset:
            data["style_preset"] = self.normalize_enum_value(style_preset.value if hasattr(style_preset, 'value') else style_preset)
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        if seed is not None:
            data["seed"] = str(seed)
        if cfg_scale is not None:
            data["cfg_scale"] = str(cfg_scale)
        
        logger.info(f"SD3.5 이미지 생성 요청: {mode} - {prompt[:50]}...")
        
        # multipart/form-data 요청을 위해 headers 수정
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*"  # 이미지 바이너리로 직접 받기
        }
        
        try:
            url = f"{self.BASE_URL}/v2beta/stable-image/generate/sd3"
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
            
            # 응답이 이미지인지 확인
            if response.headers.get('content-type', '').startswith('image/'):
                return response.content
            else:
                # JSON 응답인 경우 처리
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
        
        Args:
            prompt: 이미지 생성 프롬프트
            aspect_ratio: 이미지 비율
            output_format: 출력 형식
            image: 참조 이미지 (선택사항)
            strength: 참조 이미지 영향도
            style_preset: 스타일 프리셋
            negative_prompt: 네거티브 프롬프트
            seed: 시드 값
        
        Returns:
            생성된 이미지 바이너리 데이터
        """
        files = {}
        data = {
            "prompt": prompt,
            "aspect_ratio": self.normalize_enum_value(aspect_ratio.value if hasattr(aspect_ratio, 'value') else aspect_ratio),
            "output_format": self.normalize_enum_value(output_format.value if hasattr(output_format, 'value') else output_format)
        }
        
        if image:
            files["image"] = ("image.png", io.BytesIO(image), "image/png")
            if strength is not None:
                data["strength"] = strength
        
        if style_preset:
            data["style_preset"] = self.normalize_enum_value(style_preset.value if hasattr(style_preset, 'value') else style_preset)
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        if seed is not None:
            data["seed"] = str(seed)
        
        logger.info(f"Ultra 이미지 생성 요청: {prompt[:50]}...")
        
        # multipart/form-data 요청을 위해 headers 수정
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*"  # 이미지 바이너리로 직접 받기
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
            
            # 응답이 이미지인지 확인
            if response.headers.get('content-type', '').startswith('image/'):
                return response.content
            else:
                # JSON 응답인 경우 처리
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
        
        Args:
            prompt: 이미지 생성 프롬프트
            image: 스케치 이미지
            control_strength: 제어 강도 (0.0-1.0)
            output_format: 출력 형식
            style_preset: 스타일 프리셋
            negative_prompt: 네거티브 프롬프트
            seed: 시드 값
        
        Returns:
            생성된 이미지 바이너리 데이터
        """
        files = {
            "image": ("sketch.png", io.BytesIO(image), "image/png")
        }
        
        data = {
            "prompt": prompt,
            "control_strength": control_strength,
            "output_format": self.normalize_enum_value(output_format.value if hasattr(output_format, 'value') else output_format)
        }
        
        if style_preset:
            data["style_preset"] = self.normalize_enum_value(style_preset.value if hasattr(style_preset, 'value') else style_preset)
        if negative_prompt:
            data["negative_prompt"] = negative_prompt
        if seed is not None:
            data["seed"] = str(seed)
        
        logger.info(f"스케치→이미지 변환 요청: {prompt[:50]}...")
        
        # multipart/form-data 요청을 위해 headers 수정
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "image/*"  # 이미지 바이너리로 직접 받기
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
            
            # 응답이 이미지인지 확인
            if response.headers.get('content-type', '').startswith('image/'):
                return response.content
            else:
                # JSON 응답인 경우 처리
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
        
        Args:
            image_file: 이미지 파일 스트림
        
        Returns:
            검증 결과 딕셔너리
        """
        try:
            # PIL로 이미지 열기
            image = Image.open(image_file)
            
            # 기본 정보 수집
            width, height = image.size
            format_name = image.format
            mode = image.mode
            
            # 파일 크기 확인 (50MB 제한)
            image_file.seek(0, 2)  # 파일 끝으로 이동
            file_size = image_file.tell()
            image_file.seek(0)  # 파일 처음으로 이동
            
            # 검증 규칙
            max_size = 50 * 1024 * 1024  # 50MB
            min_resolution = 64
            max_pixels = 9437184  # 약 3072x3072
            
            errors = []
            
            if file_size > max_size:
                errors.append(f"파일 크기가 {max_size // (1024*1024)}MB를 초과합니다.")
            
            if width < min_resolution or height < min_resolution:
                errors.append(f"이미지 해상도가 {min_resolution}x{min_resolution}보다 작습니다.")
            
            if width * height > max_pixels:
                errors.append(f"이미지 픽셀 수가 {max_pixels}를 초과합니다.")
            
            # 종횡비 확인 (1:2.5 ~ 2.5:1)
            aspect_ratio = width / height
            if aspect_ratio < 0.4 or aspect_ratio > 2.5:
                errors.append("이미지 종횡비가 지원 범위(1:2.5 ~ 2.5:1)를 벗어납니다.")
            
            # 지원 형식 확인
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
        
        Args:
            image_data: 이미지 바이너리 데이터
        
        Returns:
            이미지 정보 딕셔너리
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