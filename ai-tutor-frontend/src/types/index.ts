export interface AppState {
  isListening: boolean;
  isConnected: boolean;
  currentTopic: string | null;
  aiResponse: string | null;
  userTranscript: string | null;
  imageUrl: string | null;
  highlightWord: string | null;
  isLoading: boolean;
  error: string | null;
}

export interface VoiceState {
  isListening: boolean;
  isProcessing: boolean;
  volume: number;
  status: 'idle' | 'listening' | 'processing' | 'speaking';
}

export interface AvatarState {
  isSpeaking: boolean;
  emotion: 'happy' | 'excited' | 'thinking' | 'neutral';
  animation: 'idle' | 'talking' | 'gesturing' | 'celebrating';
}

export interface ConversationMessage {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
  imageUrl?: string;
  highlightWord?: string;
}

export interface LearningSession {
  id: string;
  topic: string;
  startTime: Date;
  messages: ConversationMessage[];
  progress: number;
}

export interface AppContextType {
  // State
  appState: AppState;
  voiceState: VoiceState;
  avatarState: AvatarState;
  socket: any | null;
  socketRef: React.RefObject<any>;

  // Actions
  dispatch: React.Dispatch<any>;
  setVoiceState: (state: Partial<VoiceState>) => void;
  setAvatarState: (state: Partial<AvatarState>) => void;

  // Methods
  startListening: () => void;
  stopListening: () => void;
  setTopic: (topic: string) => void;
  createImage: (response: string) => void;
}

// Declare ElevenLabs ConvAI custom element
declare global {
  namespace JSX {
    interface IntrinsicElements {
      'elevenlabs-convai': {
        'agent-id': string;
        className?: string;
        ref?: React.Ref<HTMLElement>;
      };
    }
  }
}
