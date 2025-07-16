import { useState, useEffect, useRef } from 'react'
import { useAuth } from '../AuthContext'
import './ChatInterface.css'

const API_BASE_URL = 'http://localhost:8000'

function ChatInterface() {
  const { user } = useAuth()
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [threadId, setThreadId] = useState(null)
  const messagesEndRef = useRef(null)

  // 스크롤을 최하단으로 이동
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  // 채팅 기록 로드
  const loadChatHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/history/${user.id}/${user.session_id}`)
      if (response.ok) {
        const data = await response.json()
        setThreadId(data.thread_id)
        setMessages(data.messages)
      }
    } catch (error) {
      console.error('채팅 기록 로드 실패:', error)
    }
  }

  // 메시지 전송
  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const messageText = inputMessage.trim()
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/chat/ai`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: messageText,
          user_id: user.id,
          session_id: user.session_id,
          user_name: user.name,
          user_type: user.user_type
        })
      })

      if (response.ok) {
        const data = await response.json()
        
        // 스레드 ID 설정
        setThreadId(data.thread_id)
        
        // 사용자 메시지와 AI 응답 추가
        setMessages(prev => [...prev, data.user_message, data.ai_message])
      } else {
        throw new Error('AI 응답 실패')
      }
    } catch (error) {
      console.error('메시지 전송 오류:', error)
      
      // 에러 메시지 표시
      const errorMessage = {
        id: Date.now(),
        message: '죄송합니다. 현재 AI 서비스를 이용할 수 없습니다.',
        is_ai_response: true,
        user_name: 'AI 어시스턴트',
        user_type: 'ai',
        created_at: new Date().toISOString()
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  // Enter 키 처리
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  // 메시지 타입에 따른 스타일링
  const getMessageClass = (message) => {
    return message.is_ai_response ? 'message ai-message' : 'message user-message'
  }

  // 시간 포맷팅
  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString('ko-KR', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  // 컴포넌트 마운트 시 채팅 기록 로드
  useEffect(() => {
    if (user && user.id && user.session_id) {
      loadChatHistory()
    }
  }, [user])

  // 메시지 업데이트 시 스크롤
  useEffect(() => {
    scrollToBottom()
  }, [messages])

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>💬 AI 채팅</h3>
        <div className="user-info">
          {user.name} ({user.user_type === 'teacher' ? '선생님' : '학생'})
          {threadId && <span className="thread-info">Thread #{threadId}</span>}
        </div>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <p>👋 안녕하세요! 궁금한 것이 있으면 언제든지 물어보세요.</p>
            <p>🤖 AI가 교육적인 답변을 제공해드립니다.</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div key={`${message.id}-${index}`} className={getMessageClass(message)}>
              <div className="message-header">
                <span className="sender-name">
                  {message.is_ai_response ? '🤖 AI 어시스턴트' : `${message.user_name}`}
                </span>
                <span className="message-time">{formatTime(message.created_at)}</span>
              </div>
              <div className="message-content">
                {message.message}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="loading-indicator">
            <div className="loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span>AI가 답변을 준비중입니다...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input">
        <div className="input-container">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="메시지를 입력하세요... (Enter: 전송, Shift+Enter: 줄바꿈)"
            rows="1"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !inputMessage.trim()}
            className="send-button"
          >
            {isLoading ? '전송 중...' : '전송'}
          </button>
        </div>
        <div className="input-hint">
          💡 AI에게 궁금한 것을 물어보세요!
        </div>
      </div>
    </div>
  )
}

export default ChatInterface