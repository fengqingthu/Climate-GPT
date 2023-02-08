# ClimateGPT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a chatbot that raises awareness of climate change in a nuanced way, implemented by Qing Feng (Mediums '23) as part of the Harvard GSD MDes Open Project. This app is built on top of the [OpenAI APIs](https://beta.openai.com/docs/quickstart). You can follow the instructions below to get set up.

You can check out a [WIP deployment](https://fengqing.pythonanywhere.com/) here, which may be sporadically down due to restricted budget and OpenAI's rate limit. ClimateGPT leverages OpenAI's official model, which is unfortunately not as smart as ChatGPT's.

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

7. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file

8. Run the app

   ```bash
   $ flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)!
