# Climate-GPT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Climate-GPT is a chatbot that raises awareness of climate change in a nuanced way, serving all types of mass-customized mediums. Implemented by Qing Feng (Harvard GSD Mediums '23), this app is part of his MDes Open Project. Climate-GPT is built on top of [OpenAI APIs](https://beta.openai.com/docs/quickstart) for the chat, image generation, and voice transcription endpoints, and [Eleven Labs APIs](https://docs.elevenlabs.io/quickstart) for sythesized speeches. 

You can follow the instructions below to get set up. Also, [check out our deployment here](https://www.climate-gpt.com). ClimateGPT leverages OpenAI's GPT-3.5 model.

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/)

2. Clone this repository

3. Navigate into the project directory

   ```bash
   $ cd ClimateGPT
   ```

4. Create a new virtual environment

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file

   ```bash
   $ cp .env.example .env
   ```

7. Add your [Open AI API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file. Fill up all other fields accordingly.

8. Run the app

   ```bash
   $ flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)!
