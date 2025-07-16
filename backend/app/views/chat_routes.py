"""
채팅 관련 API 라우트
스레드 기반 1:1 AI 채팅 기능 제공
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

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