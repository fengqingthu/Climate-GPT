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
chatbot = Chatbot(api_key)
amplifier = Chatbot(api_key,
                    system_prompt=("From now on, I will send you a series of scentences that are either responses from a conversation, or prompts for generating an image. "
                                   "Amplify the scentences so that they deliver the original idea but also imply awareness of climate change in a subtle manner. "
                                   "Your modifications must be as concise and nuanced as possible. Respond conversationally. Your responses should ONLY include the amplified result."),
                    )


def amplify(prompt: str, conversation_id: str = "default", stream: bool = False) -> str:
    """
    Exposed API to prompt amplification
    """
    if stream:  # Returns a generator of strs
        amplified = amplifier.ask_stream(
            "To amplify: '" + prompt + "'. ",
            convo_id=conversation_id,
        )
        print("RAW RESPONSE=" + prompt)
    else:
        amplified = amplifier.ask(
            "To amplify: '" + prompt + ". ",
            convo_id=conversation_id,
        )
        print("RAW=" + prompt + "\nAMPLIFIED=" + amplified)
    return amplified


def get_response(prompt: str, conversation_id: str = "default") -> str:
    """
    Exposed API to chatbot application with amplified response
    """
    try:
        response = chatbot.ask(prompt, conversation_id=conversation_id)
        return amplify(response, conversation_id=conversation_id)
    except Exception as e:
        return "Sorry, we encountered an error: " + str(e)


def get_response_stream(prompt: str, conversation_id: str = "default") -> str:
    """
    Exposed API to chatbot application with amplified response, streaming
    """
    try:
        response = chatbot.ask(prompt, conversation_id=conversation_id)
        return amplify(response, conversation_id, True)
    except Exception as e:
        return "Sorry, we encountered an error: " + str(e)


def get_raw_response(prompt: str, conversation_id: str = "default") -> str:
    """
    Exposed API to chatbot application for raw responses
    """
    try:
        return chatbot.ask(prompt, conversation_id=conversation_id)
    except Exception as e:
        return "Sorry, we encountered an error: " + str(e)


def get_image(prompt: str, conversation_id: str = "default") -> str:
    """
    Exposed API to image generation application 
    """
    try:
        amplified = amplify(prompt, conversation_id)
        url = _generate_image_openai(amplified)
        # Add image generation to conversation
        chatbot.add_to_conversation(
            prompt + ": [image].", "user", conversation_id)
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
