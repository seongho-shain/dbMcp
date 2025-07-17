"""
Chat routes
API endpoints for chat operations
"""
import json
import time
from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from .service import ChatService
from .models import ChatRequest, ChatResponse, ChatHistoryResponse, ChatHealthResponse

router = APIRouter(prefix="/chat", tags=["chat"])
chat_service = ChatService()


@router.post("/ai", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    AI와 스레드 기반 1:1 채팅
    사용자별로 대화 기록이 유지됨
    Graceful degradation: DB 오류 시에도 AI 응답 제공
    """
    return await chat_service.chat_with_ai(request)


@router.post("/ai/stream")
async def chat_with_ai_stream(request: Request):
    """
    AI와 스트리밍 방식 1:1 채팅 (파일 첨부 지원)
    사용자별로 대화 기록이 유지되며, 응답을 실시간으로 스트리밍
    """
    # 스트리밍 응답 생성 함수
    async def generate_streaming_response():
        try:
            # 요청 처리
            chat_data = await chat_service.process_streaming_chat(request)
            
            collected_response = ""
            
            # 파일 첨부가 있는 경우 업로드 파일 객체 변환
            upload_files = []
            if chat_data["files"]:
                for file in chat_data["files"]:
                    if file.filename:
                        # 파일 포인터를 처음으로 리셋
                        file.file.seek(0)
                        upload_files.append(file)
            
            # 스트리밍 응답 생성 - 파일 첨부 여부에 따라 다른 함수 사용
            if upload_files:
                # 파일 첨부가 있는 경우 새로운 generate_response_with_files 사용
                # 하지만 스트리밍은 지원하지 않으므로 일반 응답 생성 후 청크로 나누어 전송
                full_response = chat_service.openai_service.generate_response_with_files(
                    chat_data["openai_messages"], 
                    upload_files, 
                    chat_data["user_context"]
                )
                
                # 응답을 청크로 나누어 스트리밍 효과 생성
                words = full_response.split()
                for i, word in enumerate(words):
                    chunk = word + (" " if i < len(words) - 1 else "")
                    collected_response += chunk
                    yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
                    time.sleep(0.05)  # 스트리밍 효과를 위한 딜레이
            else:
                # 파일 첨부가 없는 경우 기존 스트리밍 방식 사용
                for chunk in chat_service.openai_service.generate_response_stream(
                    chat_data["openai_messages"], 
                    chat_data["user_context"]
                ):
                    if chunk and chunk.strip():
                        collected_response += chunk
                        # Server-Sent Events 형식으로 청크 전송
                        yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
            
            # 최종 응답을 데이터베이스에 저장
            if chat_data["thread_id"] and chat_data["thread_id"] > 0:
                try:
                    # 사용자 메시지 저장 (파일 첨부 정보 포함)
                    user_message_text = chat_data["original_message"]
                    if chat_data["file_attachments"]:
                        attachment_info = ", ".join([f"{att['name']}" for att in chat_data["file_attachments"]])
                        user_message_text += f" [첨부파일: {attachment_info}]"
                    
                    user_message_data = {
                        "thread_id": chat_data["thread_id"],
                        "user_id": chat_data["user_id"],
                        "user_name": chat_data["user_name"],
                        "user_type": chat_data["user_type"],
                        "message": user_message_text,
                        "is_ai_response": False,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    chat_service.db_service.create_thread_message(user_message_data)
                    
                    # AI 응답 저장
                    ai_message_data = {
                        "thread_id": chat_data["thread_id"],
                        "user_id": 0,  # AI는 user_id 0
                        "user_name": "AI 어시스턴트",
                        "user_type": "ai",
                        "message": collected_response,
                        "is_ai_response": True,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    chat_service.db_service.create_thread_message(ai_message_data)
                    print(f"✅ 메시지 저장 성공")
                    
                except Exception as e:
                    print(f"⚠️ 메시지 저장 실패: {str(e)}")
            
            # 스트리밍 완료 신호
            yield f"data: {json.dumps({'type': 'done', 'thread_id': chat_data['thread_id']})}\n\n"
            
        except Exception as e:
            print(f"❌ 스트리밍 오류: {str(e)}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        generate_streaming_response(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )


@router.get("/history/{user_id}/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(user_id: int, session_id: int):
    """
    사용자별 채팅 기록 조회
    """
    return await chat_service.get_chat_history(user_id, session_id)


@router.get("/health", response_model=ChatHealthResponse)
async def health_check():
    """
    채팅 서비스 상태 확인
    """
    return ChatHealthResponse(status="healthy", service="chat")