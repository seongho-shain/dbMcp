"""
보안 관련 유틸리티 함수들
비밀번호 해싱, 토큰 생성 등 보안 관련 기능 제공
단일 책임 원칙에 따라 보안 로직을 분리
"""
import hashlib
import random
import string
from app.config.settings import CLASS_CODE_LENGTH


def hash_password(password: str) -> str:
    """
    비밀번호를 SHA-256으로 해싱
    보안을 위해 원본 비밀번호를 암호화하여 저장
    
    Args:
        password: 원본 비밀번호
        
    Returns:
        해싱된 비밀번호 문자열
    """
    return hashlib.sha256(password.encode()).hexdigest()


def generate_class_code() -> str:
    """
    클래스 코드 생성 (6자리 대문자 + 숫자)
    학생들이 클래스에 참여할 때 사용하는 고유 코드 생성
    중복 가능성을 최소화하기 위해 랜덤 생성
    
    Returns:
        6자리 클래스 코드 (예: "A1B2C3")
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=CLASS_CODE_LENGTH))