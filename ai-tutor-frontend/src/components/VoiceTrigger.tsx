import React, { useEffect, useState, useRef } from 'react';
import { useApp } from '../context/AppContext';
import './VoiceTrigger.css';

// Declare ElevenLabs types to avoid TypeScript errors
declare global {
  interface Window {
    ElevenLabsConvAI?: any;
  }
}

const VoiceTrigger: React.FC = () => {
  const {
    appState,
    setTopic,
    socketRef
  } = useApp();

  const [topicInput, setTopicInput] = useState('');
  const [showTopicInput, setShowTopicInput] = useState(!appState.currentTopic);
  const [widgetLoaded, setWidgetLoaded] = useState(false);

  // Load ElevenLabs ConvAI script (matching the working HTML implementation)
  useEffect(() => {
    const loadElevenLabsScript = () => {
      // Check if script already exists
      if (document.querySelector('script[src*="convai-widget-embed"]')) {
        console.log('ElevenLabs script already loaded');
        setWidgetLoaded(true);
        return;
      }

      console.log('Loading ElevenLabs ConvAI script...');
      const script = document.createElement('script');
      script.src = 'https://unpkg.com/@elevenlabs/convai-widget-embed';
      script.async = true;
      script.type = 'text/javascript';
      script.onload = () => {
        console.log('ElevenLabs script loaded successfully');
        setWidgetLoaded(true);
      };
      script.onerror = (error) => {
        console.error('Failed to load ElevenLabs ConvAI script:', error);
        setWidgetLoaded(true); // Still show the widget container
      };

      document.head.appendChild(script);
    };

    loadElevenLabsScript();
  }, []);

  // Handle topic submission
  const handleTopicSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (topicInput.trim()) {
      setTopic(topicInput.trim());
      setShowTopicInput(false);

      // Send topic to backend via WebSocket
      if (socketRef.current?.connected) {
        socketRef.current.emit('topic_selected', { topic: topicInput.trim() });
      }
    }
  };

  const handleTopicChange = () => {
    setShowTopicInput(true);
    setTopicInput('');
  };

  // Add keyboard shortcut to change topic (Ctrl+T or Cmd+T)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 't' && !showTopicInput) {
        e.preventDefault();
        handleTopicChange();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [showTopicInput]);

    // Optional: Handle ConvAI events (can be added later if needed)
  useEffect(() => {
    if (!widgetLoaded) return;

    console.log('ElevenLabs ConvAI widget should be loaded and ready');

    // The widget will handle all voice interactions automatically
    // No manual event handling needed for basic functionality
  }, [widgetLoaded]);

  return (
    <div className="voice-trigger-container">
      {/* Topic Selection */}
      {showTopicInput ? (
        <div className="topic-section">
          <h3>Choose a Topic</h3>
          <form onSubmit={handleTopicSubmit} className="topic-form">
            <input
              type="text"
              value={topicInput}
              onChange={(e) => setTopicInput(e.target.value)}
              placeholder="Enter a topic (e.g., Colors, Animals, Numbers)"
              className="topic-input"
              autoFocus
            />
            <button type="submit" className="topic-submit">
              Start Learning
            </button>
          </form>
        </div>
      ) : (
        <div className="widget-container">
          <elevenlabs-convai
            agent-id="agent_01jy9sz4gnew0vedv885xsrse1"
          ></elevenlabs-convai>
          <button
            onClick={handleTopicChange}
            className="floating-change-topic"
            title="Change Topic (Ctrl+T / Cmd+T)"
          >
            ⚙️
          </button>
        </div>
      )}
    </div>
  );
};

export default VoiceTrigger;
