# LiveKit Voice Agent with Sarvam STT and TTS

This voice agent uses LiveKit Agents with Sarvam for both speech-to-text (STT) and text-to-speech (TTS), optimized for Indian languages.

## Setup

### 1. Install Dependencies

```bash
pip install \
  "livekit-agents[sarvam,openai,silero,turn-detector]~=1.0" \
  "livekit-plugins-noise-cancellation~=0.2" \
  "python-dotenv"
```

### 2. Environment Variables

Create a `.env` file with your API keys:

```env
SARVAM_API_KEY=<Your Sarvam API Key>
OPENAI_API_KEY=<Your OpenAI API Key>
LIVEKIT_API_KEY=<Your LiveKit API Key>
LIVEKIT_API_SECRET=<Your LiveKit API Secret>
LIVEKIT_URL=<Your LiveKit WebSocket URL>
```

### 3. Get API Keys

- **Sarvam API Key**: Get from [Sarvam AI](https://docs.sarvam.ai/)
- **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/)
- **LiveKit Credentials**: Get from [LiveKit Cloud](https://cloud.livekit.io/) or your self-hosted instance

### 4. Download Model Files

```bash
python agent.py download-files
```

## Usage

### Console Mode (Local Testing)
```bash
python agent.py console
```

### Development Mode (Connect to LiveKit)
```bash
python agent.py dev
```

## Features

- **STT**: Sarvam STT with Hindi language support (configurable)
- **LLM**: OpenAI GPT-4o-mini for conversation
- **TTS**: Sarvam TTS for Indian language synthesis
- **VAD**: Silero Voice Activity Detection
- **Turn Detection**: Multilingual model for natural conversation flow
- **Noise Cancellation**: LiveKit Cloud enhanced background noise cancellation

## Configuration

The agent is configured for Hindi (`hi-IN`) by default. You can modify the language in `agent.py`:

```python
stt=sarvam.STT(
    language="hi-IN",  # Change to your preferred language
    model="saarika:v2.5",
),
```

Supported languages are listed in the [Sarvam documentation](https://docs.sarvam.ai/api-reference-docs/speech-to-text/transcribe#request.body.language_code.language_code).
