import React from 'react';
import { useApp } from '../context/AppContext';
import './ImageDisplay.css';

const ImageDisplay: React.FC = () => {
  const { imageState } = useApp();

  if (!imageState.imageUrl) {
    return (
      <div className="image-display-container placeholder">
        <div className="placeholder-content">
          <div className="placeholder-icon">🖼️</div>
          <p>Your generated image will appear here!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="image-display-container">
      <img src={imageState.imageUrl} alt="Generated visual aid" className="generated-image" />
      <div className="word-labels">
        <div className="word-label english">
          <span className="lang">English:</span>
          <span className="word">{imageState.englishWord}</span>
        </div>
        <div className="word-label hindi">
          <span className="lang">Hindi:</span>
          <span className="word">{imageState.hindiWord}</span>
        </div>
      </div>
    </div>
  );
};

export default ImageDisplay;
