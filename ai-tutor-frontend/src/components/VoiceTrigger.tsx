import React, { useEffect, useState, useRef } from 'react';
import { useApp } from '../context/AppContext';
import './VoiceTrigger.css';

const VoiceTrigger: React.FC = () => {
  const {
    appState,
    voiceState,
    setTopic,
    startListening,
    stopListening,
    socketRef
  } = useApp();

  const [showTopicSelection, setShowTopicSelection] = useState(!appState.currentTopic);
  const [isRecording, setIsRecording] = useState(false);
  const [conversationStarted, setConversationStarted] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // Topic options
  const topicOptions = [
    { id: 'animals', label: 'Animals', emoji: '🐾', description: 'Learn about different animals' },
    { id: 'plants', label: 'Plants', emoji: '🌱', description: 'Discover the world of plants' },
    { id: 'planets', label: 'Planets', emoji: '🪐', description: 'Explore our solar system' },
    { id: 'states', label: 'States', emoji: '🗺️', description: 'Learn about Indian states' },
    { id: 'colors', label: 'Colors', emoji: '🎨', description: 'Learn different colors' },
    { id: 'numbers', label: 'Numbers', emoji: '🔢', description: 'Practice counting and numbers' },
    { id: 'food', label: 'Food', emoji: '🍽️', description: 'Learn about different foods' },
    { id: 'family', label: 'Family', emoji: '👨‍👩‍👧‍👦', description: 'Family relationships and members' },
    { id: 'body-parts', label: 'Body Parts', emoji: '👤', description: 'Learn about body parts' }
  ];

  // Handle topic selection
  const handleTopicSelect = (topic: string) => {
    setTopic(topic);
    setShowTopicSelection(false);
  };

  const handleTopicChange = () => {
    setShowTopicSelection(true);
    setConversationStarted(false);
  };

  // Start conversation with backend
  const handleStartConversation = async () => {
    try {
      const response = await fetch('http://localhost:5001/start_session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: appState.currentTopic }),
      });

      const result = await response.json();
      if (result.success) {
        setConversationStarted(true);
        console.log('Conversation started successfully:', result);

        // Start listening for audio
        startAudioRecording();
      } else {
        console.error('Failed to start conversation:', result);
      }
    } catch (error) {
      console.error('Error starting conversation:', error);
    }
  };

  // Stop conversation with backend
  const handleStopConversation = async () => {
    try {
      stopAudioRecording();

      const response = await fetch('http://localhost:5001/end_session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });

      const result = await response.json();
      setConversationStarted(false);
      console.log('Conversation ended:', result);
    } catch (error) {
      console.error('Error ending conversation:', error);
    }
  };

  // Audio recording functions
  const startAudioRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        sendAudioToBackend(audioBlob);
        audioChunksRef.current = [];
      };

      // Record in chunks of 3 seconds
      mediaRecorder.start();
      setIsRecording(true);

      // Stop and restart recording every 3 seconds for continuous audio
      const recordingInterval = setInterval(() => {
        if (mediaRecorder.state === 'recording') {
          mediaRecorder.stop();
          setTimeout(() => {
            if (conversationStarted && mediaRecorder.state === 'inactive') {
              audioChunksRef.current = [];
              mediaRecorder.start();
            }
          }, 100);
        }
      }, 3000);

      // Store interval for cleanup
      (mediaRecorder as any).recordingInterval = recordingInterval;

    } catch (error) {
      console.error('Error starting audio recording:', error);
    }
  };

  const stopAudioRecording = () => {
    if (mediaRecorderRef.current) {
      const mediaRecorder = mediaRecorderRef.current;

      // Clear interval
      if ((mediaRecorder as any).recordingInterval) {
        clearInterval((mediaRecorder as any).recordingInterval);
      }

      if (mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
      }

      // Stop all tracks
      mediaRecorder.stream?.getTracks().forEach(track => track.stop());
    }
    setIsRecording(false);
  };

  const sendAudioToBackend = async (audioBlob: Blob) => {
    try {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64Audio = reader.result as string;
        const audioData = base64Audio.split(',')[1]; // Remove data:audio/wav;base64, prefix

        if (socketRef.current?.connected) {
          socketRef.current.emit('audio_chunk', { audio: audioData });
        }
      };
      reader.readAsDataURL(audioBlob);
    } catch (error) {
      console.error('Error sending audio to backend:', error);
    }
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopAudioRecording();
    };
  }, []);

  return (
    <div className="voice-trigger-container">
      {/* Topic Selection */}
      {showTopicSelection ? (
        <div className="topic-section">
          <h3>Choose a Topic</h3>
          <div className="topic-buttons-grid">
            {topicOptions.map((topic) => (
              <button
                key={topic.id}
                onClick={() => handleTopicSelect(topic.label)}
                className="topic-button"
                title={topic.description}
              >
                <div className="topic-emoji">{topic.emoji}</div>
                <div className="topic-label">{topic.label}</div>
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className="conversation-controls">
          <div className="topic-display">
            <h3>Learning about: {appState.currentTopic}</h3>
          </div>

          {!conversationStarted ? (
            <button
              onClick={handleStartConversation}
              className="start-conversation-btn"
              disabled={!appState.currentTopic}
            >
              🎤 Start Conversation with Nani
            </button>
          ) : (
            <div className="conversation-active">
              <div className="recording-indicator">
                <div className={`recording-dot ${isRecording ? 'active' : ''}`}></div>
                <span>Conversation Active</span>
              </div>
              <button
                onClick={handleStopConversation}
                className="stop-conversation-btn"
              >
                🛑 End Conversation
              </button>
            </div>
          )}

          <button
            onClick={handleTopicChange}
            className="change-topic-btn"
          >
            ⚙️ Change Topic
          </button>
        </div>
      )}
    </div>
  );
};

export default VoiceTrigger;
