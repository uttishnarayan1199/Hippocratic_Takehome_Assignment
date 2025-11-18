import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# --- Load .env explicitly from the project root ---
PROJECT_ROOT = Path(__file__).resolve().parent
env_path = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=env_path)
# ---------------------------------------------------


def get_api_key() -> str:
    """Return the OpenAI API key or raise an error if it is missing."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. "
            "Add it to your .env file as OPENAI_API_KEY=sk-proj-..."
        )
    return api_key


# Create a single reusable OpenAI client.
# It automatically reads OPENAI_API_KEY from the environment.
client = OpenAI(api_key=get_api_key())


def call_chat_model(
    messages,
    max_tokens: int = 1000,
    temperature: float = 0.7,
) -> str:
    """
    Generic helper to call gpt-3.5-turbo using the new OpenAI Python SDK.

    messages should be a list of dicts like:
    [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello"},
    ]
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # required by the assignment
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    # New SDK: content is under message.content (a list of TextContentBlock)
    return response.choices[0].message.content
