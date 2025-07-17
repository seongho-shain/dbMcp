import { useState, useEffect } from 'react';
import { useAuth } from '../../../AuthContext';
import GalleryUploadModal from './GalleryUploadModal';
import GalleryItem from './GalleryItem';
import Masonry from './Masonry';
import './Gallery.css';

const API_BASE_URL = 'http://localhost:8000';

function Gallery({ sessionId, sessionInfo }) {
  const [galleryItems, setGalleryItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showDetailModal, setShowDetailModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [stats, setStats] = useState(null);
  const { user } = useAuth();

  // Convert gallery items to masonry format
  const convertToMasonryItems = (items) => {
    return items.map(item => {
      // Generate random height for masonry effect (between 250-500px)
      const height = Math.floor(Math.random() * (500 - 250 + 1)) + 250;
      
      return {
        id: item.id.toString(),
        img: item.image_url,
        prompt: item.prompt,
        title: item.title || 'AI 생성 이미지',
        user_name: item.user_name,
        user_type: item.user_type,
        user_id: item.user_id,
        created_at: item.created_at,
        height: height,
        url: "#",
        originalItem: item
      };
    });
  };

  const fetchGalleryItems = async () => {
    if (!sessionId || !user) return;

    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/gallery/session/${sessionId}?user_id=${user.id}&user_type=${user.user_type}`
      );

      const data = await response.json();

      if (response.ok && data.success) {
        setGalleryItems(data.items || []);
      } else {
        throw new Error(data.detail || data.error || '갤러리를 불러오는데 실패했습니다.');
      }
    } catch (error) {
      console.error('Gallery fetch error:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    if (!sessionId || !user) return;

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/gallery/session/${sessionId}/stats?user_id=${user.id}&user_type=${user.user_type}`
      );

      const data = await response.json();

      if (response.ok && data.success) {
        setStats(data.stats);
      }
    } catch (error) {
      console.error('Stats fetch error:', error);
    }
  };

  const handleUploadSuccess = (newItem) => {
    // Add the new item to the beginning of the list
    setGalleryItems(prev => [newItem, ...prev]);
    // Refresh stats
    fetchStats();
  };

  const handleItemDelete = async (item) => {
    if (!confirm('정말로 이 작품을 삭제하시겠습니까?')) {
      return;
    }

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/gallery/${item.originalItem.id}?user_id=${user.id}&user_type=${user.user_type}`,
        {
          method: 'DELETE'
        }
      );

      const data = await response.json();

      if (response.ok && data.success) {
        // Remove the item from the list
        setGalleryItems(prev => prev.filter(galleryItem => galleryItem.id !== item.originalItem.id));
        alert('작품이 삭제되었습니다.');
        fetchStats();
      } else {
        throw new Error(data.detail || data.error || '작품 삭제에 실패했습니다.');
      }
    } catch (error) {
      console.error('Delete error:', error);
      alert(`삭제 실패: ${error.message}`);
    }
  };

  const handleItemClick = (item) => {
    setSelectedItem(item);
    setShowDetailModal(true);
  };

  const handleItemView = (item) => {
    setSelectedItem(item);
    setShowDetailModal(true);
  };

  useEffect(() => {
    fetchGalleryItems();
    fetchStats();
  }, [sessionId, user]);

  if (!sessionId || !sessionInfo) {
    return (
      <div className="recommend-dashboard__no-session">
        <h3>세션을 선택해주세요</h3>
        <p>갤러리를 보려면 세션을 선택해주세요.</p>
      </div>
    );
  }

  return (
    <div className="recommend-gallery__main">
      <div className="recommend-gallery__header">
        <div className="recommend-gallery__title">
          <h2>🖼️ 갤러리</h2>
          <div className="recommend-gallery__info">
            <span className="recommend-badge">클래스: {sessionInfo.class_code}</span>
            <span className="recommend-badge">세션 ID: {sessionInfo.id}</span>
          </div>
        </div>
        <div className="recommend-gallery__actions">
          <button 
            className="recommend-btn recommend-btn--primary"
            onClick={() => setShowUploadModal(true)}
          >
            📷 작품 업로드
          </button>
          <button 
            className="recommend-btn recommend-btn--secondary"
            onClick={() => { fetchGalleryItems(); fetchStats(); }}
            disabled={loading}
          >
            🔄 새로고침
          </button>
        </div>
      </div>

      {stats && (
        <div className="recommend-gallery__stats">
          <div className="recommend-stats-grid">
            <div className="recommend-stat-item">
              <span className="recommend-stat-item__value">{stats.total_items}</span>
              <span className="recommend-stat-item__label">전체 작품</span>
            </div>
            <div className="recommend-stat-item">
              <span className="recommend-stat-item__value">{stats.total_contributors}</span>
              <span className="recommend-stat-item__label">참여자</span>
            </div>
            <div className="recommend-stat-item">
              <span className="recommend-stat-item__value">{stats.my_items}</span>
              <span className="recommend-stat-item__label">내 작품</span>
            </div>
          </div>
        </div>
      )}

      <div className="recommend-gallery__content">
        {loading && (
          <div className="recommend-loading">
            <div className="recommend-loading__spinner"></div>
            <p>갤러리를 불러오는 중...</p>
          </div>
        )}

        {error && (
          <div className="recommend-error">
            <h3>⚠️ 오류 발생</h3>
            <p>{error}</p>
            <button 
              className="recommend-btn recommend-btn--primary"
              onClick={() => { fetchGalleryItems(); fetchStats(); }}
            >
              다시 시도
            </button>
          </div>
        )}

        {!loading && !error && galleryItems.length === 0 && (
          <div className="recommend-empty">
            <div className="recommend-empty__icon">🎨</div>
            <h3>아직 업로드된 작품이 없습니다</h3>
            <p>첫 번째 작품을 업로드해보세요!</p>
            <button 
              className="recommend-btn recommend-btn--primary"
              onClick={() => setShowUploadModal(true)}
            >
              📷 작품 업로드
            </button>
          </div>
        )}

        {!loading && !error && galleryItems.length > 0 && (
          <div className="recommend-gallery__grid">
            <Masonry 
              items={convertToMasonryItems(galleryItems)}
              onItemClick={handleItemClick}
              onItemView={handleItemView}
              onItemDelete={handleItemDelete}
              user={user}
            />
          </div>
        )}
      </div>

      {showUploadModal && (
        <GalleryUploadModal 
          sessionId={sessionId}
          sessionInfo={sessionInfo}
          onClose={() => setShowUploadModal(false)}
          onSuccess={handleUploadSuccess}
        />
      )}

      {showDetailModal && selectedItem && (
        <div className="recommend-modal-overlay" onClick={() => setShowDetailModal(false)}>
          <div className="recommend-modal recommend-modal--large" onClick={e => e.stopPropagation()}>
            <div className="recommend-modal__header">
              <h3>{selectedItem.title}</h3>
              <button 
                className="recommend-modal__close"
                onClick={() => setShowDetailModal(false)}
              >
                ×
              </button>
            </div>
            <div className="recommend-modal__content">
              <div className="recommend-gallery-detail">
                <div className="recommend-gallery-detail__image">
                  <img src={selectedItem.img} alt={selectedItem.title} />
                </div>
                <div className="recommend-gallery-detail__info">
                  <div className="recommend-gallery-detail__meta">
                    <p><strong>작성자:</strong> {selectedItem.user_name} ({selectedItem.user_type === 'teacher' ? '선생님' : '학생'})</p>
                    <p><strong>생성일:</strong> {new Date(selectedItem.created_at).toLocaleString()}</p>
                  </div>
                  {selectedItem.prompt && (
                    <div className="recommend-gallery-detail__prompt">
                      <h4>프롬프트:</h4>
                      <p>{selectedItem.prompt}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
            <div className="recommend-modal__actions">
              <a 
                href={selectedItem.img} 
                download={`${selectedItem.title}.jpg`}
                className="recommend-btn recommend-btn--primary"
              >
                💾 다운로드
              </a>
              {user && (
                (user.user_type === 'teacher' || (user.user_type === 'student' && selectedItem.user_id === user.id)) && (
                  <button 
                    className="recommend-btn recommend-btn--danger"
                    onClick={() => {
                      if (confirm('정말로 이 작품을 삭제하시겠습니까?')) {
                        handleItemDelete(selectedItem);
                        setShowDetailModal(false);
                      }
                    }}
                  >
                    🗑️ 삭제
                  </button>
                )
              )}
              <button 
                className="recommend-btn recommend-btn--secondary"
                onClick={() => setShowDetailModal(false)}
              >
                닫기
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Gallery;