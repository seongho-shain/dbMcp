"""
채팅 관련 API 라우트
스레드 기반 1:1 AI 채팅 기능 제공
"""
from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import base64
import os

from app.services.openai_service import OpenAIService
from app.services.database_service import DatabaseService

router = APIRouter()

# 요청 모델
class ChatRequest(BaseModel):
    message: str
    user_id: int
    session_id: int
    user_name: str
    user_type: str  # 'teacher' or 'student'

# 응답 모델
class ChatResponse(BaseModel):
    response: str
    thread_id: int
    user_message: Dict[str, Any]
    ai_message: Dict[str, Any]
    status: str = "success"

class ChatHistoryResponse(BaseModel):
    thread_id: int
    messages: List[Dict[str, Any]]
    status: str = "success"

@router.post("/chat/ai/stream")
async def chat_with_ai_stream(
    request: Request
):
    """
    AI와 스트리밍 방식 1:1 채팅 (파일 첨부 지원)
    사용자별로 대화 기록이 유지되며, 응답을 실시간으로 스트리밍
    """
    from fastapi.responses import StreamingResponse
    import json
    
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
    
    db_service = DatabaseService()
    thread_id = None
    previous_messages = []
    
    # 1. 파일 처리
    file_attachments = []
    if files:
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
                            # 바이너리 파일은 파일명만 표시 (PDF 등)
                            file_attachments.append({
                                "type": "binary",
                                "name": file.filename,
                                "content_type": file.content_type,
                                "size": len(file_content),
                                "raw_data": file_content  # PDF 업로드를 위한 원본 데이터
                            })
                except Exception as e:
                    print(f"파일 처리 오류 ({file.filename}): {str(e)}")
                    continue

    # 2. 데이터베이스 스레드 조회 시도 (실패해도 계속 진행)
    try:
        thread = db_service.get_or_create_chat_thread(user_id, session_id)
        thread_id = thread["id"]
        
        # 기존 대화 기록 조회 시도
        previous_messages = db_service.get_thread_messages(thread_id, limit=20)
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
            # PDF 파일인 경우 base64 인코딩 시도
            if attachment.get("content_type") == "application/pdf":
                try:
                    # PDF를 base64로 인코딩하여 전송 (실험적)
                    base64_content = base64.b64encode(attachment["raw_data"]).decode('utf-8')
                    current_message_content.append({
                        "type": "text",
                        "text": f"[PDF 파일: {attachment['name']}]\n이 파일은 PDF 형식입니다. 현재 모델에서는 PDF 내용을 직접 분석할 수 없으므로 파일 정보만 제공합니다."
                    })
                except Exception as e:
                    print(f"PDF 파일 처리 실패: {str(e)}")
                    current_message_content.append({
                        "type": "text",
                        "text": f"[PDF 파일 처리 실패: {attachment['name']}]"
                    })
            else:
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
    
    # 4. 스트리밍 응답 생성 함수
    async def generate_streaming_response():
        try:
            openai_service = OpenAIService()
            collected_response = ""
            
            # 파일 첨부가 있는 경우 업로드 파일 객체 변환
            upload_files = []
            if files:
                for file in files:
                    if file.filename:
                        # 파일 포인터를 처음으로 리셋
                        file.file.seek(0)
                        upload_files.append(file)
            
            # 스트리밍 응답 생성 - 파일 첨부 여부에 따라 다른 함수 사용
            if upload_files:
                # 파일 첨부가 있는 경우 새로운 generate_response_with_files 사용
                # 하지만 스트리밍은 지원하지 않으므로 일반 응답 생성 후 청크로 나누어 전송
                full_response = openai_service.generate_response_with_files(openai_messages, upload_files, user_context)
                
                # 응답을 청크로 나누어 스트리밍 효과 생성
                import time
                words = full_response.split()
                for i, word in enumerate(words):
                    chunk = word + (" " if i < len(words) - 1 else "")
                    collected_response += chunk
                    yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
                    time.sleep(0.05)  # 스트리밍 효과를 위한 딜레이
            else:
                # 파일 첨부가 없는 경우 기존 스트리밍 방식 사용
                for chunk in openai_service.generate_response_stream(openai_messages, user_context):
                    if chunk and chunk.strip():
                        collected_response += chunk
                        # Server-Sent Events 형식으로 청크 전송
                        yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
            
            # 최종 응답을 데이터베이스에 저장
            if thread_id and thread_id > 0:
                try:
                    # 사용자 메시지 저장 (파일 첨부 정보 포함)
                    user_message_text = message
                    if file_attachments:
                        attachment_info = ", ".join([f"{att['name']}" for att in file_attachments])
                        user_message_text += f" [첨부파일: {attachment_info}]"
                    
                    user_message_data = {
                        "thread_id": thread_id,
                        "user_id": user_id,
                        "user_name": user_name,
                        "user_type": user_type,
                        "message": user_message_text,
                        "is_ai_response": False,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    db_service.create_thread_message(user_message_data)
                    
                    # AI 응답 저장
                    ai_message_data = {
                        "thread_id": thread_id,
                        "user_id": 0,  # AI는 user_id 0
                        "user_name": "AI 어시스턴트",
                        "user_type": "ai",
                        "message": collected_response,
                        "is_ai_response": True,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    db_service.create_thread_message(ai_message_data)
                    print(f"✅ 메시지 저장 성공")
                    
                except Exception as e:
                    print(f"⚠️ 메시지 저장 실패: {str(e)}")
            
            # 스트리밍 완료 신호
            yield f"data: {json.dumps({'type': 'done', 'thread_id': thread_id})}\n\n"
            
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

@router.post("/chat/ai", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    AI와 스레드 기반 1:1 채팅
    사용자별로 대화 기록이 유지됨
    Graceful degradation: DB 오류 시에도 AI 응답 제공
    """
    db_service = DatabaseService()
    thread_id = None
    previous_messages = []
    
    # 1. 데이터베이스 스레드 조회 시도 (실패해도 계속 진행)
    try:
        thread = db_service.get_or_create_chat_thread(request.user_id, request.session_id)
        thread_id = thread["id"]
        
        # 기존 대화 기록 조회 시도
        previous_messages = db_service.get_thread_messages(thread_id, limit=20)
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
        openai_service = OpenAIService()
        ai_response = openai_service.generate_response(openai_messages, user_context)
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
            
            saved_user_message = db_service.create_thread_message(user_message_data)
            
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
            
            saved_ai_message = db_service.create_thread_message(ai_message_data)
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

@router.get("/chat/history/{user_id}/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(user_id: int, session_id: int):
    """
    사용자별 채팅 기록 조회
    """
    try:
        db_service = DatabaseService()
        
        # 사용자의 채팅 스레드 조회
        thread = db_service.get_or_create_chat_thread(user_id, session_id)
        thread_id = thread["id"]
        
        # 스레드의 모든 메시지 조회
        messages = db_service.get_thread_messages(thread_id, limit=100)
        
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

@router.get("/chat/health")
async def health_check():
    """
    채팅 서비스 상태 확인
    """
    return {"status": "healthy", "service": "chat"}