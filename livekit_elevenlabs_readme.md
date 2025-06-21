# LiveKit + ElevenLabs Integration

This project integrates LiveKit with ElevenLabs to provide a comprehensive voice AI tutoring experience. You can use both platforms simultaneously:

- **ElevenLabs ConvAI**: Direct conversational AI through the web interface
- **LiveKit Agent**: Real-time voice agent for more complex interactions

## 🚀 Quick Start

### 1. Dependencies are already installed ✅

### 2. Environment Setup

Update your `.env` file with LiveKit credentials:

```env
# LiveKit Configuration (replace with your actual credentials)
LIVEKIT_API_KEY=your_livekit_api_key_here
LIVEKIT_API_SECRET=your_livekit_api_secret_here
LIVEKIT_URL=wss://your-project.livekit.cloud

# ElevenLabs Configuration (already set)
ELEVENLABS_API_KEY=sk_7137ced07d37e770474adaae359ff88078fc8a594f041404
ELEVENLABS_AGENT_ID=agent_01jy9sz4gnew0vedv885xsrse1

# OpenAI Configuration (already set)
OPENAI_API_KEY=sk-proj-...
```

### 3. Get LiveKit Credentials

1. Go to [LiveKit Cloud](https://cloud.livekit.io/)
2. Create a new project
3. Copy your API Key and Secret
4. Update the `.env` file

## 🎯 Usage Options

### Option 1: Web Interface (Current)
```bash
python main.py
```
Access at `http://localhost:5001` - Uses ElevenLabs ConvAI widget

### Option 2: LiveKit Console Mode
```bash
python livekit_elevenlabs_integration.py console
```
Direct console interaction with the Nani agent

### Option 3: LiveKit Development Mode
```bash
python livekit_elevenlabs_integration.py dev
```
Connects to LiveKit room for real-time interaction

### Option 4: Test Integration
```bash
python test_livekit.py
```
Verify that everything is set up correctly

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Frontend  │    │   Flask Backend  │    │   AI Services   │
│                 │    │                  │    │                 │
│ ElevenLabs      │◄──►│ main.py         │◄──►│ ElevenLabs API  │
│ ConvAI Widget   │    │                  │    │                 │
│                 │    │ SocketIO         │    │ OpenAI API      │
│ Image Display   │    │ REST API         │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ LiveKit Agent    │
                       │                  │
                       │ Voice AI Agent   │
                       │ Real-time STT    │
                       │ Real-time TTS    │
                       │ Nani Personality │
                       └──────────────────┘
```

## 📱 Features

### ElevenLabs Integration
- ✅ Real-time conversational AI
- ✅ Natural voice interactions
- ✅ Agent response corrections
- ✅ Latency monitoring
- ✅ WebSocket support

### LiveKit Integration
- ✅ Real-time voice agent
- ✅ OpenAI STT (Speech-to-Text)
- ✅ OpenAI LLM (GPT-4o-mini)
- ✅ OpenAI TTS (Text-to-Speech)
- ✅ Voice Activity Detection
- ✅ Noise Cancellation
- ✅ Multilingual turn detection

### Nani AI Coach
- ✅ Hindi language teaching
- ✅ Cultural storytelling
- ✅ Topic-based learning (animals, birds, nature, etc.)
- ✅ Interactive vocabulary lessons
- ✅ Pronunciation guidance
- ✅ Engaging mythological stories

## 🔧 Configuration

### Nani Personality
Both integrations use the same "Nani" personality:
- Warm, loving grandmother figure
- Hindi language coach
- Teaches vocabulary with pronunciation
- Tells engaging stories
- Interactive and patient

### Voice Settings
- **ElevenLabs**: Uses your configured agent voice
- **LiveKit**: Uses OpenAI "nova" voice (female, nurturing)
- **Speed**: Slightly slower for children (0.9x)

## 🧪 Testing

Run comprehensive tests:
```bash
python test_livekit.py
```

Expected output:
```
🧪 Testing LiveKit Integration

✅ All required environment variables are set
✅ LiveKit ElevenLabs integration imported successfully
✅ ElevenLabs integration imported successfully
✅ LiveKit agents imported successfully
✅ LiveKit topic setting works
✅ LiveKit topic retrieval works

🎉 All tests passed! LiveKit integration is ready.
```

## 📊 API Endpoints

### General
- `GET /` - Web interface
- `POST /set_topic` - Set topic for both integrations
- `POST /create_image` - Generate learning images

### ElevenLabs
- `GET /elevenlabs/status` - Get ElevenLabs status
- `POST /elevenlabs/start_conversation` - Start ElevenLabs session
- `POST /elevenlabs/end_conversation` - End ElevenLabs session

### LiveKit
- `GET /livekit/status` - Get LiveKit status
- `POST /livekit/set_topic` - Set LiveKit topic

## 🎮 Development

### File Structure
```
├── main.py                          # Flask app with both integrations
├── elevenlabs_integration.py        # ElevenLabs ConvAI integration
├── livekit_elevenlabs_integration.py # LiveKit agent integration
├── test_livekit.py                  # Integration tests
├── templates/index.html             # Web interface
└── static/js/                       # Frontend JavaScript
```

### Adding New Features

1. **ElevenLabs Features**: Edit `elevenlabs_integration.py`
2. **LiveKit Features**: Edit `livekit_elevenlabs_integration.py`
3. **Web Interface**: Edit `templates/index.html`
4. **API Endpoints**: Edit `main.py`

## 🎭 Character Prompts

Both integrations use consistent prompts for Nani:
- Short conversational responses (2-3 sentences)
- Vocabulary format: "The Hindi word for [word] is [script] pronounced as [SYL-LA-BLES]"
- Longer engaging stories (8-10 sentences)
- One concept at a time
- Patient, encouraging interactions

## 🚀 Next Steps

1. **Get LiveKit Credentials**: Sign up at [LiveKit Cloud](https://cloud.livekit.io/)
2. **Update .env**: Add your LiveKit API credentials
3. **Test Both Modes**: Try both web interface and LiveKit console
4. **Customize Agent**: Modify prompts and voice settings as needed
5. **Deploy**: Consider deployment options for production use

## 🆘 Troubleshooting

### Common Issues

**Import Errors**:
```bash
pip install -r requirements.txt
```

**Environment Variables**:
```bash
python test_livekit.py
```

**LiveKit Connection**:
- Check your API credentials
- Verify LIVEKIT_URL is correct
- Ensure firewall allows WebSocket connections

**ElevenLabs Issues**:
- Verify API key is valid
- Check agent ID is correct
- Monitor browser console for errors

---

**Ready to teach Hindi with Nani! 👵🏽📚🎯**
