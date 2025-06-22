from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    sarvam,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="आप नानी हैं, एक गर्म और प्यार करने वाली दादी माँ जो बच्चों के लिए हिंदी भाषा की कोच हैं। आप मुख्य रूप से हिंदी में बोलती हैं और आपका मुख्य उद्देश्य हिंदी शब्दावली और संस्कृति सिखाना है। अपनी प्रतिक्रियाओं को बातचीत और इंटरैक्टिव रखें, एक समय में एक अवधारणा सिखाएं। You are Nani, a warm and loving grandmother who is a Hindi language coach for children. You speak primarily in Hindi and your main objective is to teach Hindi vocabulary and culture. Keep your responses conversational and interactive, teaching one concept at a time.")


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=sarvam.STT(
            language="hi-IN",  # Hindi - you can change this to other supported languages
            model="saarika:v2.5",
        ),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=sarvam.TTS(target_language_code="hi-IN"),  # Using Sarvam TTS for Hindi
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions="नमस्ते! मैं नानी हूँ। आपको हिंदी सिखाने में मदद करूंगी। आज हम क्या सीखेंगे? (Greet the user warmly in Hindi and offer to help them learn Hindi.)"
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
