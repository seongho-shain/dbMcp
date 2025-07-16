"""
애플리케이션 설정 관리
환경 변수 및 설정값들을 중앙에서 관리하여 유지보수성을 높임
MVC 패턴에서 설정 정보를 분리하여 관리
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Supabase 설정
SUPABASE_URL = "https://etpqutdudxszedkkrjam.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV0cHF1dGR1ZHhzemVka2tyamFtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI2NDE2OTQsImV4cCI6MjA2ODIxNzY5NH0.Nu9_ZKlGVX1Sub9A4AHbgyzAL3Pctn8_ClrtjkLjnT8"

# CORS 설정
CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

# 서버 설정
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8000

# 세션 설정
SESSION_EXPIRE_HOURS = 24  # 클래스 세션 만료 시간 (24시간)

# 클래스 코드 설정
CLASS_CODE_LENGTH = 6  # 클래스 코드 길이

# OpenAI API 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"  # 사용할 모델 (최신 모델)

def get_supabase_headers() -> Dict[str, Any]:
    """
    Supabase API 요청용 헤더 반환
    API 키와 인증 토큰을 포함한 표준 헤더 생성
    """
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }