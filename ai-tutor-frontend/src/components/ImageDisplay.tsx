import React, { useEffect, useState } from 'react';
import { useApp } from '../context/AppContext';
import './ImageDisplay.css';

const ImageDisplay: React.FC = () => {
  const { appState, avatarState } = useApp();
  const [isVisible, setIsVisible] = useState(false);
  const [animationClass, setAnimationClass] = useState('');

  useEffect(() => {
    if (appState.imageUrl && appState.highlightWord) {
      setIsVisible(true);
      setAnimationClass('bounce-in');

      // Reset animation class after animation completes
      setTimeout(() => {
        setAnimationClass('');
      }, 800);
    } else {
      setIsVisible(false);
    }
  }, [appState.imageUrl, appState.highlightWord]);

  const handleSpeakWord = () => {
    if (appState.highlightWord && 'speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(appState.highlightWord);
      utterance.rate = 0.8;
      utterance.pitch = 1.2;
      utterance.volume = 0.8;

      // Try to use a female voice if available
      const voices = speechSynthesis.getVoices();
      const femaleVoice = voices.find(voice =>
        voice.name.toLowerCase().includes('female') ||
        voice.name.toLowerCase().includes('zira') ||
        voice.name.toLowerCase().includes('hazel')
      );
      if (femaleVoice) {
        utterance.voice = femaleVoice;
      }

      speechSynthesis.speak(utterance);
    }
  };

  const renderSparkles = () => {
    const sparkles = ['✨', '⭐', '🌟', '💫'];
    return (
      <div className="image-sparkles">
        {sparkles.map((sparkle, index) => (
          <span key={index} className="sparkle" style={{ animationDelay: `${index * 0.2}s` }}>
            {sparkle}
          </span>
        ))}
      </div>
    );
  };

  if (!isVisible || !appState.imageUrl || !appState.highlightWord) {
    return (
      <div className="image-display-placeholder">
        <div className="placeholder-content">
          <div className="placeholder-icon">🖼️</div>
          <p>Images will appear here when you start talking!</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`image-display-container ${animationClass}`}>
      <div className="image-display-content">
        {/* Bouncy Header */}
        <div className="bouncy-header">
          <h3>Look what I found!</h3>
        </div>

        {/* Image Wrapper */}
        <div className="image-wrapper">
          <div className="image-frame">
            <img
              src={appState.imageUrl}
              alt="Generated visual"
              className="generated-image"
              onError={(e) => {
                console.error('Failed to load image:', appState.imageUrl);
                e.currentTarget.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjgwIiBoZWlnaHQ9IjI4MCIgdmlld0JveD0iMCAwIDI4MCAyODAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyODAiIGhlaWdodD0iMjgwIiBmaWxsPSIjRjBGMEYwIi8+Cjx0ZXh0IHg9IjE0MCIgeT0iMTUwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjOTk5IiBmb250LXNpemU9IjE0Ij5JbWFnZSBub3QgZm91bmQ8L3RleHQ+Cjwvc3ZnPg==';
              }}
            />
            {renderSparkles()}
          </div>
        </div>

        {/* Word Display */}
        <div className="word-display">
          <div className="word-bubble">
            <span className="featured-word">
              {appState.highlightWord}
            </span>
            <button
              className="speak-button"
              onClick={handleSpeakWord}
              title="Click to hear pronunciation"
            >
              🔊
            </button>
          </div>
        </div>

        {/* Fun Actions */}
        <div className="fun-actions">
          <button
            className="action-button celebrate"
            onClick={() => {
              setAnimationClass('wiggle');
              setTimeout(() => setAnimationClass(''), 1000);
            }}
          >
            🎉 Celebrate!
          </button>
          <button
            className="action-button speak"
            onClick={handleSpeakWord}
          >
            🗣️ Say it!
          </button>
        </div>

        {/* AI Response Context */}
        {appState.aiResponse && (
          <div className="ai-context">
            <div className="context-bubble">
              <p>"{appState.aiResponse.substring(0, 100)}..."</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageDisplay;
