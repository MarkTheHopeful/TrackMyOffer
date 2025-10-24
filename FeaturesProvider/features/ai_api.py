import os

import requests
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("API_KEY")

# MODEL_NAME = "deepseek/deepseek-v3-base:free"
MODEL_NAME = "google/gemini-2.0-flash-exp:free"
# MODEL_NAME = "nousresearch/deephermes-3-mistral-24b-preview:free"


def request_model(prompt: str, system_prompt: str | None = None) -> str | None:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    data = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=5)

        if response.status_code == 200:
            json_response = response.json()
            if "choices" in json_response:
                return json_response["choices"][0]["message"]["content"]

        logger.error(f"API Error: {response.status_code}, Response: {response.text}")

    except Exception as e:
        logger.error(f"Connection error: {e}")

    return None


if __name__ == "__main__":
    print(request_model("Make a greeting for Isaac Newton"))
