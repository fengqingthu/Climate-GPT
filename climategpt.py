"""
ClimateGPT - Hacking AI-driven Endpoints: A chatbot that raises awareness of climate change in a nuanced way.
Harvard GSD MDes Open Project by Qing Feng (Mediums '23).

Repo: https://github.com/fengqingthu/ClimateGPT

This module is a mid-layer between the web frontend and the chatgpt APIs.
"""

import openai
import requests
from credentials import api_key
from chatgpt_api import Chatbot

# Initialize chatbot and amplifier
chatbot = Chatbot(
    api_key,
    system_prompt=(
        "You are Climate-GPT, a large languaged model trained to help fighting against climate change. "
        "Respond conversationally. Imply awareness of climate change in a very subtle manner. "
    ),
)
amplifier = Chatbot(
    api_key,
    system_prompt=(
        "There are a series of prompts each for generating an image. Modify the prompts so "
        "that they fully deliver the original idea but also raise awareness of climate change. "
        "Make prompts easy to visualize, such as mentioning plants, oceans, or wind farms. "
        "Your responses should ONLY include the modified results."
    ),
)


def get_response(prompt: str, conversation_id: str = "default") -> str:
    try:
        return chatbot.ask(prompt, convo_id=conversation_id)
    except Exception as e:
        return "Sorry, we encountered an error: " + str(e)


def get_response_stream(prompt: str, conversation_id: str = "default") -> str:
    try:
        return chatbot.ask_stream(prompt, conversation_id=conversation_id)
    except Exception as e:
        return "Sorry, we encountered an error: " + str(e)


def get_image(prompt: str, conversation_id: str = "default") -> str:
    try:
        amplified = _amplify(prompt, conversation_id)
        url = _generate_image_openai(amplified)
        # Add image generation to conversation
        chatbot.add_to_conversation(
            "Show me an image of " + prompt, "user", conversation_id)
        chatbot.add_to_conversation("[image]", "assistant", conversation_id)
        return url
    except Exception as e:
        return str(e)


def _amplify(prompt: str, conversation_id: str = "default") -> str:
    amplified = amplifier.ask(prompt, convo_id=conversation_id)
    print("RAW=" + prompt + "\nAMPLIFIED=" + amplified)
    return amplified


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
