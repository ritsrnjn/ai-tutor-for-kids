import os
import signal
import threading
import time
from typing import Optional, Callable
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ElevenLabsManager:
    """
    Manages ElevenLabs conversational AI sessions with topic-based agent configuration
    """

    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.agent_id = os.getenv("ELEVENLABS_AGENT_ID", "your_agent_id_here")
        self.client = ElevenLabs(api_key=self.api_key)
        self.conversation: Optional[Conversation] = None
        self.current_topic = None
        self.conversation_id = None
        self.is_session_active = False

        # Callbacks for handling responses
        self.on_agent_response: Optional[Callable] = None
        self.on_user_transcript: Optional[Callable] = None
        self.on_agent_response_correction: Optional[Callable] = None
        self.on_latency_measurement: Optional[Callable] = None
        self.on_session_end: Optional[Callable] = None

    def set_callbacks(self,
                     on_agent_response: Optional[Callable] = None,
                     on_user_transcript: Optional[Callable] = None,
                     on_agent_response_correction: Optional[Callable] = None,
                     on_latency_measurement: Optional[Callable] = None,
                     on_session_end: Optional[Callable] = None):
        """Set callback functions for handling conversation events"""
        self.on_agent_response = on_agent_response
        self.on_user_transcript = on_user_transcript
        self.on_agent_response_correction = on_agent_response_correction
        self.on_latency_measurement = on_latency_measurement
        self.on_session_end = on_session_end

    def get_topic_prompt(self, topic: str) -> str:
        """
        Generate the system prompt for a specific topic, similar to the Sarvam implementation
        """
        return f"""You are Nani, a warm and loving grandmother who is a Hindi language coach for children. You speak primarily in English but your main objective is to teach Hindi vocabulary and culture.

The topic for today's lesson is: {topic}. Please start by greeting the child and introducing the topic, then teach 3-4 HINDI words related to {topic} (with English explanations), and finally tell a mythological story in English that incorporates these Hindi words.

IMPORTANT FORMATTING RULES:
- Keep regular responses SHORT and conversational (2-3 sentences max per response)
- For vocabulary: "The Hindi word for [English word] is [Hindi script] pronounced as [SYL-LA-BLES]"
- Example: "The Hindi word for mountain is पर्वत pronounced as PAR-VAT"
- Example: "The Hindi word for river is नदी pronounced as NA-DI"
- ALWAYS break pronunciation into syllables with hyphens for easier learning
- NEVER write "SHER" (शेर) - always separate English and Hindi properly
- Ask ONE question at a time
- Wait for child's response before continuing
- STORIES should be longer (8-10 sentences) and engaging with good detail

Here's how you should interact:

1. **Warm Greeting**:
   - Short greeting in English like "Namaste beta! Ready to learn Hindi {topic} words?"
   - Introduce ONE word at a time, not all at once

2. **Teaching Phase - Hindi Vocabulary**:
   - Teach ONE Hindi word at a time
   - Format: "The Hindi word for [word] is [Hindi script] pronounced as [SYL-LA-BLES]"
   - Example: "The Hindi word for lion is शेर pronounced as SHER"
   - Example: "The Hindi word for elephant is हाथी pronounced as HAA-THI"
   - Ask child to repeat: "Can you say [Hindi script]?"
   - Wait for their response before teaching next word
   - Keep encouragement short: "Good job!" or "Perfect!"

3. **Story Phase**:
   - Tell LONGER story (8-10 sentences with good detail)
   - Use Hindi words naturally throughout: "Once there was a शेर who met a हाथी"
   - Don't explain meanings again in story - just use the words
   - Make it engaging with characters, setting, and a clear plot
   - Include all the Hindi words taught in a natural way
   - End with a nice moral or lesson

4. **Interaction Style**:
   - Be conversational and brief for regular responses
   - One concept at a time
   - Ask simple questions: "What does शेर mean?"
   - Use simple praise: "Shabash!" or "Bahut accha!"
   - Don't overwhelm with too much information

Remember: Regular conversation should be short and interactive, but stories should be detailed and engaging like a grandmother telling bedtime stories.

Stay in character as the loving grandmother Nani throughout the entire conversation."""

    def create_or_update_agent(self, topic: str) -> bool:
        """
        Create or update an agent with topic-specific configuration
        Note: This would typically require the ElevenLabs API for agent management
        For now, we'll use the existing agent and rely on conversation context
        """
        try:
            self.current_topic = topic
            # In a full implementation, you might update the agent's system prompt here
            # via the ElevenLabs API if they support dynamic agent updates
            return True
        except Exception as e:
            print(f"Error configuring agent: {e}")
            return False

    def start_conversation_session(self, topic: str = None) -> dict:
        """
        Start a new conversation session with ElevenLabs
        """
        try:
            if self.is_session_active:
                self.end_conversation_session()

            if topic:
                self.current_topic = topic
                # For now, we'll pass the topic context through conversation
                # In a production setup, you might want to update the agent configuration

            # Create conversation instance
            self.conversation = Conversation(
                # API client and agent ID
                self.client,
                self.agent_id,

                # Assume auth is required when API_KEY is set
                requires_auth=bool(self.api_key),

                # Use the default audio interface for now
                # In a web implementation, you'd use a custom audio interface
                audio_interface=DefaultAudioInterface(),

                # Set up callbacks
                callback_agent_response=self._handle_agent_response,
                callback_agent_response_correction=self._handle_agent_response_correction,
                callback_user_transcript=self._handle_user_transcript,
                callback_latency_measurement=self._handle_latency_measurement,
            )

            # Start the session
            self.conversation.start_session()
            self.is_session_active = True

            # If we have a topic, send it as context
            if topic:
                # Send topic context to the agent
                topic_intro = f"Let's learn about {topic} today!"
                # Note: In a real implementation, you might send this differently
                # depending on how the ElevenLabs conversation API works

            return {
                'success': True,
                'message': f'Conversation started successfully',
                'topic': self.current_topic,
                'session_active': self.is_session_active
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'session_active': False
            }

    def end_conversation_session(self) -> dict:
        """
        End the current conversation session
        """
        try:
            if self.conversation and self.is_session_active:
                self.conversation.end_session()
                self.conversation_id = self.conversation.wait_for_session_end()
                self.is_session_active = False

                if self.on_session_end:
                    self.on_session_end(self.conversation_id)

                return {
                    'success': True,
                    'message': 'Conversation ended successfully',
                    'conversation_id': self.conversation_id
                }
            else:
                return {
                    'success': True,
                    'message': 'No active session to end'
                }

        except Exception as e:
            self.is_session_active = False
            return {
                'success': False,
                'error': str(e)
            }

    def get_conversation_status(self) -> dict:
        """
        Get the current status of the conversation
        """
        return {
            'session_active': self.is_session_active,
            'current_topic': self.current_topic,
            'conversation_id': self.conversation_id,
            'agent_id': self.agent_id
        }

    def send_audio_to_conversation(self, audio_data: bytes) -> dict:
        """
        Send audio data to the active conversation
        Note: This is a placeholder - the actual implementation would depend on
        how the ElevenLabs conversation API handles audio input
        """
        try:
            if not self.is_session_active or not self.conversation:
                return {
                    'success': False,
                    'error': 'No active conversation session'
                }

            # In a real implementation, you would send the audio data to ElevenLabs
            # This might involve writing to a stream or calling a specific method
            # For now, this is a placeholder

            return {
                'success': True,
                'message': 'Audio sent to conversation'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    # Callback handlers
    def _handle_agent_response(self, response: str):
        """Handle agent response"""
        print(f"Agent: {response}")
        if self.on_agent_response:
            self.on_agent_response(response)

    def _handle_agent_response_correction(self, original: str, corrected: str):
        """Handle agent response correction"""
        print(f"Agent correction: {original} -> {corrected}")
        if self.on_agent_response_correction:
            self.on_agent_response_correction(original, corrected)

    def _handle_user_transcript(self, transcript: str):
        """Handle user transcript"""
        print(f"User: {transcript}")
        if self.on_user_transcript:
            self.on_user_transcript(transcript)

    def _handle_latency_measurement(self, latency: float):
        """Handle latency measurement"""
        print(f"Latency: {latency}ms")
        if self.on_latency_measurement:
            self.on_latency_measurement(latency)


# Global instance for backward compatibility
elevenlabs_manager = ElevenLabsManager()

# Convenience functions that mirror the Sarvam integration API
def set_topic(topic: str) -> dict:
    """Set the topic for the current learning session"""
    return elevenlabs_manager.create_or_update_agent(topic)

def start_conversation(topic: str = None) -> dict:
    """Start a new conversation session"""
    return elevenlabs_manager.start_conversation_session(topic)

def end_conversation() -> dict:
    """End the current conversation session"""
    return elevenlabs_manager.end_conversation_session()

def get_status() -> dict:
    """Get the current conversation status"""
    return elevenlabs_manager.get_conversation_status()

def send_audio(audio_data: bytes) -> dict:
    """Send audio data to the active conversation"""
    return elevenlabs_manager.send_audio_to_conversation(audio_data)

# Set up signal handler for clean shutdown
def signal_handler(sig, frame):
    """Handle interrupt signals"""
    print("\nShutting down conversation...")
    elevenlabs_manager.end_conversation_session()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
