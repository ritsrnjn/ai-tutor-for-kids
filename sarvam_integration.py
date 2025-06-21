import asyncio
from sarvamai import AsyncSarvamAI
from sarvamai import SarvamAI

client = SarvamAI(
    api_subscription_key="ed1e03a4-3d46-4adf-a65f-6ceda5e5a5a7",
)

# maintain this message as global variable
messages=[
            {"role": "system", "content": "You are a helpful AI tutor for young childrens"}
        ]

def chat_completion(input_message):
    # append in messages
    messages.append({"role": "user", "content": input_message})

    response = client.chat.completions(
        messages=messages,
        temperature=0.7,
        top_p= 1,
        max_tokens= 1000
    )

    # if received response is assistant, append in messages
    if response.choices[0].message.role == "assistant":
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
    print(response.choices[0].message.content)
    return response.choices[0].message.content



def transcribe_file(file_path):
    response = client.speech_to_text.transcribe(
        file=open(file_path, "rb"),
        model="saarika:v2.5"
    )
    print("Transcription:")
    print(response.transcript)

    return response.transcript

# Convert text to speech
def convert_text_to_speech(text):
    audio = client.text_to_speech.convert(
        target_language_code="en-IN",
        text=text,
        model="bulbul:v2",
        speaker="anushka"
    )
    # The output is a wave file encoded as a base64 string
    return audio



# async def transcribe_stream(audio_base64):
#     client = AsyncSarvamAI(
#         api_subscription_key="sk_gyaud0vy_aAfpfG3QFOjggIr3MhZ4Mdjp")

#     # Connect to streaming transcription
#     async with client.speech_to_text_streaming.connect(
#         language_code="kn-IN") as ws:
#         # Send audio data as base64 string
#         await ws.transcribe(audio=audio_base64)
#         print("[Debug]: sent audio message")

#         # Receive transcription response
#         resp = await ws.recv()
#         print(f"[Debug]: received response: {resp}")
