import uuid
import tempfile
from climategpt import get_response, get_response_stream, get_image, transcribe
from redditbot import start_monitor_thread
from flask import Flask, render_template, request, session, Response, send_from_directory, jsonify
from elevenlabs_api import ElevenLabsSpeech

speech_client = ElevenLabsSpeech()

app = Flask(__name__)
app.static_folder = 'static'

app.secret_key = "secret_key"


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["GET"])
def get_bot_response():
    userText = request.args.get('msg')
    if "conversation_id" not in session:
        id = str(uuid.uuid4())
        session["conversation_id"] = id
    else:
        id = session["conversation_id"]

    return get_response(userText, conversation_id=id)


@app.route("/chat_stream", methods=["GET"])
def get_bot_response_stream():
    userText = request.args.get('msg')
    if "conversation_id" not in session:
        id = str(uuid.uuid4())
        session["conversation_id"] = id
    else:
        id = session["conversation_id"]

    return Response(get_response_stream(userText, conversation_id=id), content_type='text/plain')


@app.route('/synthesize', methods=['POST'])
def synthesize():
    text = request.form.get('text', '')
    audio_url = speech_client.synthesize_speech(
        text,
        4,  # Elli
    )
    return jsonify({'audio_url': audio_url})


@app.route("/image", methods=["GET"])
def generate_image():
    prompt = request.args.get('prompt')
    if "conversation_id" not in session:
        id = str(uuid.uuid4())
        session["conversation_id"] = id
    else:
        id = session["conversation_id"]

    return get_image(prompt, conversation_id=id)


@app.route("/monitor", methods=["GET"])
def monitor_reddit_thread():
    thread_url = request.args.get('thread_url')
    return start_monitor_thread(thread_url)


@app.route("/whisper", methods=["POST"])
def audio_recognition():
    if 'wav' not in request.files:
        return "No audio file received", 400
    webm_file = request.files['wav']
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
        temp_path = temp_file.name
        webm_file.save(temp_path)
    return transcribe(temp_path)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
