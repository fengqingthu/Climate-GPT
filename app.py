import uuid, os
from climategpt import get_response
from image_generator import get_image_openai as get_image
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.static_folder = 'static'

email = os.environ.get("OPENAI_EMAIL")
password = os.environ.get("OPENAI_PASSWORD")
app.secret_key = password


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
    print("id=" + id)
    return get_response(userText, conversation_id=id)


@app.route("/image", methods=["GET"])
def generate_image():
    prompt = request.args.get('prompt')
    return get_image(prompt)


if __name__ == "__main__":
    app.run()
