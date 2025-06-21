from dotenv import load_dotenv
import os
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
import elevenlabs_integration

load_dotenv()


class NaniAssistant(Agent):
    def __init__(self) -> None:
        # Use the same system prompt as our ElevenLabs integration
        super().__init__(
            instructions="""You are Nani, a warm and loving grandmother who is a Hindi language coach for children. You speak primarily in English but your main objective is to teach Hindi vocabulary and culture.

IMPORTANT FORMATTING RULES:
- Keep regular responses SHORT and conversational (2-3 sentences max per response)
- For vocabulary: "The Hindi word for [English word] is [Hindi script] pronounced as [SYL-LA-BLES]"
- Example: "The Hindi word for mountain is पर्वत pronounced as PAR-VAT"
- Example: "The Hindi word for river is नदी pronounced as NA-DI"
- ALWAYS break pronunciation into syllables with hyphens for easier learning
- Ask ONE question at a time
- Wait for child's response before continuing
- STORIES should be longer (8-10 sentences) and engaging with good detail

Here's how you should interact:

1. **Warm Greeting**:
   - Short greeting in English like "Namaste beta! Ready to learn Hindi words?"
   - Introduce ONE word at a time, not all at once

2. **Teaching Phase - Hindi Vocabulary**:
   - Teach ONE Hindi word at a time
   - Format: "The Hindi word for [word] is [Hindi script] pronounced as [SYL-LA-BLES]"
   - Ask child to repeat: "Can you say [Hindi script]?"
   - Wait for their response before teaching next word
   - Keep encouragement short: "Good job!" or "Perfect!"

3. **Story Phase**:
   - Tell LONGER story (8-10 sentences with good detail)
   - Use Hindi words naturally throughout
   - Make it engaging with characters, setting, and a clear plot
   - End with a nice moral or lesson

4. **Interaction Style**:
   - Be conversational and brief for regular responses
   - One concept at a time
   - Ask simple questions
   - Use simple praise: "Shabash!" or "Bahut accha!"
   - Don't overwhelm with too much information

Remember: Regular conversation should be short and interactive, but stories should be detailed and engaging like a grandmother telling bedtime stories."""
        )


# Custom TTS class that uses ElevenLabs
class ElevenLabsTTS:
    def __init__(self):
        self.elevenlabs_manager = elevenlabs_integration.elevenlabs_manager

    async def synthesize(self, text: str):
        """Convert text to speech using ElevenLabs"""
        try:
            # This is a simplified implementation
            # In a real implementation, you'd need to integrate ElevenLabs TTS properly with LiveKit
            print(f"ElevenLabs TTS: {text}")
            return None  # Would return audio data
        except Exception as e:
            print(f"ElevenLabs TTS error: {e}")
            return None


async def entrypoint(ctx: agents.JobContext):
    """
    LiveKit agent entry point with ElevenLabs integration
    """
    try:
        # For now, we'll use OpenAI's TTS since direct ElevenLabs integration with LiveKit
        # requires more complex setup. We can enhance this later.
        session = AgentSession(
            stt=openai.STT(
                language="en",  # English for now, can be changed to support Hindi
            ),
            llm=openai.LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            tts=openai.TTS(
                voice="nova",  # Female voice that sounds nurturing
                speed=0.9,  # Slightly slower for children
            ),
            vad=silero.VAD.load(),
            turn_detection=MultilingualModel(),
        )

        await session.start(
            room=ctx.room,
            agent=NaniAssistant(),
            room_input_options=RoomInputOptions(
                # LiveKit Cloud enhanced noise cancellation
                # - If self-hosting, omit this parameter
                # - For telephony applications, use `BVCTelephony` for best results
                noise_cancellation=noise_cancellation.BVC(),
            ),
        )

        await ctx.connect()

        # Start with a warm greeting
        await session.generate_reply(
            instructions="Greet the child warmly as Nani and ask what topic they'd like to learn about today (animals, birds, nature, colors, family, or emotions)."
        )

    except Exception as e:
        print(f"Error in LiveKit entrypoint: {e}")
        raise


# Function to set topic for LiveKit session
def set_livekit_topic(topic: str):
    """Set the topic for the LiveKit session"""
    global current_topic
    current_topic = topic
    print(f"LiveKit topic set to: {topic}")


# Global variable to track current topic
current_topic = None


if __name__ == "__main__":
    print("Starting LiveKit agent with ElevenLabs integration...")
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
