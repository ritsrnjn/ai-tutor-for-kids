import React from 'react';
import { AppProvider } from './context/AppContext';
import VoiceTrigger from './components/VoiceTrigger';
import ImageDisplay from './components/ImageDisplay';
import './App.css';

const App: React.FC = () => {
  return (
    <AppProvider>
      <div className="App">
        <header className="App-header">
          <h1>AI Tutor for Kids</h1>
          <p>Interactive Learning with Voice & Images</p>
        </header>

        <main className="App-main">
          <div className="learning-container">
            {/* Voice Interface */}
            <div className="voice-section">
              <VoiceTrigger />
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
