import requests
from climategpt import amplify

def get_image(prompt: str):
    """
    Exposed API to image generation application
    """
    try:
        amplified = amplify(prompt)

        print("prompt= " + prompt + "\namplified= " + amplified)

        # return "test"
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
        return "Sorry, we encountered an error: " + str(e)
