from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import base64
import os
from dotenv import load_dotenv
import image_util

# Load environment variables
load_dotenv()

# Import both integrations
import sarvam_integration
import elevenlabs_integration
import image_util

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Initialize SocketIO for WebSocket support
socketio = SocketIO(app, cors_allowed_origins="*")

# Choose which integration to use (can be controlled via environment variable)
USE_ELEVENLABS = os.getenv('USE_ELEVENLABS', 'false').lower() == 'true'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/set_topic', methods=['POST'])
def set_topic():
    """Set the topic for the current learning session"""
    try:
        data = request.json
        topic = data.get('topic')

        if not topic:
            return jsonify({'error': 'No topic provided'}), 400

        if USE_ELEVENLABS:
            # Use ElevenLabs integration
            result = elevenlabs_integration.set_topic(topic)
            if result:
                return jsonify({
                    'success': True,
                    'message': f'Topic set to: {topic}',
                    'topic': topic,
                    'using_elevenlabs': True
                })
            else:
                return jsonify({'error': 'Failed to set topic in ElevenLabs'}), 500
        else:
            # Use Sarvam integration (existing behavior)
            sarvam_integration.set_topic(topic)
            return jsonify({
                'success': True,
                'message': f'Topic set to: {topic}',
                'topic': topic,
                'using_elevenlabs': False
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/talk', methods=['POST'])
def talk():
    try:
        data = request.json
        audio_base64 = data.get('audio')

        if not audio_base64:
            return jsonify({'error': 'No audio data provided'}), 400

        # Step 1: Convert base64 to bytes and save as WAV file
        audio_data = base64.b64decode(audio_base64)
        audio_filename = 'recorded_audio.wav'

        with open(audio_filename, 'wb') as audio_file:
            audio_file.write(audio_data)

        # Step 2: Transcribe the audio
        transcript = sarvam_integration.transcribe_file(audio_filename)

        if not transcript or transcript.strip() == "":
            return jsonify({'error': 'Could not transcribe audio'}), 400

        # Step 3: Get AI response using chat completion
        ai_response = sarvam_integration.chat_completion(transcript)

        # Step 4: Convert AI response to speech
        response_audio_obj = sarvam_integration.convert_text_to_speech(
            ai_response)

        # Extract the base64 audio data from the response object
        response_audio = None
        if hasattr(response_audio_obj, 'audios') and len(
                response_audio_obj.audios) > 0:
            response_audio = response_audio_obj.audios[0]
        else:
            print("Warning: No audio data in response object")

        # Generate image for the AI response
        try:
            image_url = image_util.generate_relevant_image(ai_response)
        except Exception as e:
            print(f"Error generating image: {e}")
            image_url = None

        return jsonify({
            'success': True,
            'transcript': transcript,
            'ai_response': ai_response,
            'response_audio': response_audio,
            'image_url': image_url,
            'message': 'Conversation completed successfully'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ElevenLabs-specific routes and SocketIO handlers
@app.route('/elevenlabs/status', methods=['GET'])
def elevenlabs_status():
    """Get ElevenLabs conversation status"""
    try:
        status = elevenlabs_integration.get_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/elevenlabs/start_conversation', methods=['POST'])
def start_elevenlabs_conversation():
    """Start an ElevenLabs conversation session"""
    try:
        data = request.json or {}
        topic = data.get('topic')

        result = elevenlabs_integration.start_conversation(topic)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/elevenlabs/end_conversation', methods=['POST'])
def end_elevenlabs_conversation():
    """End the current ElevenLabs conversation session"""
    try:
        result = elevenlabs_integration.end_conversation()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_image', methods=['POST'])
def create_image():
    """Generate an image based on AI response"""
    try:
        data = request.json
        ai_response = data.get('response')

        if not ai_response:
            return jsonify({'error': 'No AI response provided'}), 400

        # Generate image using the image utility
        image_url, highlight_word = image_util.generate_relevant_image_and_highlight_word(ai_response)

        return jsonify({
            'success': True,
            'image_url': image_url,
            'ai_response': ai_response,
            'highlight_word': highlight_word
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# SocketIO event handlers for real-time communication
@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print('Client connected')
    emit('status', {'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')

@socketio.on('start_conversation')
def handle_start_conversation(data):
    """Handle start conversation request via WebSocket"""
    try:
        topic = data.get('topic')
        result = elevenlabs_integration.start_conversation(topic)
        emit('conversation_started', result)
    except Exception as e:
        emit('error', {'error': str(e)})

@socketio.on('end_conversation')
def handle_end_conversation():
    """Handle end conversation request via WebSocket"""
    try:
        result = elevenlabs_integration.end_conversation()
        emit('conversation_ended', result)
    except Exception as e:
        emit('error', {'error': str(e)})

@socketio.on('audio_chunk')
def handle_audio_chunk(data):
    """Handle incoming audio chunks for ElevenLabs"""
    try:
        audio_data = data.get('audio')
        if audio_data:
            # Convert base64 to bytes
            audio_bytes = base64.b64decode(audio_data)
            result = elevenlabs_integration.send_audio(audio_bytes)
            if not result['success']:
                emit('error', result)
    except Exception as e:
        emit('error', {'error': str(e)})

@socketio.on('get_status')
def handle_get_status():
    """Handle status request via WebSocket"""
    try:
        status = elevenlabs_integration.get_status()
        emit('status_update', status)
    except Exception as e:
        emit('error', {'error': str(e)})

# Set up ElevenLabs callbacks for WebSocket communication
def setup_elevenlabs_callbacks():
    """Set up callbacks for ElevenLabs events"""
    def on_agent_response(response):
        socketio.emit('agent_response', {'response': response})

    def on_user_transcript(transcript):
        socketio.emit('user_transcript', {'transcript': transcript})

    def on_agent_response_correction(original, corrected):
        socketio.emit('agent_response_correction', {
            'original': original,
            'corrected': corrected
        })

    def on_latency_measurement(latency):
        socketio.emit('latency_measurement', {'latency': latency})

    def on_session_end(conversation_id):
        socketio.emit('session_ended', {'conversation_id': conversation_id})

    # Set the callbacks
    elevenlabs_integration.elevenlabs_manager.set_callbacks(
        on_agent_response=on_agent_response,
        on_user_transcript=on_user_transcript,
        on_agent_response_correction=on_agent_response_correction,
        on_latency_measurement=on_latency_measurement,
        on_session_end=on_session_end
    )

# Initialize ElevenLabs callbacks
setup_elevenlabs_callbacks()

if __name__ == '__main__':
    print(f"Starting server with {'ElevenLabs' if USE_ELEVENLABS else 'Sarvam'} integration")
    # Use SocketIO's run method instead of app.run for WebSocket support
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
