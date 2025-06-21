from flask import Flask, render_template, request, jsonify
import base64
import sarvam_integration

app = Flask(__name__)


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

        # Set the topic in the sarvam integration
        sarvam_integration.set_topic(topic)

        return jsonify({
            'success': True,
            'message': f'Topic set to: {topic}',
            'topic': topic
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

        return jsonify({
            'success': True,
            'transcript': transcript,
            'ai_response': ai_response,
            'response_audio': response_audio,
            'message': 'Conversation completed successfully'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
