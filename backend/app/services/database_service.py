"""
데이터베이스 서비스 계층
Supabase와의 모든 데이터베이스 상호작용을 담당
Repository 패턴을 구현하여 데이터 접근 로직을 추상화
비즈니스 로직에서 데이터베이스 세부사항을 분리
"""
import requests
from typing import List, Dict, Any, Optional
from fastapi import HTTPException

from app.config.settings import SUPABASE_URL, get_supabase_headers


class DatabaseService:
    """
    데이터베이스 서비스 클래스
    Supabase REST API를 통한 CRUD 작업 제공
    """
    
    def __init__(self):
        self.base_url = SUPABASE_URL
        self.headers = get_supabase_headers()

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        HTTP 요청을 보내고 응답을 처리하는 헬퍼 메서드
        공통 에러 처리와 응답 파싱을 담당
        
        Args:
            method: HTTP 메서드 (GET, POST, PUT, DELETE)
            endpoint: API 엔드포인트
            data: 요청 본문 데이터
            
        Returns:
            API 응답 데이터
            
        Raises:
            HTTPException: 요청 실패 시
        """
        try:
            url = f"{self.base_url}/rest/v1/{endpoint}"
            
            if method.upper() == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            elif method.upper() == 'PATCH':
                response = requests.patch(url, headers=self.headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                raise HTTPException(status_code=400, detail="Unsupported HTTP method")
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # 선생님 관련 데이터베이스 작업
    def get_teacher_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """이메일로 선생님 정보 조회"""
        teachers = self._make_request('GET', f'teachers?email=eq.{email}')
        return teachers[0] if teachers else None

    def create_teacher(self, teacher_data: Dict[str, Any]) -> Dict[str, Any]:
        """선생님 정보 생성"""
        result = self._make_request('POST', 'teachers', teacher_data)
        return result[0] if isinstance(result, list) else result

    def get_teacher_sessions(self, teacher_id: int) -> List[Dict[str, Any]]:
        """선생님의 클래스 세션 목록 조회"""
        return self._make_request('GET', f'class_sessions?teacher_id=eq.{teacher_id}')

    # 클래스 세션 관련 데이터베이스 작업
    def get_session_by_class_code(self, class_code: str) -> Optional[Dict[str, Any]]:
        """클래스 코드로 세션 조회"""
        sessions = self._make_request('GET', f'class_sessions?class_code=eq.{class_code}')
        return sessions[0] if sessions else None

    def create_class_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """클래스 세션 생성"""
        result = self._make_request('POST', 'class_sessions', session_data)
        return result[0] if isinstance(result, list) else result

    def get_session_students(self, session_id: int) -> List[Dict[str, Any]]:
        """세션에 참여한 학생 목록 조회"""
        return self._make_request('GET', f'students?session_id=eq.{session_id}')

    # 학생 관련 데이터베이스 작업
    def get_student_by_name_and_code(self, name: str, class_code: str) -> Optional[Dict[str, Any]]:
        """이름과 클래스 코드로 학생 조회"""
        students = self._make_request('GET', f'students?name=eq.{name}&class_code=eq.{class_code}')
        return students[0] if students else None

    def create_student(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """학생 정보 생성"""
        result = self._make_request('POST', 'students', student_data)
        return result[0] if isinstance(result, list) else result