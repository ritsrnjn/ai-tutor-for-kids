import asyncio
import os
import threading
from typing import Optional, Callable
from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    sarvam,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load environment variables
load_dotenv()

class LiveKitManager:
    """
    Manages LiveKit conversational AI sessions with Sarvam STT/TTS
    """

    def __init__(self):
        self.api_key = os.getenv("LIVEKIT_API_KEY")
        self.api_secret = os.getenv("LIVEKIT_API_SECRET")
        self.livekit_url = os.getenv("LIVEKIT_URL", "ws://localhost:7880")
        self.sarvam_api_key = os.getenv("SARVAM_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        self.room_name = None
        self.agent_thread = None
        self.is_session_active = False
        self.current_topic = None

        # Callbacks for handling responses
        self.on_agent_response: Optional[Callable] = None
        self.on_user_transcript: Optional[Callable] = None
        self.on_session_end: Optional[Callable] = None

    def set_callbacks(self,
                     on_agent_response: Optional[Callable] = None,
                     on_user_transcript: Optional[Callable] = None,
                     on_session_end: Optional[Callable] = None):
        """Set callback functions for handling conversation events"""
        self.on_agent_response = on_agent_response
        self.on_user_transcript = on_user_transcript
        self.on_session_end = on_session_end

    def get_nani_instructions(self, topic: str = None) -> str:
        """
        Get the Nani character instructions for the agent
        """
        topic_context = f"Today's topic is: {topic}. " if topic else ""

        return f"""You are Nani, a warm and loving grandmother who is a Hindi language coach for children. You speak primarily in English but your main objective is to teach Hindi vocabulary and culture.

{topic_context}

IMPORTANT FORMATTING RULES:
- Keep responses SHORT and conversational (2-3 sentences max per response)
- For vocabulary: "The Hindi word for [English word] is [Hindi script] pronounced as [SYL-LA-BLES]"
- Example: "The Hindi word for mountain is पर्वत pronounced as PAR-VAT"
- ALWAYS break pronunciation into syllables with hyphens for easier learning
- Ask ONE question at a time
- Wait for child's response before continuing
- Be encouraging and use simple praise like "Shabash!" or "Bahut accha!"

Here's how you should interact:

1. **Teaching Phase - Hindi Vocabulary**:
   - Teach ONE Hindi word at a time
   - Format: "The Hindi word for [word] is [Hindi script] pronounced as [SYL-LA-BLES]"
   - Ask child to repeat: "Can you say [Hindi script]?"
   - Keep encouragement short: "Good job!" or "Perfect!"

2. **Interaction Style**:
   - Be conversational and brief
   - One concept at a time
   - Ask simple questions
   - Don't overwhelm with too much information

Remember: Stay in character as the loving grandmother Nani throughout the entire conversation."""

    class NaniAssistant(Agent):
        def __init__(self, instructions: str) -> None:
            super().__init__(instructions=instructions)

    async def create_agent_session(self, topic: str = None) -> AgentSession:
        """
        Create a new agent session with Sarvam STT/TTS and OpenAI LLM
        """
        instructions = self.get_nani_instructions(topic)

        session = AgentSession(
            stt=sarvam.STT(
                language="hi-IN",  # Hindi support
                model="saarika:v2.5",
            ),
            llm=openai.LLM(model="gpt-4o-mini"),
            tts=sarvam.TTS(target_language_code="hi-IN"),  # Hindi TTS
            vad=silero.VAD.load(),
            turn_detection=MultilingualModel(),
        )

        return session

    def start_livekit_session(self, topic: str = None, room_name: str = "nani-hindi-tutor") -> dict:
        """
        Start a new LiveKit session
        """
        try:
            if self.is_session_active:
                return {'success': False, 'error': 'Session already active'}

            self.current_topic = topic
            self.room_name = room_name

            # Start agent in a separate thread
            def run_agent():
                asyncio.run(self._run_agent_session())

            self.agent_thread = threading.Thread(target=run_agent, daemon=True)
            self.agent_thread.start()
            self.is_session_active = True

            return {
                'success': True,
                'message': f'LiveKit session started',
                'room_name': room_name,
                'topic': topic,
                'session_active': self.is_session_active
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'session_active': False
            }

    async def _run_agent_session(self):
        """
        Internal method to run the agent session
        """
        try:
            # Create room connection
            room = rtc.Room()

            # Create agent session
            session = await self.create_agent_session(self.current_topic)
            agent = self.NaniAssistant(self.get_nani_instructions(self.current_topic))

            await session.start(
                room=room,
                agent=agent,
                room_input_options=RoomInputOptions(
                    noise_cancellation=noise_cancellation.BVC(),
                ),
            )

            # Connect to LiveKit room
            token = rtc.AccessToken(self.api_key, self.api_secret) \
                .with_identity("nani-agent") \
                .with_name("Nani Hindi Tutor") \
                .with_grants(rtc.VideoGrants(room_join=True, room=self.room_name)) \
                .to_jwt()

            await room.connect(self.livekit_url, token)

            # Generate initial greeting
            await session.generate_reply(
                instructions="Greet the child warmly as Nani and ask what they'd like to learn about today."
            )

            # Keep session alive
            while self.is_session_active:
                await asyncio.sleep(1)

        except Exception as e:
            print(f"Error in agent session: {e}")
            self.is_session_active = False
            if self.on_session_end:
                self.on_session_end(str(e))

    def end_livekit_session(self) -> dict:
        """
        End the current LiveKit session
        """
        try:
            if self.is_session_active:
                self.is_session_active = False

                if self.on_session_end:
                    self.on_session_end(self.room_name)

                return {
                    'success': True,
                    'message': 'LiveKit session ended successfully',
                    'room_name': self.room_name
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

    def get_session_status(self) -> dict:
        """
        Get the current session status
        """
        return {
            'session_active': self.is_session_active,
            'room_name': self.room_name,
            'current_topic': self.current_topic,
            'has_api_keys': bool(self.api_key and self.api_secret and self.sarvam_api_key)
        }

# Create global instance
livekit_manager = LiveKitManager()

# Main API functions for LiveKit integration
def set_topic(topic: str) -> dict:
    """Set the topic for the current learning session"""
    livekit_manager.current_topic = topic
    return {'success': True, 'topic': topic}

def start_session(topic: str = None, room_name: str = "nani-hindi-tutor") -> dict:
    """Start a LiveKit session"""
    return livekit_manager.start_livekit_session(topic, room_name)

def end_session() -> dict:
    """End the current LiveKit session"""
    return livekit_manager.end_livekit_session()

def get_status() -> dict:
    """Get LiveKit session status"""
    return livekit_manager.get_session_status()

def set_callbacks(**kwargs):
    """Set callback functions for LiveKit events"""
    livekit_manager.set_callbacks(**kwargs)
