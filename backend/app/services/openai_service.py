"""
OpenAI API 서비스
OpenAI GPT 모델을 활용한 AI 응답 생성 서비스
채팅 메시지를 받아서 AI 응답을 생성하고 반환
"""
import os
import asyncio
from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion

from app.config.settings import OPENAI_API_KEY, OPENAI_MODEL


class OpenAIService:
    """
    OpenAI API를 활용한 AI 응답 생성 서비스
    GPT 모델을 통해 자연스러운 대화형 응답 제공
    동기 및 비동기 모드 지원
    """
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY가 설정되지 않았습니다.")
        
        # OpenAI 클라이언트 초기화 (동기 및 비동기)
        self.client = OpenAI(
            api_key=OPENAI_API_KEY,
            timeout=30.0  # 타임아웃 설정
        )
        self.async_client = AsyncOpenAI(
            api_key=OPENAI_API_KEY,
            timeout=30.0
        )
        self.model = OPENAI_MODEL or "gpt-4o"
    
    def generate_response(self, messages: List[Dict[str, str]], user_context: Optional[Dict[str, Any]] = None) -> str:
        """
        사용자 메시지에 대한 AI 응답 생성 (동기 방식)
        
        Args:
            messages: 대화 히스토리 (role: user/assistant, content: 메시지)
            user_context: 사용자 정보 (이름, 역할 등)
            
        Returns:
            AI 생성 응답 텍스트
            
        Raises:
            HTTPException: OpenAI API 호출 실패 시
        """
        try:
            # API 키 확인
            if not OPENAI_API_KEY:
                print("❌ OpenAI API 키가 설정되지 않았습니다.")
                raise HTTPException(status_code=500, detail="OpenAI API 키가 설정되지 않았습니다.")
            
            print(f"🔑 OpenAI API 키: {OPENAI_API_KEY[:10]}...")
            print(f"🤖 사용 모델: {self.model}")
            
            # 시스템 메시지 설정 (AI의 역할과 맥락 정의)
            system_message = self._create_system_message(user_context)
            
            # 전체 대화 컨텍스트 구성
            full_messages = [system_message] + messages
            
            print(f"📝 전송할 메시지 개수: {len(full_messages)}")
            for i, msg in enumerate(full_messages):
                print(f"  {i+1}. {msg['role']}: {msg['content'][:50]}...")
            
            # OpenAI API 호출 (최신 패턴 적용)
            print("🚀 OpenAI API 호출 시작...")
            completion: ChatCompletion = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                max_tokens=500,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1,
                stream=False  # 스트리밍 비활성화
            )
            
            print("✅ OpenAI API 호출 성공!")
            
            # 안전한 응답 추출
            if completion.choices and completion.choices[0].message.content:
                response = completion.choices[0].message.content.strip()
                print(f"📤 AI 응답: {response[:100]}...")
                return response
            else:
                print("❌ AI 응답이 비어있습니다.")
                raise HTTPException(status_code=500, detail="AI 응답이 비어있습니다.")
            
        except Exception as e:
            print(f"❌ OpenAI API 오류: {str(e)}")
            print(f"❌ 오류 타입: {type(e).__name__}")
            
            # 구체적인 오류 처리
            if "rate_limit" in str(e).lower():
                raise HTTPException(status_code=429, detail="API 사용량 한도 초과")
            elif "timeout" in str(e).lower():
                raise HTTPException(status_code=504, detail="API 응답 시간 초과")
            elif "invalid_api_key" in str(e).lower():
                raise HTTPException(status_code=401, detail="유효하지 않은 API 키")
            else:
                raise HTTPException(status_code=500, detail=f"AI 응답 생성 실패: {str(e)}")
    
    async def generate_response_async(self, messages: List[Dict[str, str]], user_context: Optional[Dict[str, Any]] = None) -> str:
        """
        사용자 메시지에 대한 AI 응답 생성 (비동기 방식)
        
        Args:
            messages: 대화 히스토리 (role: user/assistant, content: 메시지)
            user_context: 사용자 정보 (이름, 역할 등)
            
        Returns:
            AI 생성 응답 텍스트
            
        Raises:
            HTTPException: OpenAI API 호출 실패 시
        """
        try:
            # 시스템 메시지 설정
            system_message = self._create_system_message(user_context)
            
            # 전체 대화 컨텍스트 구성
            full_messages = [system_message] + messages
            
            # 비동기 OpenAI API 호출
            async with self.async_client:
                completion: ChatCompletion = await self.async_client.chat.completions.create(
                    model=self.model,
                    messages=full_messages,
                    max_tokens=500,
                    temperature=0.7,
                    presence_penalty=0.1,
                    frequency_penalty=0.1,
                    stream=False
                )
            
            # 안전한 응답 추출
            if completion.choices and completion.choices[0].message.content:
                return completion.choices[0].message.content.strip()
            else:
                raise HTTPException(status_code=500, detail="AI 응답이 비어있습니다.")
            
        except Exception as e:
            # 구체적인 오류 처리
            if "rate_limit" in str(e).lower():
                raise HTTPException(status_code=429, detail="API 사용량 한도 초과")
            elif "timeout" in str(e).lower():
                raise HTTPException(status_code=504, detail="API 응답 시간 초과")
            else:
                raise HTTPException(status_code=500, detail=f"AI 응답 생성 실패: {str(e)}")
    
    def generate_response_stream(self, messages: List[Dict[str, str]], user_context: Optional[Dict[str, Any]] = None):
        """
        스트리밍 방식으로 AI 응답 생성
        
        Args:
            messages: 대화 히스토리
            user_context: 사용자 정보
            
        Yields:
            스트리밍 응답 청크
        """
        try:
            # 시스템 메시지 설정
            system_message = self._create_system_message(user_context)
            
            # 전체 대화 컨텍스트 구성
            full_messages = [system_message] + messages
            
            # 스트리밍 OpenAI API 호출
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                max_tokens=500,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"오류: {str(e)}"
    
    def _create_system_message(self, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """
        시스템 메시지 생성 (AI의 역할과 행동 방식 정의)
        
        Args:
            user_context: 사용자 정보
            
        Returns:
            시스템 메시지 딕셔너리
        """
        base_prompt = """
        당신은 교육용 AI 어시스턴트입니다. 
        선생님과 학생들이 함께 사용하는 교육 플랫폼에서 도움을 제공합니다.
        
        다음 지침을 따라주세요:
        1. 친근하고 도움이 되는 톤으로 대화하세요
        2. 교육적 가치가 있는 답변을 제공하세요
        3. 학습에 도움이 되는 질문이나 설명을 해주세요
        4. 부적절한 내용은 정중히 거절하세요
        5. 한국어로 답변해주세요
        """
        
        if user_context:
            user_type = user_context.get('user_type', 'student')
            user_name = user_context.get('user_name', '사용자')
            
            if user_type == 'teacher':
                base_prompt += f"""
                
                현재 대화 상대는 {user_name} 선생님입니다.
                선생님의 수업 준비나 학생 관리에 도움이 되는 조언을 제공하세요.
                """
            else:
                base_prompt += f"""
                
                현재 대화 상대는 {user_name} 학생입니다.
                학습에 도움이 되는 친근한 설명과 격려를 제공하세요.
                """
        
        return {"role": "system", "content": base_prompt}
    
    def generate_educational_response(self, question: str, subject: Optional[str] = None, level: Optional[str] = None) -> str:
        """
        교육적 질문에 대한 특화된 응답 생성
        
        Args:
            question: 교육 관련 질문
            subject: 과목 (선택사항)
            level: 학습 수준 (선택사항)
            
        Returns:
            교육적 AI 응답
        """
        messages = [
            {
                "role": "user",
                "content": f"질문: {question}" + 
                          (f"\n과목: {subject}" if subject else "") +
                          (f"\n수준: {level}" if level else "")
            }
        ]
        
        return self.generate_response(messages)
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료 - 리소스 정리"""
        if hasattr(self.client, 'close'):
            self.client.close()
        if hasattr(self.async_client, 'close'):
            asyncio.create_task(self.async_client.close())