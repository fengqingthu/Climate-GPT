import requests
import os
from climategpt import amplify

api_key = os.environ.get("OPENAI_API_KEY")


def get_image_stable_diffusion(prompt: str):
    """
    Exposed API to image generation application using stable diffusion hosted by deepai.org 
    """
    try:
        amplified = amplify(prompt)
        print("prompt=" + prompt + "\namplified=" + amplified)

        response = requests.post(
            "https://api.deepai.org/api/stable-diffusion",
            data={
                'text': amplified,
                'grid_size': "1",
                'width': "768",
                'height': "768",
            },
            headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
        )

        return response.json()["output_url"]
    except Exception as e:
        return str(e)


def get_image_openai(prompt: str):
    """
    Exposed API to image generation application using openai's Dall-e 
    """
    try:
        amplified = amplify(prompt)
        print("prompt=" + prompt + "\namplified=" + amplified)

        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            json={
                'prompt': amplified,
                'n': 1,
                'size': '1024x1024',
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + api_key,
            }
        )

        return response.json()['data'][0]['url']
    except Exception as e:
        return str(e)
