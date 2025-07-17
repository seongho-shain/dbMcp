import React, { useState, useRef } from 'react';
import { useAuth } from '../../AuthContext';
import './GalleryUploadModal.css';

const API_BASE_URL = 'http://localhost:8000';

function GalleryUploadModal({ isOpen, onClose, sessionId, onUploadSuccess }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [title, setTitle] = useState('');
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);
  const { user } = useAuth();

  const handleFileSelect = (file) => {
    if (!file) return;

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      alert('지원하지 않는 파일 형식입니다. JPG, PNG, WebP 파일만 업로드 가능합니다.');
      return;
    }

    // Validate file size (5MB limit)
    const maxSize = 5 * 1024 * 1024; // 5MB in bytes
    if (file.size > maxSize) {
      alert('파일 크기가 너무 큽니다. 5MB 이하의 파일만 업로드 가능합니다.');
      return;
    }

    setSelectedFile(file);

    // Create preview URL
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    handleFileSelect(file);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleFileSelect(files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedFile || !prompt.trim()) {
      alert('이미지와 프롬프트를 모두 입력해주세요.');
      return;
    }

    if (!sessionId || !user) {
      alert('세션 정보가 없습니다. 다시 로그인해주세요.');
      return;
    }

    setUploading(true);
    
    try {
      const formData = new FormData();
      formData.append('image', selectedFile);
      formData.append('session_id', sessionId.toString());
      formData.append('user_id', user.id.toString());
      formData.append('user_name', user.name);
      formData.append('user_type', user.user_type);
      formData.append('prompt', prompt.trim());
      if (title.trim()) {
        formData.append('title', title.trim());
      }

      const response = await fetch(`${API_BASE_URL}/api/gallery/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.success) {
        alert('작품이 성공적으로 업로드되었습니다!');
        
        // Reset form
        setSelectedFile(null);
        setPreviewUrl(null);
        setPrompt('');
        setTitle('');
        
        // Call success callback
        if (onUploadSuccess) {
          onUploadSuccess(data.item);
        }
        
        onClose();
      } else {
        throw new Error(data.detail || data.error || '업로드에 실패했습니다.');
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert(`업로드 실패: ${error.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleClose = () => {
    if (uploading) return; // Don't close while uploading
    
    // Clean up preview URL
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    
    // Reset form
    setSelectedFile(null);
    setPreviewUrl(null);
    setPrompt('');
    setTitle('');
    setDragActive(false);
    
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="gallery-upload-modal-overlay" onClick={handleClose}>
      <div className="gallery-upload-modal" onClick={(e) => e.stopPropagation()}>
        <div className="gallery-upload-modal__header">
          <h2>작품 업로드</h2>
          <button 
            className="gallery-upload-modal__close"
            onClick={handleClose}
            disabled={uploading}
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="gallery-upload-form">
          <div className="gallery-upload-form__section">
            <label className="gallery-upload-form__label">이미지 *</label>
            <div 
              className={`gallery-upload-dropzone ${dragActive ? 'active' : ''} ${selectedFile ? 'has-file' : ''}`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              
              {previewUrl ? (
                <div className="gallery-upload-preview">
                  <img src={previewUrl} alt="미리보기" />
                  <div className="gallery-upload-preview__overlay">
                    <span>클릭하여 다른 이미지 선택</span>
                  </div>
                </div>
              ) : (
                <div className="gallery-upload-dropzone__content">
                  <div className="gallery-upload-dropzone__icon">📸</div>
                  <p>이미지를 드래그하여 놓거나 클릭하여 선택하세요</p>
                  <small>JPG, PNG, WebP (최대 5MB)</small>
                </div>
              )}
            </div>
          </div>

          <div className="gallery-upload-form__section">
            <label className="gallery-upload-form__label" htmlFor="prompt">
              프롬프트 설명 *
            </label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="이 이미지를 생성할 때 사용한 프롬프트나 설명을 입력해주세요..."
              className="gallery-upload-form__textarea"
              rows={4}
              required
            />
            <small className="gallery-upload-form__help">
              다른 학생들이 참고할 수 있도록 자세히 작성해주세요.
            </small>
          </div>

          <div className="gallery-upload-form__section">
            <label className="gallery-upload-form__label" htmlFor="title">
              작품 제목 (선택사항)
            </label>
            <input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="작품에 제목을 붙여주세요"
              className="gallery-upload-form__input"
              maxLength={100}
            />
          </div>

          <div className="gallery-upload-form__actions">
            <button
              type="button"
              onClick={handleClose}
              className="gallery-upload-btn gallery-upload-btn--secondary"
              disabled={uploading}
            >
              취소
            </button>
            <button
              type="submit"
              className="gallery-upload-btn gallery-upload-btn--primary"
              disabled={uploading || !selectedFile || !prompt.trim()}
            >
              {uploading ? '업로드 중...' : '업로드'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default GalleryUploadModal;