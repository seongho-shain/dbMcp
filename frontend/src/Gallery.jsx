import React from 'react';
import Masonry from './components/Masonry';
import './Gallery.css';

// 가상 데이터 (추후 API로 대체)
const galleryItems = [
  {
    id: "1",
    img: 'https://via.placeholder.com/600x450.png/A7C7E7/FFFFFF?text=Galaxy+Cat',
    prompt: 'A cat floating in a vibrant galaxy, surrounded by stars and nebulae, digital art.',
    author: 'Student123',
    height: 450,
    url: "#",
  },
  {
    id: "2",
    img: 'https://via.placeholder.com/600x350.png/C1E1C1/FFFFFF?text=Future+City',
    prompt: 'A futuristic city with flying cars and holographic billboards, neon-punk style.',
    author: 'TeacherA',
    height: 350,
    url: "#",
  },
  {
    id: "3",
    img: 'https://via.placeholder.com/600x550.png/F5D2D3/FFFFFF?text=Enchanted+Forest',
    prompt: 'An enchanted forest with glowing mushrooms and ancient trees, fantasy art.',
    author: 'Student456',
    height: 550,
    url: "#",
  },
  {
    id: "4",
    img: 'https://via.placeholder.com/600x400.png/AEC6CF/FFFFFF?text=Ocean+Lighthouse',
    prompt: 'Lighthouse on a cliff overlooking a stormy ocean, oil painting style.',
    author: 'TeacherB',
    height: 400,
    url: "#",
  },
  {
    id: "5",
    img: 'https://via.placeholder.com/600x480.png/B39EB5/FFFFFF?text=Robot+Companion',
    prompt: 'A friendly robot companion helping a child with homework, 3d-model style.',
    author: 'Student789',
    height: 480,
    url: "#",
  },
  {
    id: "6",
    img: 'https://via.placeholder.com/600x380.png/FFDAB9/FFFFFF?text=Desert+Oasis',
    prompt: 'A hidden oasis in a vast desert at sunset, photographic style.',
    author: 'TeacherC',
    height: 380,
    url: "#",
  },
];

function Gallery() {
  return (
    <div className="gallery-main">
      <div className="gallery-header">
        <h1>AI 창작 갤러리</h1>
        <p>학생과 선생님들이 AI로 만든 멋진 이미지들을 감상하고, 프롬프트를 공유해보세요.</p>
      </div>
      <div className="gallery-container">
        <Masonry
          items={galleryItems}
          ease="power3.out"
          duration={0.6}
          stagger={0.05}
          animateFrom="bottom"
          scaleOnHover={true}
          hoverScale={0.95}
          blurToFocus={true}
          colorShiftOnHover={false}
        />
      </div>
    </div>
  );
}

export default Gallery;
