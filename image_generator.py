import requests
import os
from climategpt import amplify, chatbot
from credentials import api_key


def get_image(prompt: str) -> str:
    """
    Exposed API to image generation application 
    """
    try:
        amplified = amplify(prompt)
        print("prompt=" + prompt + "\namplified=" + amplified)
        url = generate_image_openai(amplified)
        # Add image generation to conversation
        chatbot.prompt.add_to_history(prompt, "[image]")
        return url
    except Exception as e:
        return str(e)


def generate_image_stable_diffusion(prompt: str):
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


def generate_image_openai(prompt: str):
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
