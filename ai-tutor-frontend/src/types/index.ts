import { Socket } from 'socket.io-client';

export interface AppState {
  isListening: boolean;
  isConnected: boolean;
  currentTopic: string | null;
  aiResponse: string | null;
  userTranscript: string | null;
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

export interface ImageState {
  imageUrl: string | null;
  englishWord: string | null;
  hindiWord: string | null;
}

export interface ConversationMessage {
  id: string;
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

export interface LearningSession {
  id: string;
  topic: string;
  startTime: Date;
  messages: ConversationMessage[];
  progress: number;
}

export interface AppContextType {
  appState: AppState;
  voiceState: VoiceState;
  avatarState: AvatarState;
  imageState: ImageState;
  socket: Socket | null;
  socketRef: React.RefObject<Socket | null>;
  dispatch: React.Dispatch<any>;
  setVoiceState: (state: Partial<VoiceState>) => void;
  setAvatarState: (state: Partial<AvatarState>) => void;
  setImageState: (state: Partial<ImageState>) => void;
  startListening: () => void;
  stopListening: () => void;
  setTopic: (topic: string) => Promise<void>;
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
