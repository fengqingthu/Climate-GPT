from climategpt import get_response
from image_generator import get_image_openai as get_image
from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["GET"])
def get_bot_response():
    userText = request.args.get('msg')
    return get_response(userText)


@app.route("/image", methods=["GET"])
def generate_image():
    prompt = request.args.get('prompt')
    return get_image(prompt)


if __name__ == "__main__":
    app.run()
