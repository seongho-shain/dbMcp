"""
OpenAI API 서비스
OpenAI GPT 모델을 활용한 AI 응답 생성 서비스
채팅 메시지를 받아서 AI 응답을 생성하고 반환
파일 첨부 기능 포함 (이미지, 텍스트, 문서)
"""
import os
import asyncio
import base64
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
from fastapi import HTTPException, UploadFile
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion
from openai.types import FileObject

from app.config.settings import OPENAI_API_KEY, OPENAI_MODEL


class OpenAIService:
    """
    OpenAI API를 활용한 AI 응답 생성 서비스
    GPT 모델을 통해 자연스러운 대화형 응답 제공
    동기 및 비동기 모드 지원
    파일 첨부 기능 지원 (이미지, 텍스트, 문서)
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
        
        # 지원하는 파일 형식 정의
        self.SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        self.SUPPORTED_TEXT_FORMATS = {'.txt', '.md', '.json', '.csv', '.py', '.js', '.html', '.css'}
        self.SUPPORTED_DOC_FORMATS = {'.pdf', '.doc', '.docx'}
    
    def generate_response(self, messages: List[Dict[str, Any]], user_context: Optional[Dict[str, Any]] = None) -> str:
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
    
    async def generate_response_async(self, messages: List[Dict[str, Any]], user_context: Optional[Dict[str, Any]] = None) -> str:
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
    
    def generate_response_stream(self, messages: List[Dict[str, Any]], user_context: Optional[Dict[str, Any]] = None):
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
        6. 파일이 첨부된 경우, 해당 파일의 내용을 분석하고 구체적으로 답변하세요
        7. 이미지가 첨부된 경우, 이미지의 내용을 자세히 설명하고 관련 질문에 답변하세요
        8. 텍스트 파일이 첨부된 경우, 파일 내용을 읽고 분석하여 답변하세요
        9. 파일을 "열거나 다운로드할 수 없다"고 답변하지 마세요 - 첨부된 파일은 이미 분석 가능한 상태입니다
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
    
    def upload_file(self, file_path: Union[str, Path], purpose: str = "assistants") -> FileObject:
        """
        파일을 OpenAI API에 업로드
        
        Args:
            file_path: 업로드할 파일 경로
            purpose: 파일 용도 (assistants, fine-tune, batch 등)
            
        Returns:
            업로드된 파일 객체
            
        Raises:
            HTTPException: 파일 업로드 실패 시
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise HTTPException(status_code=400, detail="파일이 존재하지 않습니다.")
            
            # 파일 업로드
            with open(file_path, 'rb') as file:
                uploaded_file = self.client.files.create(
                    file=file,
                    purpose=purpose
                )
            
            print(f"✅ 파일 업로드 성공: {uploaded_file.id}")
            return uploaded_file
            
        except Exception as e:
            print(f"❌ 파일 업로드 실패: {str(e)}")
            raise HTTPException(status_code=500, detail=f"파일 업로드 실패: {str(e)}")
    
    def encode_image_to_base64(self, file_path: Union[str, Path]) -> str:
        """
        이미지 파일을 base64로 인코딩
        
        Args:
            file_path: 이미지 파일 경로
            
        Returns:
            base64 인코딩된 이미지 문자열
        """
        try:
            with open(file_path, 'rb') as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"이미지 인코딩 실패: {str(e)}")
    
    def generate_response_with_files(
        self, 
        messages: List[Dict[str, Any]], 
        files: Optional[List[UploadFile]] = None,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        파일 첨부가 포함된 AI 응답 생성
        
        Args:
            messages: 대화 히스토리
            files: 첨부 파일 목록
            user_context: 사용자 정보
            
        Returns:
            AI 생성 응답 텍스트
        """
        try:
            # 파일이 있는 경우 처리
            if files:
                processed_messages = self._process_files_in_messages(messages, files)
            else:
                processed_messages = messages
            
            # 기존 응답 생성 메서드 호출
            return self.generate_response(processed_messages, user_context)
            
        except Exception as e:
            print(f"❌ 파일 포함 응답 생성 실패: {str(e)}")
            raise HTTPException(status_code=500, detail=f"파일 포함 응답 생성 실패: {str(e)}")
    
    def _process_files_in_messages(self, messages: List[Dict[str, Any]], files: List[UploadFile]) -> List[Dict[str, Any]]:
        """
        메시지에 파일 정보를 포함시켜 처리
        
        Args:
            messages: 원본 메시지 목록
            files: 첨부 파일 목록
            
        Returns:
            파일 정보가 포함된 메시지 목록
        """
        processed_messages = messages.copy()
        
        # 마지막 사용자 메시지에 파일 정보 추가
        if processed_messages and processed_messages[-1].get('role') == 'user':
            last_message = processed_messages[-1]
            
            # 텍스트 content를 배열 형태로 변환
            if isinstance(last_message.get('content'), str):
                text_content = last_message['content']
                last_message['content'] = [
                    {"type": "text", "text": text_content}
                ]
            
            # 각 파일 처리
            for file in files:
                file_ext = Path(file.filename).suffix.lower()
                
                if file_ext in self.SUPPORTED_IMAGE_FORMATS:
                    # 이미지 파일 처리
                    file_content = file.file.read()
                    file.file.seek(0)  # 파일 포인터 리셋
                    
                    # base64 인코딩
                    encoded_image = base64.b64encode(file_content).decode('utf-8')
                    
                    # 이미지 타입 결정
                    image_type = file_ext.lstrip('.')
                    if image_type == 'jpg':
                        image_type = 'jpeg'
                    
                    # 메시지에 이미지 추가
                    last_message['content'].append({
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/{image_type};base64,{encoded_image}",
                            "detail": "high"
                        }
                    })
                    
                elif file_ext in self.SUPPORTED_TEXT_FORMATS:
                    # 텍스트 파일 처리
                    file_content = file.file.read().decode('utf-8')
                    file.file.seek(0)
                    
                    # 텍스트 내용을 메시지에 추가
                    last_message['content'].append({
                        "type": "text",
                        "text": f"\n\n[파일: {file.filename}]\n{file_content}"
                    })
                    
                elif file_ext in self.SUPPORTED_DOC_FORMATS:
                    # 문서 파일의 경우 OpenAI Files API 사용
                    # 임시 파일로 저장 후 업로드
                    temp_file_path = f"/tmp/{file.filename}"
                    with open(temp_file_path, 'wb') as temp_file:
                        temp_file.write(file.file.read())
                    
                    # 파일 업로드
                    uploaded_file = self.upload_file(temp_file_path)
                    
                    # 파일 정보를 메시지에 추가
                    last_message['content'].append({
                        "type": "text",
                        "text": f"\n\n[첨부 파일: {file.filename} (ID: {uploaded_file.id})]"
                    })
                    
                    # 임시 파일 삭제
                    os.remove(temp_file_path)
                    
                else:
                    # 지원하지 않는 파일 형식
                    last_message['content'].append({
                        "type": "text",
                        "text": f"\n\n[지원하지 않는 파일 형식: {file.filename}]"
                    })
        
        return processed_messages
    
    def get_file_content(self, file_id: str) -> str:
        """
        업로드된 파일의 내용을 가져오기
        
        Args:
            file_id: 파일 ID
            
        Returns:
            파일 내용 (텍스트)
        """
        try:
            file_content = self.client.files.retrieve_content(file_id)
            return file_content
        except Exception as e:
            print(f"❌ 파일 내용 조회 실패: {str(e)}")
            raise HTTPException(status_code=500, detail=f"파일 내용 조회 실패: {str(e)}")
    
    def delete_file(self, file_id: str) -> bool:
        """
        업로드된 파일 삭제
        
        Args:
            file_id: 삭제할 파일 ID
            
        Returns:
            삭제 성공 여부
        """
        try:
            self.client.files.delete(file_id)
            print(f"✅ 파일 삭제 성공: {file_id}")
            return True
        except Exception as e:
            print(f"❌ 파일 삭제 실패: {str(e)}")
            return False
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료 - 리소스 정리"""
        if hasattr(self.client, 'close'):
            self.client.close()
        if hasattr(self.async_client, 'close'):
            asyncio.create_task(self.async_client.close())