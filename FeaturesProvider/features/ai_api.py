import os

import requests
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()

API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv("API_KEY")
API_TIMEOUT = 20

# MODEL_NAME = "gpt-4o"
MODEL_NAME = "gpt-4o-mini"


def request_model(prompt: str) -> str | None:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "stream": False,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=API_TIMEOUT)

        if response.status_code == 200:
            json_response = response.json()
            logger.info(f"API Response: {json_response}")
            if "choices" in json_response and len(json_response["choices"]) > 0:
                return json_response["choices"][0]["message"]["content"]

        logger.error(f"API Error: {response.status_code}, Response: {response.text}")

    except Exception as e:
        logger.error(f"Connection error: {e}")

    return None


if __name__ == "__main__":
    print(request_model("Make a greeting for Isaac Newton"))
