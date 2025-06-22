import React from 'react';
import { useApp } from '../context/AppContext';
import './VoiceOrb.css';

const VoiceOrb: React.FC = () => {
  const { appState, voiceState, avatarState } = useApp();

  const getOrbState = () => {
    if (appState.isListening) return 'listening';
    if (avatarState.isSpeaking) return 'speaking';
    if (appState.isConnected) return 'connected';
    return 'idle';
  };

  const orbState = getOrbState();

  return (
    <div className="voice-orb-container">
      <div className={`voice-orb ${orbState}`}>
        {/* Main orb */}
        <div className="orb-core"></div>

        {/* Animated rings */}
        <div className="orb-ring ring-1"></div>
        <div className="orb-ring ring-2"></div>
        <div className="orb-ring ring-3"></div>

        {/* Energy particles */}
        <div className="energy-particles">
          {[...Array(12)].map((_, i) => (
            <div key={i} className={`particle particle-${i + 1}`}></div>
          ))}
        </div>

        {/* Glow effect */}
        <div className="orb-glow"></div>
      </div>

      {/* Status text */}
      <div className="orb-status">
        {orbState === 'listening' && 'Listening...'}
        {orbState === 'speaking' && 'Nani is speaking...'}
        {orbState === 'connected' && 'Ready to chat'}
        {orbState === 'idle' && 'Offline'}
      </div>
    </div>
  );
};

export default VoiceOrb;
