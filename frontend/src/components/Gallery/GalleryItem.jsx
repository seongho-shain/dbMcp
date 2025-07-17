import React, { useState } from 'react';
import { useAuth } from '../../AuthContext';
import './GalleryItem.css';

const API_BASE_URL = 'http://localhost:8000';

function GalleryItem({ item, onDelete }) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [showPromptModal, setShowPromptModal] = useState(false);
  const { user } = useAuth();

  const canDelete = user && (
    (user.user_type === 'student' && user.id === item.user_id && item.user_type === 'student') ||
    (user.user_type === 'teacher' && item.user_type === 'student')
  );

  const handleDelete = async () => {
    if (!canDelete || isDeleting) return;

    setIsDeleting(true);
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/gallery/${item.id}?user_id=${user.id}&user_type=${user.user_type}`,
        {
          method: 'DELETE',
        }
      );

      const data = await response.json();

      if (response.ok && data.success) {
        if (onDelete) {
          onDelete(item.id);
        }
      } else {
        throw new Error(data.detail || data.error || '삭제에 실패했습니다.');
      }
    } catch (error) {
      console.error('Delete error:', error);
      alert(`삭제 실패: ${error.message}`);
    } finally {
      setIsDeleting(false);
      setShowDeleteConfirm(false);
    }
  };

  const formatDate = (dateString) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return '날짜 정보 없음';
    }
  };

  const getUserTypeLabel = (userType) => {
    return userType === 'teacher' ? '선생님' : '학생';
  };

  return (
    <>
      <div className="gallery-item">
        <div className="gallery-item__image-container">
          <img 
            src={item.image_url} 
            alt={item.title || item.prompt} 
            className="gallery-item__image"
            loading="lazy"
          />
          <div className="gallery-item__overlay">
            <button 
              className="gallery-item__action-btn gallery-item__action-btn--view"
              onClick={() => setShowPromptModal(true)}
              title="프롬프트 보기"
            >
              👁️
            </button>
            {canDelete && (
              <button 
                className="gallery-item__action-btn gallery-item__action-btn--delete"
                onClick={() => setShowDeleteConfirm(true)}
                title="삭제"
                disabled={isDeleting}
              >
                🗑️
              </button>
            )}
          </div>
        </div>
        
        <div className="gallery-item__content">
          {item.title && (
            <h3 className="gallery-item__title">{item.title}</h3>
          )}
          
          <p className="gallery-item__prompt">
            {item.prompt.length > 100 
              ? `${item.prompt.substring(0, 100)}...` 
              : item.prompt
            }
          </p>
          
          <div className="gallery-item__meta">
            <div className="gallery-item__author">
              <span className="gallery-item__author-name">{item.user_name}</span>
              <span className="gallery-item__author-type">
                {getUserTypeLabel(item.user_type)}
              </span>
            </div>
            <time className="gallery-item__date">
              {formatDate(item.created_at)}
            </time>
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="gallery-modal-overlay" onClick={() => setShowDeleteConfirm(false)}>
          <div className="gallery-modal gallery-modal--small" onClick={(e) => e.stopPropagation()}>
            <h3>작품 삭제</h3>
            <p>정말로 이 작품을 삭제하시겠습니까?</p>
            <p className="gallery-modal__warning">삭제된 작품은 복구할 수 없습니다.</p>
            
            <div className="gallery-modal__actions">
              <button 
                onClick={() => setShowDeleteConfirm(false)}
                className="gallery-btn gallery-btn--secondary"
                disabled={isDeleting}
              >
                취소
              </button>
              <button 
                onClick={handleDelete}
                className="gallery-btn gallery-btn--danger"
                disabled={isDeleting}
              >
                {isDeleting ? '삭제 중...' : '삭제'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Prompt Detail Modal */}
      {showPromptModal && (
        <div className="gallery-modal-overlay" onClick={() => setShowPromptModal(false)}>
          <div className="gallery-modal" onClick={(e) => e.stopPropagation()}>
            <div className="gallery-modal__header">
              <h3>{item.title || '작품 상세'}</h3>
              <button 
                className="gallery-modal__close"
                onClick={() => setShowPromptModal(false)}
              >
                ×
              </button>
            </div>
            
            <div className="gallery-modal__content">
              <div className="gallery-modal__image">
                <img src={item.image_url} alt={item.title || item.prompt} />
              </div>
              
              <div className="gallery-modal__details">
                <div className="gallery-modal__section">
                  <h4>프롬프트</h4>
                  <p className="gallery-modal__prompt">{item.prompt}</p>
                </div>
                
                <div className="gallery-modal__section">
                  <h4>작품 정보</h4>
                  <div className="gallery-modal__info">
                    <div className="gallery-modal__info-item">
                      <span className="gallery-modal__info-label">작성자:</span>
                      <span>{item.user_name} ({getUserTypeLabel(item.user_type)})</span>
                    </div>
                    <div className="gallery-modal__info-item">
                      <span className="gallery-modal__info-label">생성일:</span>
                      <span>{formatDate(item.created_at)}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="gallery-modal__actions">
              <button 
                onClick={() => setShowPromptModal(false)}
                className="gallery-btn gallery-btn--primary"
              >
                닫기
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default GalleryItem;