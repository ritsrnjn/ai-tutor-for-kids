import React from 'react';
import { AppProvider } from './context/AppContext';
import VoiceTrigger from './components/VoiceTrigger';
import VoiceOrb from './components/VoiceOrb';
import ImageDisplay from './components/ImageDisplay';
import './App.css';

const App: React.FC = () => {
  return (
    <AppProvider>
      <div className="App">
        <header className="App-header">
          <h1>Nani ki kahani unhi ki zubani</h1>
          <p>Interactive Learning with Voice & Images</p>
        </header>

        <main className="App-main">
          <div className="learning-container">
            {/* Voice Interface */}
            <div className="voice-section">
              <VoiceTrigger />
            </div>

            {/* Voice Orb - The main visual element */}
            <div className="orb-section">
              <VoiceOrb />
            </div>

            {/* Image Display */}
            <div className="image-section">
              <ImageDisplay />
            </div>
          </div>
        </main>
      </div>
    </AppProvider>
  );
};

export default App;
