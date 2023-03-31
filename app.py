import uuid
from climategpt import get_response, get_image
from redditbot import start_monitor_thread
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.static_folder = 'static'

app.secret_key = "secret_key"


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


@app.route("/image", methods=["GET"])
def generate_image():
    prompt = request.args.get('prompt')
    return get_image(prompt)


@app.route("/monitor", methods=["GET"])
def monitor_reddit_thread():
    thread_url = request.args.get('thread_url')
    return start_monitor_thread(thread_url)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
