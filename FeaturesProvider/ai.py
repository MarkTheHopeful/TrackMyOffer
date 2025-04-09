import logging
import os

import requests
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    # not a single string, because otherwise Openrouter bans it as soon as we commit it to Github
    API_KEY = "sk-or-v1"
    API_KEY += "-53584dae5c76645a56f6164f81cc5c3e63d0489a4cc5a138ca373b169a9e0518"
logger.info(f"API_KEY: {API_KEY}")
assert API_KEY, "API_KEY environment variable is not set"

# MODEL_NAME = "deepseek/deepseek-v3-base:free"
MODEL_NAME = "google/gemini-2.0-flash-exp:free"
PROMPTS = """
Please, write a greeting for person named '{}'.
It should be short and funny.
"""


def request_model(text: str) -> str | None:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": PROMPTS.format(text),
            }
        ],
        "stream": False,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=5)

        if response.status_code == 200:
            json_response = response.json()
            if "choices" in json_response:
                return json_response["choices"][0]["message"]["content"]

        logging.error(f"API Error: {response.status_code}, Response: {response.text}")

    except Exception as e:
        logging.error(f"Connection error: {e}")

    return None


if __name__ == "__main__":
    print(request_model("John"))
