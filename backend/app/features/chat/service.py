"""
Chat service
Business logic for chat operations with OpenAI integration
"""
import base64
from datetime import datetime
from typing import List, Dict, Any
from fastapi import HTTPException, Request, UploadFile

from app.core.services.openai_service import OpenAIService
from app.core.services.database_service import DatabaseService
from .models import ChatRequest, ChatResponse, ChatHistoryResponse


class ChatService:
    """
    채팅 관련 비즈니스 로직을 처리하는 서비스
    OpenAI API와 데이터베이스 연동을 담당
    """
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.db_service = DatabaseService()

    async def chat_with_ai(self, request: ChatRequest) -> ChatResponse:
        """
        AI와 스레드 기반 1:1 채팅
        사용자별로 대화 기록이 유지됨
        Graceful degradation: DB 오류 시에도 AI 응답 제공
        """
        thread_id = None
        previous_messages = []
        
        # 1. 데이터베이스 스레드 조회 시도 (실패해도 계속 진행)
        try:
            thread = self.db_service.get_or_create_chat_thread(request.user_id, request.session_id)
            thread_id = thread["id"]
            
            # 기존 대화 기록 조회 시도
            previous_messages = self.db_service.get_thread_messages(thread_id, limit=20)
            print(f"✅ DB 연결 성공: Thread {thread_id}, 메시지 {len(previous_messages)}개")
            
        except Exception as e:
            print(f"⚠️ DB 연결 실패, 대화 기록 없이 진행: {str(e)}")
            thread_id = 0  # 임시 thread_id
            previous_messages = []
        
        # 2. OpenAI API 형식으로 변환
        openai_messages = []
        for msg in previous_messages:
            role = "assistant" if msg["is_ai_response"] else "user"
            openai_messages.append({
                "role": role,
                "content": msg["message"]
            })
        
        # 현재 메시지 추가
        openai_messages.append({
            "role": "user",
            "content": request.message
        })
        
        # 3. 사용자 컨텍스트 구성
        user_context = {
            "user_type": request.user_type,
            "user_name": request.user_name,
            "user_id": request.user_id
        }
        
        # 4. OpenAI 서비스 인스턴스 생성 및 AI 응답 생성
        try:
            ai_response = self.openai_service.generate_response(openai_messages, user_context)
        except Exception as e:
            print(f"❌ OpenAI API 오류: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"AI 응답 생성 실패: {str(e)}"
            )
        
        # 5. 데이터베이스 저장 시도 (실패해도 응답은 반환)
        saved_user_message = None
        saved_ai_message = None
        
        if thread_id and thread_id > 0:
            try:
                # 사용자 메시지 저장
                user_message_data = {
                    "thread_id": thread_id,
                    "user_id": request.user_id,
                    "user_name": request.user_name,
                    "user_type": request.user_type,
                    "message": request.message,
                    "is_ai_response": False,
                    "created_at": datetime.now().isoformat()
                }
                
                saved_user_message = self.db_service.create_thread_message(user_message_data)
                
                # AI 응답 저장
                ai_message_data = {
                    "thread_id": thread_id,
                    "user_id": 0,  # AI는 user_id 0
                    "user_name": "AI 어시스턴트",
                    "user_type": "ai",
                    "message": ai_response,
                    "is_ai_response": True,
                    "created_at": datetime.now().isoformat()
                }
                
                saved_ai_message = self.db_service.create_thread_message(ai_message_data)
                print(f"✅ 메시지 저장 성공")
                
            except Exception as e:
                print(f"⚠️ 메시지 저장 실패, 응답은 반환: {str(e)}")
                # 저장 실패 시 임시 메시지 객체 생성
                saved_user_message = {
                    "id": 0,
                    "thread_id": thread_id,
                    "user_id": request.user_id,
                    "user_name": request.user_name,
                    "user_type": request.user_type,
                    "message": request.message,
                    "is_ai_response": False,
                    "created_at": datetime.now().isoformat()
                }
                
                saved_ai_message = {
                    "id": 0,
                    "thread_id": thread_id,
                    "user_id": 0,
                    "user_name": "AI 어시스턴트",
                    "user_type": "ai",
                    "message": ai_response,
                    "is_ai_response": True,
                    "created_at": datetime.now().isoformat()
                }
        
        # 6. 응답 반환 (DB 저장 실패와 관계없이)
        return ChatResponse(
            response=ai_response,
            thread_id=thread_id or 0,
            user_message=saved_user_message or {},
            ai_message=saved_ai_message or {},
            status="success"
        )

    async def get_chat_history(self, user_id: int, session_id: int) -> ChatHistoryResponse:
        """
        사용자별 채팅 기록 조회
        """
        try:
            # 사용자의 채팅 스레드 조회
            thread = self.db_service.get_or_create_chat_thread(user_id, session_id)
            thread_id = thread["id"]
            
            # 스레드의 모든 메시지 조회
            messages = self.db_service.get_thread_messages(thread_id, limit=100)
            
            return ChatHistoryResponse(
                thread_id=thread_id,
                messages=messages,
                status="success"
            )
            
        except Exception as e:
            print(f"Error in get_chat_history: {str(e)}")
            raise HTTPException(
                status_code=500, 
                detail=f"채팅 기록 조회 실패: {str(e)}"
            )

    async def process_streaming_chat(self, request: Request):
        """
        스트리밍 채팅 처리
        파일 첨부 지원
        """
        # 폼 데이터 파싱
        form = await request.form()
        
        # 기본 파라미터 추출
        message = form.get('message', '')
        user_id = int(form.get('user_id', 0))
        session_id = int(form.get('session_id', 0))
        user_name = form.get('user_name', '')
        user_type = form.get('user_type', '')
        
        # 파일 파라미터 추출 (file_0, file_1, file_2... 형태)
        files = []
        for key, value in form.items():
            if key.startswith('file_') and hasattr(value, 'filename') and value.filename:
                files.append(value)
        
        thread_id = None
        previous_messages = []
        
        # 1. 파일 처리
        file_attachments = []
        if files:
            file_attachments = await self._process_file_attachments(files)

        # 2. 데이터베이스 스레드 조회 시도 (실패해도 계속 진행)
        try:
            thread = self.db_service.get_or_create_chat_thread(user_id, session_id)
            thread_id = thread["id"]
            
            # 기존 대화 기록 조회 시도
            previous_messages = self.db_service.get_thread_messages(thread_id, limit=20)
            print(f"✅ DB 연결 성공: Thread {thread_id}, 메시지 {len(previous_messages)}개")
            
        except Exception as e:
            print(f"⚠️ DB 연결 실패, 대화 기록 없이 진행: {str(e)}")
            thread_id = 0  # 임시 thread_id
            previous_messages = []
        
        # 3. OpenAI API 형식으로 변환
        openai_messages = []
        for msg in previous_messages:
            role = "assistant" if msg["is_ai_response"] else "user"
            openai_messages.append({
                "role": role,
                "content": msg["message"]
            })
        
        # 현재 메시지 구성 (파일 첨부 포함)
        current_message_content = []
        
        # 텍스트 메시지 추가
        if message.strip():
            current_message_content.append({
                "type": "text",
                "text": message
            })
        
        # 파일 첨부 추가
        for attachment in file_attachments:
            if attachment["type"] == "image":
                current_message_content.append({
                    "type": "image_url",
                    "image_url": {"url": attachment["data"]}
                })
            elif attachment["type"] == "text":
                current_message_content.append({
                    "type": "text",
                    "text": f"[파일: {attachment['name']}]\n{attachment['data']}"
                })
            elif attachment["type"] == "binary":
                current_message_content.append({
                    "type": "text",
                    "text": f"[첨부파일: {attachment['name']} ({attachment['size']} bytes) - 지원되지 않는 파일 형식]"
                })
        
        # 메시지가 비어있으면 기본 메시지 추가
        if not current_message_content:
            current_message_content.append({
                "type": "text",
                "text": "파일을 첨부했습니다."
            })
        
        # OpenAI API 호출 방식 결정
        if len(current_message_content) == 1 and current_message_content[0]["type"] == "text":
            # 단순 텍스트 메시지인 경우
            openai_messages.append({
                "role": "user",
                "content": current_message_content[0]["text"]
            })
        else:
            # 멀티모달 메시지인 경우 (파일 첨부 포함)
            openai_messages.append({
                "role": "user",
                "content": current_message_content
            })
        
        # 4. 사용자 컨텍스트 구성
        user_context = {
            "user_type": user_type,
            "user_name": user_name,
            "user_id": user_id
        }
        
        return {
            "openai_messages": openai_messages,
            "user_context": user_context,
            "thread_id": thread_id,
            "files": files,
            "file_attachments": file_attachments,
            "original_message": message,
            "user_id": user_id,
            "user_name": user_name,
            "user_type": user_type
        }

    async def _process_file_attachments(self, files: List[UploadFile]) -> List[Dict[str, Any]]:
        """
        파일 첨부 처리
        """
        file_attachments = []
        
        for file in files:
            if file.filename:
                try:
                    # 파일 내용 읽기
                    file_content = await file.read()
                    
                    # 이미지 파일인 경우 base64로 인코딩
                    if file.content_type and file.content_type.startswith('image/'):
                        base64_content = base64.b64encode(file_content).decode('utf-8')
                        file_attachments.append({
                            "type": "image",
                            "name": file.filename,
                            "content_type": file.content_type,
                            "data": f"data:{file.content_type};base64,{base64_content}"
                        })
                    else:
                        # 텍스트 파일인 경우
                        try:
                            text_content = file_content.decode('utf-8')
                            file_attachments.append({
                                "type": "text",
                                "name": file.filename,
                                "content_type": file.content_type,
                                "data": text_content
                            })
                        except UnicodeDecodeError:
                            # 바이너리 파일은 파일명만 표시
                            file_attachments.append({
                                "type": "binary",
                                "name": file.filename,
                                "content_type": file.content_type,
                                "size": len(file_content),
                                "raw_data": file_content
                            })
                except Exception as e:
                    print(f"파일 처리 오류 ({file.filename}): {str(e)}")
                    continue
        
        return file_attachments