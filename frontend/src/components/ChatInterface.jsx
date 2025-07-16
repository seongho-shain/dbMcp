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
  const [attachedFiles, setAttachedFiles] = useState([])
  const [isDragging, setIsDragging] = useState(false)
  const messagesEndRef = useRef(null)
  const fileInputRef = useRef(null)

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

  // 파일 첨부 상태 초기화
  const resetFileAttachments = () => {
    setAttachedFiles([])
    // 파일 입력 필드도 초기화
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  // 파일 첨부 관련 함수들
  const handleFileSelect = (event) => {
    const files = Array.from(event.target.files)
    addFiles(files)
  }

  const addFiles = (files) => {
    const validFiles = files.filter(file => {
      // 파일 크기 제한 (10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert(`파일 ${file.name}이 너무 큽니다. 10MB 이하의 파일만 첨부할 수 있습니다.`)
        return false
      }
      
      // 지원되는 파일 형식 확인
      const supportedTypes = [
        'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp',
        'text/plain', 'text/csv', 'text/html', 'text/css', 'text/javascript',
        'application/json', 'application/xml', 'text/xml',
        'application/pdf'
      ]
      
      const supportedExtensions = ['.txt', '.md', '.csv', '.html', '.css', '.js', '.json', '.xml', '.pdf']
      
      const isTypeSupported = supportedTypes.includes(file.type)
      const isExtensionSupported = supportedExtensions.some(ext => file.name.toLowerCase().endsWith(ext))
      
      if (!isTypeSupported && !isExtensionSupported) {
        alert(`파일 ${file.name}은 지원되지 않는 형식입니다.\n지원되는 형식: 이미지(jpg, png, gif, webp), 텍스트(txt, md, csv, html, css, js, json, xml), PDF`)
        return false
      }
      
      return true
    })

    if (validFiles.length > 0) {
      setAttachedFiles(prev => {
        // 중복 파일 제거 (이름과 크기로 비교)
        const newFiles = validFiles.filter(newFile => 
          !prev.some(existingFile => 
            existingFile.name === newFile.name && existingFile.size === newFile.size
          )
        )
        return [...prev, ...newFiles]
      })
    }
  }

  const removeFile = (index) => {
    setAttachedFiles(prev => prev.filter((_, i) => i !== index))
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const files = Array.from(e.dataTransfer.files)
    addFiles(files)
  }

  // 메시지 전송
  const sendMessage = async () => {
    if ((!inputMessage.trim() && attachedFiles.length === 0) || isLoading) return

    const messageText = inputMessage.trim()
    setInputMessage('')
    setIsLoading(true)

    // 1. 사용자 메시지 즉시 렌더링 (파일 정보 포함)
    const userMessage = {
      id: Date.now(),
      message: messageText || (attachedFiles.length > 0 ? '파일을 첨부했습니다.' : ''),
      is_ai_response: false,
      user_name: user.name,
      user_type: user.user_type,
      created_at: new Date().toISOString(),
      attachments: attachedFiles.map(file => ({
        name: file.name,
        size: file.size,
        type: file.type
      }))
    }
    
    // 사용자 메시지를 즉시 화면에 표시
    setMessages(prev => [...prev, userMessage])

    // 2. AI 응답을 위한 임시 메시지 생성
    const aiMessageId = Date.now() + 1
    const aiMessage = {
      id: aiMessageId,
      message: '',
      is_ai_response: true,
      user_name: 'AI 어시스턴트',
      user_type: 'ai',
      created_at: new Date().toISOString()
    }
    
    // AI 메시지를 빈 상태로 미리 추가
    setMessages(prev => [...prev, aiMessage])

    try {
      // 3. FormData로 파일과 메시지 준비
      const formData = new FormData()
      formData.append('message', messageText)
      formData.append('user_id', user.id)
      formData.append('session_id', user.session_id)
      formData.append('user_name', user.name)
      formData.append('user_type', user.user_type)
      
      // 파일 첨부
      attachedFiles.forEach((file, index) => {
        formData.append(`file_${index}`, file)
      })

      // 4. 스트리밍 API 호출
      const response = await fetch(`${API_BASE_URL}/chat/ai/stream`, {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        const reader = response.body.getReader()
        const decoder = new TextDecoder()
        
        while (true) {
          const { done, value } = await reader.read()
          if (done) break
          
          const chunk = decoder.decode(value)
          const lines = chunk.split('\n')
          
          for (const line of lines) {
            if (line.trim().startsWith('data: ')) {
              try {
                const data = JSON.parse(line.trim().substring(6))
                
                if (data.type === 'chunk') {
                  // 스트리밍 텍스트를 실시간으로 업데이트
                  setMessages(prev => prev.map(msg => 
                    msg.id === aiMessageId 
                      ? { ...msg, message: msg.message + data.content }
                      : msg
                  ))
                } else if (data.type === 'done') {
                  // 스트리밍 완료 시 스레드 ID 업데이트
                  setThreadId(data.thread_id)
                } else if (data.type === 'error') {
                  throw new Error(data.message)
                }
              } catch (parseError) {
                console.error('JSON 파싱 오류:', parseError)
              }
            }
          }
        }
      } else {
        throw new Error('AI 응답 실패')
      }
    } catch (error) {
      console.error('메시지 전송 오류:', error)
      
      // 에러 시 AI 메시지 내용을 오류 메시지로 업데이트
      setMessages(prev => prev.map(msg => 
        msg.id === aiMessageId 
          ? { ...msg, message: '죄송합니다. 현재 AI 서비스를 이용할 수 없습니다.' }
          : msg
      ))
    } finally {
      setIsLoading(false)
      resetFileAttachments() // 전송 후 첨부파일 초기화
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
            <p>📎 파일을 첨부하여 질문할 수도 있습니다.</p>
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
                {message.attachments && message.attachments.length > 0 && (
                  <div className="message-attachments">
                    {message.attachments.map((attachment, idx) => (
                      <div key={idx} className="attachment-item">
                        <span className="attachment-icon">📎</span>
                        <span className="attachment-name">{attachment.name}</span>
                        <span className="attachment-size">
                          ({(attachment.size / 1024).toFixed(1)}KB)
                        </span>
                      </div>
                    ))}
                  </div>
                )}
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

      <div 
        className={`chat-input ${isDragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {/* 파일 첨부 영역 */}
        {attachedFiles.length > 0 && (
          <div className="attached-files">
            <div className="attached-files-header">
              <span>첨부된 파일 ({attachedFiles.length})</span>
            </div>
            <div className="attached-files-list">
              {attachedFiles.map((file, index) => (
                <div key={index} className="attached-file-item">
                  <span className="file-icon">📎</span>
                  <span className="file-name">{file.name}</span>
                  <span className="file-size">({(file.size / 1024).toFixed(1)}KB)</span>
                  <button
                    onClick={() => removeFile(index)}
                    className="remove-file-button"
                    title="파일 제거"
                  >
                    ×
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="input-container">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            multiple
            style={{ display: 'none' }}
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            className="file-attach-button"
            disabled={isLoading}
            title="파일 첨부"
          >
            📎
          </button>
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="메시지를 입력하거나 파일을 드래그하세요... (Enter: 전송, Shift+Enter: 줄바꿈)"
            rows="1"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || (!inputMessage.trim() && attachedFiles.length === 0)}
            className="send-button"
          >
            {isLoading ? '전송 중...' : '전송'}
          </button>
        </div>
        <div className="input-hint">
          💡 AI에게 궁금한 것을 물어보세요! 파일을 첨부하여 질문할 수도 있습니다.
        </div>
        {isDragging && (
          <div className="drag-overlay">
            <div className="drag-message">
              📎 파일을 여기에 놓으세요
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatInterface