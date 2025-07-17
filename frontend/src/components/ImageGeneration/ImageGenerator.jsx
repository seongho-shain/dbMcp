import { useState, useEffect, useRef } from 'react'
import './ImageGenerator.css'

const API_BASE_URL = 'http://localhost:8000'

const ImageGenerator = ({ onClose }) => {
  const [activeTab, setActiveTab] = useState('generation')
  const [generationType, setGenerationType] = useState('core')
  const [generationMode, setGenerationMode] = useState('text-to-image')
  
  // 폼 데이터
  const [formData, setFormData] = useState({
    prompt: '',
    negative_prompt: '',
    output_format: 'png',
    aspect_ratio: '1:1',
    style_preset: '',
    seed: '',
    // SD3.5 전용
    model: 'sd3.5-large',
    strength: 0.8,
    // 제어 전용
    control_strength: 0.7,
  })

  // 파일 관리
  const [uploadedImage, setUploadedImage] = useState(null)
  const [uploadPreview, setUploadPreview] = useState(null)
  
  // UI 상태
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [generatedImage, setGeneratedImage] = useState(null)
  const [constants, setConstants] = useState(null)
  // const [educationalPrompts, setEducationalPrompts] = useState(null) // 제거됨
  
  const fileInputRef = useRef(null)

  // 상수 데이터 로드
  useEffect(() => {
    const loadConstants = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/image/constants`)
        if (response.ok) {
          const data = await response.json()
          setConstants(data)
        }
      } catch (error) {
        console.error('상수 로드 실패:', error)
      }
    }

    loadConstants()
  }, [])

  // 폼 데이터 업데이트
  const updateFormData = (key, value) => {
    setFormData(prev => ({ ...prev, [key]: value }))
  }

  // 파일 선택 처리
  const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
      // 파일 크기 및 형식 검증
      const maxSize = 50 * 1024 * 1024 // 50MB
      const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']
      
      if (file.size > maxSize) {
        setError('파일 크기가 50MB를 초과합니다.')
        return
      }
      
      if (!allowedTypes.includes(file.type)) {
        setError('지원되지 않는 파일 형식입니다. (JPEG, PNG, WebP만 지원)')
        return
      }
      
      setUploadedImage(file)
      setUploadPreview(URL.createObjectURL(file))
      setError(null)
    }
  }

  // 파일 드래그 앤 드롭 처리
  const handleDragOver = (e) => {
    e.preventDefault()
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const files = e.dataTransfer.files
    if (files.length > 0) {
      const file = files[0]
      // 파일 입력 필드에 설정
      const dt = new DataTransfer()
      dt.items.add(file)
      fileInputRef.current.files = dt.files
      handleFileSelect({ target: { files: [file] } })
    }
  }

  // 이미지 생성 API 호출
  const generateImage = async () => {
    try {
      setLoading(true)
      setError(null)
      setGeneratedImage(null)

      const formDataToSend = new FormData()
      
      // 기본 데이터 추가
      Object.keys(formData).forEach(key => {
        if (formData[key] !== '' && formData[key] !== null) {
          formDataToSend.append(key, formData[key])
        }
      })

      // 모드에 따른 파일 추가
      if (generationMode === 'image-to-image' && uploadedImage) {
        formDataToSend.append('image', uploadedImage)
      }

      // API 엔드포인트 결정
      let endpoint
      switch (generationType) {
        case 'core':
          endpoint = '/api/image/generate/core'
          break
        case 'sd35':
          endpoint = '/api/image/generate/sd35'
          formDataToSend.append('mode', generationMode)
          break
        case 'ultra':
          endpoint = '/api/image/generate/ultra'
          break
        default:
          throw new Error('알 수 없는 생성 타입')
      }

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        body: formDataToSend
      })

      if (response.ok) {
        // 모든 모델이 이미지 바이너리 응답으로 통일
        const imageBlob = await response.blob()
        const imageUrl = URL.createObjectURL(imageBlob)
        setGeneratedImage(imageUrl)
      } else {
        const errorData = await response.json()
        throw new Error(errorData.detail || '이미지 생성 실패')
      }

    } catch (err) {
      console.error('이미지 생성 오류:', err)
      setError(err.message || '이미지 생성 중 오류가 발생했습니다.')
    } finally {
      setLoading(false)
    }
  }

  // 스케치 변환 API 호출
  const convertSketch = async () => {
    try {
      setLoading(true)
      setError(null)
      setGeneratedImage(null)

      if (!uploadedImage) {
        throw new Error('스케치 이미지를 업로드해주세요.')
      }

      const formDataToSend = new FormData()
      
      Object.keys(formData).forEach(key => {
        if (formData[key] !== '' && formData[key] !== null) {
          formDataToSend.append(key, formData[key])
        }
      })

      formDataToSend.append('image', uploadedImage)

      const response = await fetch(`${API_BASE_URL}/api/image/control/sketch`, {
        method: 'POST',
        body: formDataToSend
      })

      if (response.ok) {
        const imageBlob = await response.blob()
        const imageUrl = URL.createObjectURL(imageBlob)
        setGeneratedImage(imageUrl)
      } else {
        const errorData = await response.json()
        throw new Error(errorData.detail || '스케치 변환 실패')
      }

    } catch (err) {
      console.error('스케치 변환 오류:', err)
      setError(err.message || '스케치 변환 중 오류가 발생했습니다.')
    } finally {
      setLoading(false)
    }
  }

  // 교육용 프롬프트 예시 선택 (제거됨)
  // const selectEducationalPrompt = (prompt) => {
  //   updateFormData('prompt', prompt)
  // }

  if (!constants) {
    return <div className="image-generator-loading">로딩 중...</div>
  }

  return (
    <div className="image-generator">
      <div className="image-generator-header">
        <h2>🎨 AI 이미지 생성</h2>
      </div>

      <div className="image-generator-tabs">
        <button 
          className={`tab-btn ${activeTab === 'generation' ? 'active' : ''}`}
          onClick={() => setActiveTab('generation')}
        >
          이미지 생성
        </button>
        <button 
          className={`tab-btn ${activeTab === 'control' ? 'active' : ''}`}
          onClick={() => setActiveTab('control')}
        >
          스케치 변환
        </button>
      </div>

      <div className="image-generator-content">
        {activeTab === 'generation' && (
          <div className="generation-panel">
            <div className="controls">
              {/* 생성 타입 선택 */}
              <div className="control-group">
                <label>생성 모델</label>
                <select 
                  value={generationType} 
                  onChange={(e) => setGenerationType(e.target.value)}
                >
                  <option value="core">Core (기본) - 3 크레딧</option>
                  <option value="sd35">SD 3.5 (고급) - 4 크레딧</option>
                  <option value="ultra">Ultra (최고급) - 8 크레딧</option>
                </select>
              </div>

              {/* SD3.5 모드 선택 */}
              {generationType === 'sd35' && (
                <div className="control-group">
                  <label>생성 모드</label>
                  <select 
                    value={generationMode} 
                    onChange={(e) => setGenerationMode(e.target.value)}
                  >
                    <option value="text-to-image">텍스트 → 이미지</option>
                    <option value="image-to-image">이미지 → 이미지</option>
                  </select>
                </div>
              )}

              {/* 프롬프트 입력 */}
              <div className="control-group">
                <label>프롬프트</label>
                <textarea
                  value={formData.prompt}
                  onChange={(e) => updateFormData('prompt', e.target.value)}
                  placeholder="생성하고 싶은 이미지를 상세히 설명해주세요..."
                  rows={4}
                />
              </div>

              {/* 교육용 프롬프트 예시 제거됨 */}

              {/* 이미지 업로드 (Image-to-Image 모드) */}
              {generationMode === 'image-to-image' && (
                <div className="control-group">
                  <label>입력 이미지</label>
                  <div 
                    className="file-upload-area"
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                  >
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/*"
                      onChange={handleFileSelect}
                      style={{ display: 'none' }}
                    />
                    <div onClick={() => fileInputRef.current?.click()}>
                      {uploadPreview ? (
                        <img src={uploadPreview} alt="업로드된 이미지" className="upload-preview" />
                      ) : (
                        <div className="upload-placeholder">
                          <p>📷 이미지를 클릭하거나 드래그해주세요</p>
                          <small>JPEG, PNG, WebP 지원 (최대 50MB)</small>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* 기본 설정들 */}
              <div className="basic-controls">
                <div className="control-row">
                  <div className="control-group">
                    <label>출력 형식</label>
                    <select 
                      value={formData.output_format}
                      onChange={(e) => updateFormData('output_format', e.target.value)}
                    >
                      <option value="png">PNG</option>
                      <option value="jpeg">JPEG</option>
                      <option value="webp">WEBP</option>
                    </select>
                  </div>

                  {/* 종횡비 */}
                  {(generationType !== 'sd35' || generationMode !== 'image-to-image') && (
                    <div className="control-group">
                      <label>이미지 비율</label>
                      <select 
                        value={formData.aspect_ratio}
                        onChange={(e) => updateFormData('aspect_ratio', e.target.value)}
                      >
                        <option value="1:1">정사각형 (1:1)</option>
                        <option value="16:9">가로형 (16:9)</option>
                        <option value="9:16">세로형 (9:16)</option>
                        <option value="3:2">가로형 (3:2)</option>
                        <option value="2:3">세로형 (2:3)</option>
                        <option value="5:4">가로형 (5:4)</option>
                        <option value="4:5">세로형 (4:5)</option>
                        <option value="21:9">울트라 와이드 (21:9)</option>
                        <option value="9:21">울트라 세로 (9:21)</option>
                      </select>
                    </div>
                  )}

                  <div className="control-group">
                    <label>스타일 프리셋</label>
                    <select 
                      value={formData.style_preset}
                      onChange={(e) => updateFormData('style_preset', e.target.value)}
                    >
                      <option value="">기본 스타일</option>
                      <option value="3d-model">3D 모델링 스타일</option>
                      <option value="analog-film">아날로그 필름 스타일</option>
                      <option value="anime">일본 애니메이션 스타일</option>
                      <option value="cinematic">영화적 스타일</option>
                      <option value="comic-book">만화책 스타일</option>
                      <option value="digital-art">디지털 아트 스타일</option>
                      <option value="enhance">품질 향상 스타일</option>
                      <option value="fantasy-art">판타지 아트 스타일</option>
                      <option value="isometric">아이소메트릭 스타일</option>
                      <option value="line-art">선화 스타일</option>
                      <option value="low-poly">로우 폴리 스타일</option>
                      <option value="modeling-compound">모델링 컴파운드 스타일</option>
                      <option value="neon-punk">네온펑크 스타일</option>
                      <option value="origami">종이접기 스타일</option>
                      <option value="photographic">사진과 같은 현실적 스타일</option>
                      <option value="pixel-art">픽셀 아트 스타일</option>
                      <option value="tile-texture">타일 텍스처 스타일</option>
                    </select>
                  </div>
                </div>

                {/* SD3.5 전용 설정 */}
                {generationType === 'sd35' && (
                  <div className="control-row">
                    <div className="control-group">
                      <label>SD3.5 모델</label>
                      <select 
                        value={formData.model}
                        onChange={(e) => updateFormData('model', e.target.value)}
                      >
                        <option value="sd3.5-large">최고 품질 (느림)</option>
                        <option value="sd3.5-large-turbo">빠른 생성 (중간 품질)</option>
                        <option value="sd3.5-medium">균형잡힌 품질과 속도</option>
                      </select>
                    </div>

                    {generationMode === 'image-to-image' && (
                      <div className="control-group">
                        <label>변형 강도: {formData.strength}</label>
                        <input
                          type="range"
                          min="0"
                          max="1"
                          step="0.1"
                          value={formData.strength}
                          onChange={(e) => updateFormData('strength', parseFloat(e.target.value))}
                        />
                      </div>
                    )}
                  </div>
                )}
              </div>

              <button 
                className="generate-btn"
                onClick={generateImage}
                disabled={loading || !formData.prompt.trim()}
              >
                {loading ? '생성 중...' : '🎨 이미지 생성'}
              </button>
            </div>
          </div>
        )}

        {activeTab === 'control' && (
          <div className="control-panel">
            <div className="controls">
              <div className="control-group">
                <label>프롬프트</label>
                <textarea
                  value={formData.prompt}
                  onChange={(e) => updateFormData('prompt', e.target.value)}
                  placeholder="스케치를 어떤 이미지로 변환할지 설명해주세요..."
                  rows={3}
                />
              </div>

              <div className="control-group">
                <label>스케치 이미지</label>
                <div 
                  className="file-upload-area"
                  onDragOver={handleDragOver}
                  onDrop={handleDrop}
                >
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    style={{ display: 'none' }}
                  />
                  <div onClick={() => fileInputRef.current?.click()}>
                    {uploadPreview ? (
                      <img src={uploadPreview} alt="업로드된 스케치" className="upload-preview" />
                    ) : (
                      <div className="upload-placeholder">
                        <p>✏️ 스케치 이미지를 클릭하거나 드래그해주세요</p>
                        <small>JPEG, PNG, WebP 지원 (최대 50MB)</small>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              <div className="control-group">
                <label>제어 강도: {formData.control_strength}</label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={formData.control_strength}
                  onChange={(e) => updateFormData('control_strength', parseFloat(e.target.value))}
                />
              </div>

              <button 
                className="generate-btn"
                onClick={convertSketch}
                disabled={loading || !uploadedImage || !formData.prompt.trim()}
              >
                {loading ? '변환 중...' : '✏️ 스케치 → 이미지'}
              </button>
            </div>
          </div>
        )}

        {/* 결과 영역 */}
        <div className="result-area">
          {loading && (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <p>AI가 이미지를 생성하고 있습니다...</p>
            </div>
          )}
          
          {error && (
            <div className="error-display">
              <h3>⚠️ 오류 발생</h3>
              <p>{error}</p>
              <button onClick={() => setError(null)}>닫기</button>
            </div>
          )}
          
          {generatedImage && (
            <div className="generated-image">
              <h3>✨ 생성된 이미지</h3>
              <img src={generatedImage} alt="생성된 이미지" />
              <div className="image-actions">
                <a 
                  href={generatedImage} 
                  download={`ai-generated-${Date.now()}.${formData.output_format}`}
                  className="download-btn"
                >
                  💾 다운로드
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ImageGenerator