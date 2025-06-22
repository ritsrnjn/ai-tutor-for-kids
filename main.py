from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import base64
import os
from dotenv import load_dotenv

# Custom OpenAI integration for image generation
import openai_integration

# Load environment variables
load_dotenv()

# Choose platform at startup
PLATFORM = os.getenv('PLATFORM', 'elevenlabs').lower()
print(f"🚀 Starting with platform: {PLATFORM.upper()}")

# Import based on chosen platform
if PLATFORM == 'livekit':
    import livekit_integration as ai_platform
    PLATFORM_NAME = "LiveKit + Sarvam"
    print("📡 Loading LiveKit integration...")
else:
    import elevenlabs_integration as ai_platform
    PLATFORM_NAME = "ElevenLabs"
    print("🎙️ Loading ElevenLabs integration...")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Enable CORS for all routes
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

# Initialize SocketIO for WebSocket support
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    # Pass platform info to template so it can render the right interface
    return render_template('index.html', platform=PLATFORM, platform_name=PLATFORM_NAME)

@app.route('/demo')
def demo():
    """Demo page to choose between platforms"""
    with open('demo_platforms.html', 'r') as f:
        return f.read()

@app.route('/set_topic', methods=['POST'])
def set_topic():
    """Set the topic for the current learning session"""
    try:
        data = request.json
        topic = data.get('topic')

        if not topic:
            return jsonify({'error': 'No topic provided'}), 400

        # Use the chosen platform
        if PLATFORM == 'livekit':
            result = ai_platform.set_topic(topic)
            return jsonify({
                'success': result['success'],
                'message': f'Topic set to: {topic} for {PLATFORM_NAME}',
                'topic': topic,
                'platform': PLATFORM
            })
        else:
            result = ai_platform.set_topic(topic)
            if result:
                # Emit topic update to connected clients for dynamic variables
                socketio.emit('topic_updated', {'topic': topic, 'platform': PLATFORM})
                return jsonify({
                    'success': True,
                    'message': f'Topic set to: {topic} for {PLATFORM_NAME}',
                    'topic': topic,
                    'platform': PLATFORM
                })
            else:
                return jsonify({'error': f'Failed to set topic in {PLATFORM_NAME}'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    """Get current platform status"""
    try:
        status_data = ai_platform.get_status()
        status_data['platform'] = PLATFORM
        status_data['platform_name'] = PLATFORM_NAME
        return jsonify(status_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/start_session', methods=['POST'])
def start_session():
    """Start a session with the chosen platform"""
    try:
        data = request.json or {}
        topic = data.get('topic')

        if PLATFORM == 'livekit':
            room_name = data.get('room_name', 'nani-hindi-tutor')
            result = ai_platform.start_session(topic, room_name)
        else:
            result = ai_platform.start_conversation(topic)

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/end_session', methods=['POST'])
def end_session():
    """End the current session"""
    try:
        if PLATFORM == 'livekit':
            result = ai_platform.end_session()
        else:
            result = ai_platform.end_conversation()

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_image', methods=['POST'])
def create_image():
    """
    Creates an image based on the agent's response using the enhanced workflow.
    """
    try:
        data = request.json
        agent_response = data.get('response')
        print(f"\n[DEBUG] 1. Received in /create_image, Agent Response: {agent_response}\n")

        if not agent_response:
            return jsonify({'error': 'No agent response provided'}), 400

        # Phase 1: Create enhanced prompt and words
        enhanced_data = openai_integration.create_enhanced_image_prompt(agent_response)
        print(f"[DEBUG] Enhanced data received: {enhanced_data}")
        if not enhanced_data or 'image_prompt' not in enhanced_data:
            print(f"[DEBUG] ERROR: Invalid enhanced data: {enhanced_data}")
            return jsonify({'error': 'Failed to create enhanced image prompt'}), 500

        image_prompt = enhanced_data.get('image_prompt')
        english_word = enhanced_data.get('english_word')
        hindi_word = enhanced_data.get('hindi_word')
        print(f"[DEBUG] About to generate image with prompt: {image_prompt}")

        # Phase 2: Generate image with the new prompt
        image_url = openai_integration.generate_image_with_dalle(image_prompt)
        print(f"[DEBUG] DALL-E returned image URL: {image_url}")
        if not image_url:
            print(f"[DEBUG] ERROR: DALL-E failed to generate image")
            return jsonify({'error': 'Failed to generate image with DALL-E'}), 500

        # Phase 3: Send all data to the frontend
        response_data = {
            'success': True,
            'image_url': image_url,
            'english_word': english_word,
            'hindi_word': hindi_word
        }
        print(f"[DEBUG] Sending response to frontend: {response_data}")
        return jsonify(response_data)

    except Exception as e:
        print(f"Error in /create_image: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/livekit_voice', methods=['POST'])
def livekit_voice():
    """Handle voice input for LiveKit platform"""
    try:
        if PLATFORM != 'livekit':
            return jsonify({'error': 'Not in LiveKit mode'}), 400

        data = request.json
        audio_data = data.get('audio')

        if not audio_data:
            return jsonify({'error': 'No audio data provided'}), 400

        # For now, simulate processing and return a Hindi response
        # In a real implementation, this would:
        # 1. Convert audio to text using Sarvam STT
        # 2. Process with OpenAI
        # 3. Convert response to speech using Sarvam TTS

        import random
        hindi_responses = [
            'नमस्ते! आप कैसे हैं? (Hello! How are you?)',
            'आज हम हिंदी सीखेंगे। (Today we will learn Hindi.)',
            'बहुत अच्छा! (Very good!)',
            'क्या आप और कुछ सीखना चाहते हैं? (Do you want to learn something more?)',
            'शाबाश! आप अच्छा बोल रहे हैं। (Excellent! You are speaking well.)',
            'हिंदी में "पानी" का मतलब "water" है। (In Hindi, "पानी" means "water".)',
            'आप बहुत अच्छे छात्र हैं! (You are a very good student!)'
        ]

        response_text = random.choice(hindi_responses)

        return jsonify({
            'success': True,
            'response': response_text,
            'user_transcript': 'Processing your voice...',
            'platform': 'livekit'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# SocketIO event handlers for real-time communication
@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print('Client connected')
    emit('status', {
        'message': f'Connected to server using {PLATFORM_NAME}',
        'platform': PLATFORM
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

@socketio.on('start_conversation')
def handle_start_conversation(data):
    """Handle start conversation request via WebSocket (legacy compatibility)"""
    try:
        topic = data.get('topic')

        if PLATFORM == 'livekit':
            room_name = data.get('room_name', 'nani-hindi-tutor')
            result = ai_platform.start_session(topic, room_name)
            emit('session_started', result)
        else:
            result = ai_platform.start_conversation(topic)
            emit('conversation_started', result)
    except Exception as e:
        emit('error', {'error': str(e), 'platform': PLATFORM})

@socketio.on('end_conversation')
def handle_end_conversation():
    """Handle end conversation request via WebSocket (legacy compatibility)"""
    try:
        if PLATFORM == 'livekit':
            result = ai_platform.end_session()
            emit('session_ended', result)
        else:
            result = ai_platform.end_conversation()
            emit('conversation_ended', result)
    except Exception as e:
        emit('error', {'error': str(e), 'platform': PLATFORM})

@socketio.on('audio_chunk')
def handle_audio_chunk(data):
    """Handle incoming audio chunks"""
    try:
        audio_data = data.get('audio')
        if audio_data:
            # Convert base64 to bytes
            audio_bytes = base64.b64decode(audio_data)

            if PLATFORM == 'elevenlabs':
                result = ai_platform.send_audio(audio_bytes)
                if not result['success']:
                    emit('error', result)
            # LiveKit handles audio differently - through WebRTC
    except Exception as e:
        emit('error', {'error': str(e)})

@socketio.on('get_status')
def handle_get_status():
    """Handle status request via WebSocket"""
    try:
        status_data = ai_platform.get_status()
        status_data['platform'] = PLATFORM
        status_data['platform_name'] = PLATFORM_NAME
        emit('status_update', status_data)
    except Exception as e:
        emit('error', {'error': str(e)})

# Set up platform-specific callbacks
def setup_callbacks():
    """Set up callbacks based on chosen platform"""
    def on_agent_response(response):
        print(f"Agent response received: {response}")
        socketio.emit('agent_response', {
            'response': response,
            'platform': PLATFORM
        })

    def on_user_transcript(transcript):
        socketio.emit('user_transcript', {
            'transcript': transcript,
            'platform': PLATFORM
        })

    def on_session_end(session_info):
        socketio.emit('session_ended', {
            'session_info': session_info,
            'platform': PLATFORM
        })

    # Set callbacks based on platform
    if PLATFORM == 'livekit':
        ai_platform.set_callbacks(
            on_agent_response=on_agent_response,
            on_user_transcript=on_user_transcript,
            on_session_end=on_session_end
        )
    else:
        # For ElevenLabs, the manager is the main point of interaction
        # We can set the callbacks directly on the imported module if it's structured that way
        ai_platform.set_callbacks(
            on_agent_response=on_agent_response,
            on_user_transcript=on_user_transcript
        )

# Initialize callbacks
setup_callbacks()

if __name__ == '__main__':
    print(f"🌟 Starting server with {PLATFORM_NAME} integration")
    print(f"🎯 Platform: {PLATFORM.upper()}")
    print(f"📍 Available at: http://localhost:5001")
    # Use SocketIO's run method instead of app.run for WebSocket support
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
