import { useState, useEffect } from 'react';
import { useAuth } from './AuthContext';
import GalleryUploadModal from './components/Gallery/GalleryUploadModal';
import GalleryItem from './components/Gallery/GalleryItem';
import Masonry from './components/Gallery/Masonry';
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
          method: 'DELETE',
        }
      );

      const data = await response.json();

      if (response.ok && data.success) {
        // Remove the item from the list
        setGalleryItems(prev => prev.filter(galleryItem => galleryItem.id !== item.originalItem.id));
        // Refresh stats
        fetchStats();
        alert('작품이 삭제되었습니다.');
      } else {
        throw new Error(data.detail || data.error || '삭제에 실패했습니다.');
      }
    } catch (error) {
      console.error('Delete error:', error);
      alert(`삭제 실패: ${error.message}`);
    }
  };

  const handleItemView = (item) => {
    setSelectedItem(item.originalItem);
    setShowDetailModal(true);
  };

  const handleItemClick = (item) => {
    handleItemView(item);
  };

  useEffect(() => {
    fetchGalleryItems();
    fetchStats();
  }, [sessionId, user]);

  if (!sessionId) {
    return (
      <div className="gallery-main">
        <div className="gallery-header">
          <h1>AI 창작 갤러리</h1>
          <div className="gallery-no-session">
            <div className="gallery-no-session__icon">🎨</div>
            <p>갤러리를 이용하려면 클래스 세션에 참여해주세요.</p>
            <small>선생님이 제공한 클래스 코드로 로그인하거나, 선생님이 새로운 클래스를 생성해주세요.</small>
          </div>
        </div>
      </div>
    );
  }

  if (loading && galleryItems.length === 0) {
    return (
      <div className="gallery-main">
        <div className="gallery-header">
          <h1>AI 창작 갤러리</h1>
          <div className="gallery-loading">
            <div className="gallery-loading__spinner"></div>
            <p>갤러리를 불러오는 중...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="gallery-main">
        <div className="gallery-header">
          <h1>AI 창작 갤러리</h1>
          <div className="gallery-error">
            <div className="gallery-error__icon">⚠️</div>
            <p>갤러리를 불러오는데 문제가 발생했습니다.</p>
            <small>{error}</small>
            <button 
              onClick={fetchGalleryItems}
              className="gallery-retry-btn"
            >
              다시 시도
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="gallery-main">
      <div className="gallery-header">
        <div className="gallery-header__content">
          <div className="gallery-header__text">
            <h1>AI 창작 갤러리</h1>
            <p>학생과 선생님들이 AI로 만든 멋진 이미지들을 감상하고, 프롬프트를 공유해보세요.</p>
          </div>
          <div className="gallery-header__actions">
            <button 
              onClick={() => setShowUploadModal(true)}
              className="gallery-upload-btn"
            >
              <span className="gallery-upload-btn__icon">📤</span>
              작품 업로드
            </button>
          </div>
        </div>

        {sessionInfo && (
          <div className="gallery-session-info">
            <div className="gallery-session-info__main">
              <span className="gallery-session-info__label">현재 클래스:</span>
              <span className="gallery-session-info__code">{sessionInfo.class_code}</span>
            </div>
            {stats && (
              <div className="gallery-session-stats">
                <div className="gallery-stat">
                  <span className="gallery-stat__value">{stats.total_items}</span>
                  <span className="gallery-stat__label">총 작품</span>
                </div>
                <div className="gallery-stat">
                  <span className="gallery-stat__value">{stats.student_items}</span>
                  <span className="gallery-stat__label">학생 작품</span>
                </div>
                <div className="gallery-stat">
                  <span className="gallery-stat__value">{stats.teacher_items}</span>
                  <span className="gallery-stat__label">선생님 작품</span>
                </div>
                <div className="gallery-stat">
                  <span className="gallery-stat__value">{stats.unique_contributors}</span>
                  <span className="gallery-stat__label">참여자</span>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="gallery-container">
        {galleryItems.length === 0 ? (
          <div className="gallery-empty">
            <div className="gallery-empty__icon">🎨</div>
            <h3>아직 업로드된 작품이 없습니다</h3>
            <p>첫 번째 작품을 업로드해보세요!</p>
            <button 
              onClick={() => setShowUploadModal(true)}
              className="gallery-upload-btn gallery-upload-btn--large"
            >
              <span className="gallery-upload-btn__icon">📤</span>
              작품 업로드하기
            </button>
          </div>
        ) : (
          <Masonry
            items={convertToMasonryItems(galleryItems)}
            ease="power3.out"
            duration={0.6}
            stagger={0.05}
            animateFrom="bottom"
            scaleOnHover={true}
            hoverScale={1.02}
            blurToFocus={true}
            colorShiftOnHover={false}
            onItemClick={handleItemClick}
            onItemView={handleItemView}
            onItemDelete={handleItemDelete}
            user={user}
          />
        )}
      </div>

      <GalleryUploadModal
        isOpen={showUploadModal}
        onClose={() => setShowUploadModal(false)}
        sessionId={sessionId}
        onUploadSuccess={handleUploadSuccess}
      />

      {selectedItem && (
        <GalleryItem
          isModal={true}
          isOpen={showDetailModal}
          item={selectedItem}
          onClose={() => {
            setShowDetailModal(false);
            setSelectedItem(null);
          }}
          onDelete={(itemId) => {
            // Close modal first
            setShowDetailModal(false);
            setSelectedItem(null);
            // Remove item from list
            setGalleryItems(prev => prev.filter(item => item.id !== itemId));
            // Refresh stats
            fetchStats();
          }}
        />
      )}
    </div>
  );
}

export default Gallery;
