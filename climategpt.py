"""
ClimateGPT - Hacking AI-driven Endpoints: A chatbot that raises awareness of climate change in a nuanced way.
Harvard GSD MDes Open Project by Qing Feng (Mediums '23).

Repo: https://github.com/fengqingthu/ClimateGPT

This module is a mid-layer between the web frontend and the chatgpt APIs.
"""
import os
import openai
import requests
from credentials import api_key, email, password
from chatgpt_api_v1 import Chatbot as Chatbot_v1
from chatgpt_api_v2 import Chatbot as Chatbot_v2
from chatgpt_api_v3 import Chatbot as Chatbot_v3

version = os.environ.get("CHATGPT_API_VERSION")

chatbot = None
amplifier = None
base_prompt_sent = False

# Initialize chatbot and amplifier
if version == "1":
    chatbot = Chatbot_v1(api_key)
    amplifier = Chatbot_v1(api_key)
elif version == "2":
    print("Logging in...")
    chatbot = Chatbot_v2(email=email, password=password)
    amplifier = Chatbot_v2(email=email, password=password)
    print("Logged in")
elif version == "3":
    chatbot = Chatbot_v3(api_key)
    amplifier = Chatbot_v3(api_key)
else:
    raise Exception("No ChatGPT API version found!")


def amplify(prompt: str, stream=False) -> str:
    """
    Exposed API to prompt amplification
    """
    global base_prompt_sent
    if not base_prompt_sent:
        amplifier.ask(
            ("From now on, I will send you a series of scentences that are either responses from a conversation, or prompts for generating an image. "
             "Modify the scentences so that they deliver the original idea but also implying awareness of climate change in a very subtle manner. "
             "Your modifications must be as concise and nuanced as possible. Paraphrase yourself from time to time. Understand?")
        )
        base_prompt_sent = True

    if stream:
        amplified = amplifier.ask_stream(
            "To modify: '" + prompt + "'. Your response should ONLY include the modified result.")
        print("raw response=" + prompt)
    else:
        amplified = amplifier.ask(
            "To modify: '" + prompt + "'. Your response should ONLY include the modified result.")
        print("prompt=" + prompt + "\namplified=" + amplified)
    return amplified


def get_response(prompt: str, conversation_id: str = None) -> str:
    """
    Exposed API to chatbot application with amplified response
    """
    try:
        response = chatbot.ask(prompt, conversation_id=conversation_id)
        return amplify(response)
    except Exception as e:
        return "Sorry, we encountered an error: " + str(e)


def get_response_stream(prompt: str, conversation_id: str = None) -> str:
    """
    Exposed API to chatbot application with amplified response, streaming
    """
    try:
        response = chatbot.ask(prompt, conversation_id=conversation_id)
        return amplify(response, True)
    except Exception as e:
        return "Sorry, we encountered an error: " + str(e)


def get_raw_response(prompt: str, conversation_id: str = None) -> str:
    """
    Exposed API to chatbot application for raw responses
    """
    try:
        return chatbot.ask(prompt, conversation_id=conversation_id)
    except Exception as e:
        return "Sorry, we encountered an error: " + str(e)


def get_image(prompt: str) -> str:
    """
    Exposed API to image generation application 
    """
    try:
        amplified = amplify(prompt)
        url = _generate_image_openai(amplified)
        # Add image generation to conversation
        if version == 1:
            chatbot.prompt.add_to_history(prompt, "[image]")
        return url
    except Exception as e:
        return str(e)


def _generate_image_stable_diffusion(prompt: str) -> str:
    response = requests.post(
        "https://api.deepai.org/api/stable-diffusion",
        data={
            'text': prompt,
            'grid_size': "1",
            'width': "768",
            'height': "768",
        },
        headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
    )
    return response.json()["output_url"]


def _generate_image_openai(prompt: str) -> str:
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        json={
            'prompt': prompt,
            'n': 1,
            'size': '1024x1024',
        },
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + api_key,
        }
    )

    return response.json()['data'][0]['url']


def transcribe(fname):
    try:
        with open(fname, 'rb') as audio_file:
            transcription = openai.Audio.transcribe("whisper-1", audio_file)
            return transcription['text']
    except Exception as e:
        return str(e)
