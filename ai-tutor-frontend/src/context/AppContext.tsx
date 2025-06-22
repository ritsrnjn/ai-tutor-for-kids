import React, { createContext, useContext, useReducer, useEffect, ReactNode, useRef } from 'react';
import io, { Socket } from 'socket.io-client';
import { AppState, VoiceState, AvatarState, AppContextType } from '../types';

// Action types
type AppAction =
  | { type: 'SET_LISTENING'; payload: boolean }
  | { type: 'SET_CONNECTED'; payload: boolean }
  | { type: 'SET_TOPIC'; payload: string }
  | { type: 'SET_AI_RESPONSE'; payload: string }
  | { type: 'SET_USER_TRANSCRIPT'; payload: string }
  | { type: 'SET_IMAGE'; payload: { url: string; word: string } }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_VOICE_STATE'; payload: Partial<VoiceState> }
  | { type: 'SET_AVATAR_STATE'; payload: Partial<AvatarState> };

// Initial states
const initialAppState: AppState = {
  isListening: false,
  isConnected: false,
  currentTopic: null,
  aiResponse: null,
  userTranscript: null,
  imageUrl: null,
  highlightWord: null,
  isLoading: false,
  error: null,
};

const initialVoiceState: VoiceState = {
  isListening: false,
  isProcessing: false,
  volume: 0,
  status: 'idle',
};

const initialAvatarState: AvatarState = {
  isSpeaking: false,
  emotion: 'neutral',
  animation: 'idle',
};

// Reducer
function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_LISTENING':
      return { ...state, isListening: action.payload };
    case 'SET_CONNECTED':
      return { ...state, isConnected: action.payload };
    case 'SET_TOPIC':
      return { ...state, currentTopic: action.payload };
    case 'SET_AI_RESPONSE':
      return { ...state, aiResponse: action.payload };
    case 'SET_USER_TRANSCRIPT':
      return { ...state, userTranscript: action.payload };
    case 'SET_IMAGE':
      return {
        ...state,
        imageUrl: action.payload.url,
        highlightWord: action.payload.word
      };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    default:
      return state;
  }
}

// Context will use the imported AppContextType from types

const AppContext = createContext<AppContextType | undefined>(undefined);

// Provider component
interface AppProviderProps {
  children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  const [appState, dispatch] = useReducer(appReducer, initialAppState);
  const [voiceState, setVoiceStateLocal] = React.useState<VoiceState>(initialVoiceState);
  const [avatarState, setAvatarStateLocal] = React.useState<AvatarState>(initialAvatarState);
  const [socket, setSocket] = React.useState<Socket | null>(null);
  const socketRef = useRef<Socket | null>(socket);

  // Initialize WebSocket connection
  useEffect(() => {
    const newSocket = io('http://localhost:5001');
    setSocket(newSocket);
    socketRef.current = newSocket;

    newSocket.on('connect', () => {
      dispatch({ type: 'SET_CONNECTED', payload: true });
      console.log('Connected to server');
    });

    newSocket.on('disconnect', () => {
      dispatch({ type: 'SET_CONNECTED', payload: false });
      console.log('Disconnected from server');
    });

    newSocket.on('agent_response', (data: { response: string }) => {
      dispatch({ type: 'SET_AI_RESPONSE', payload: data.response });
      setAvatarStateLocal(prev => ({ ...prev, isSpeaking: true, animation: 'talking' }));
    });

    newSocket.on('user_transcript', (data: { transcript: string }) => {
      dispatch({ type: 'SET_USER_TRANSCRIPT', payload: data.transcript });
    });

    newSocket.on('error', (data: { error: string }) => {
      dispatch({ type: 'SET_ERROR', payload: data.error });
    });

    return () => {
      newSocket.close();
    };
  }, []);

  // Helper functions
  const setVoiceState = (state: Partial<VoiceState>) => {
    setVoiceStateLocal(prev => ({ ...prev, ...state }));
  };

  const setAvatarState = (state: Partial<AvatarState>) => {
    setAvatarStateLocal(prev => ({ ...prev, ...state }));
  };

  const startListening = () => {
    dispatch({ type: 'SET_LISTENING', payload: true });
    setVoiceState({ isListening: true, status: 'listening' });
    setAvatarState({ emotion: 'excited', animation: 'gesturing' });

    if (socket) {
      socket.emit('start_conversation', { topic: appState.currentTopic });
    }
  };

  const stopListening = () => {
    dispatch({ type: 'SET_LISTENING', payload: false });
    setVoiceState({ isListening: false, status: 'idle' });
    setAvatarState({ emotion: 'neutral', animation: 'idle' });

    if (socket) {
      socket.emit('end_conversation');
    }
  };

  const setTopic = async (topic: string) => {
    dispatch({ type: 'SET_TOPIC', payload: topic });
    dispatch({ type: 'SET_LOADING', payload: true });

    try {
      const response = await fetch('http://localhost:5001/set_topic', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic }),
      });

      if (!response.ok) throw new Error('Failed to set topic');

      const data = await response.json();
      console.log('Topic set successfully:', data);
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: 'Failed to set topic' });
      console.error('Error setting topic:', error);
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const createImage = async (response: string) => {
    try {
      const result = await fetch('http://localhost:5001/create_image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ response }),
      });

      if (!result.ok) throw new Error('Failed to create image');

      const data = await result.json();
      dispatch({
        type: 'SET_IMAGE',
        payload: { url: data.image_url, word: data.highlight_word }
      });
    } catch (error) {
      console.error('Error creating image:', error);
    }
  };

  const contextValue: AppContextType = {
    appState,
    voiceState,
    avatarState,
    socket,
    socketRef,
    dispatch,
    setVoiceState,
    setAvatarState,
    startListening,
    stopListening,
    setTopic,
    createImage,
  };

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};

// Custom hook
export const useApp = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
