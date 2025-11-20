import os

import requests
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("API_KEY")
API_TIMEOUT = 20

# MODEL_NAME = "gpt-4o"
MODEL_NAME = "gpt-4o-mini"


def _request_model(
    prompt: str,
    api_url: str,
    api_key: str,
    api_timeout: int,
    service_name: str,
    system_prompt: str | None = None
) -> str | None:
    if not api_key:
        logger.warning(f"{service_name} API key not set, skipping {service_name}")
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
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
        response = requests.post(api_url, headers=headers, json=data, timeout=api_timeout)

        if response.status_code == 200:
            json_response = response.json()
            logger.info(f"{service_name} API Response: {json_response}")
            if "choices" in json_response and len(json_response["choices"]) > 0:
                return json_response["choices"][0]["message"]["content"]

        logger.error(f"{service_name} API Error: {response.status_code}, Response: {response.text}")

    except Exception as e:
        logger.error(f"{service_name} connection error: {e}")

    return None


def request_model(prompt: str, system_prompt: str | None = None) -> str | None:
    result = _request_model(prompt, OPENAI_API_URL, OPENAI_API_KEY, API_TIMEOUT, "OpenAI", system_prompt=system_prompt)
    if result is not None:
        return result

    logger.info("OpenAI failed, falling back to OpenRouter")
    return _request_model(prompt, OPENROUTER_API_URL, OPENROUTER_API_KEY, API_TIMEOUT, "OpenRouter", system_prompt=system_prompt)


if __name__ == "__main__":
    print(request_model("Make a greeting for Isaac Newton"))
