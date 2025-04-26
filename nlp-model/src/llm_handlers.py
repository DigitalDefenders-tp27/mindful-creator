"""Refactored LLM handler using a persistent Session and generic template support."""
import sys
import os
import logging

# Ensure project root is on PYTHONPATH
proj_root = os.path.dirname(os.path.abspath(__file__))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

import requests
from typing import Optional, Dict
from configparser import ConfigParser, Error as ConfigError

# --- Configuration ---
CONFIG_FILE_PATH = os.path.join(proj_root, 'config.ini')
DEFAULT_MODEL = "deepseek/deepseek-chat-v3-0324:free"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Set up logging
LOGLEVEL = os.getenv('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger(__name__)

# Module-level session
_session = requests.Session()
_api_key: Optional[str] = None
_model_name: str = DEFAULT_MODEL

# Load config once
def load_config() -> None:
    global _api_key, _model_name
    parser = ConfigParser()
    try:
        if os.path.exists(CONFIG_FILE_PATH):
            parser.read(CONFIG_FILE_PATH)
            _api_key = parser.get('API_KEYS', 'OPENROUTER_API_KEY', fallback=_api_key)
            _model_name = parser.get('SETTINGS', 'MODEL_NAME', fallback=_model_name)
            logger.info("Config loaded: model=%s", _model_name)
        else:
            logger.warning("Config file not found: %s", CONFIG_FILE_PATH)
    except ConfigError as e:
        logger.error("Error reading config: %s", e)
    # Fallback to env var
    if not _api_key:
        _api_key = os.getenv('OPENROUTER_API_KEY')
    if _api_key:
        _session.headers.update({"Authorization": f"Bearer {_api_key}"})
    _session.headers.update({"Content-Type": "application/json"})

load_config()


def set_api_key(key: str) -> None:
    """Programmatically set/override the API key."""
    global _api_key
    _api_key = key
    _session.headers.update({"Authorization": f"Bearer {_api_key}"})
    logger.info("API key set programmatically.")


def generate_response(
    prompt: str,
    system_message: str = "You are a helpful assistant.",
    model: Optional[str] = None,
    max_tokens: int = 10000
) -> Optional[str]:
    """Generic LLM call. Returns the response content or None."""
    if not _api_key:
        logger.error("No API key configured.")
        return None
    payload = {
        "model": model or _model_name,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }
    try:
        resp = _session.post(API_URL, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        choices = data.get('choices') or []
        if choices:
            content = choices[0].get('message', {}).get('content')
            return content.strip() if isinstance(content, str) else None
        logger.warning("No choices in response: %s", data)
    except requests.RequestException as e:
        logger.error("Request error: %s", e)
    except ValueError as e:
        logger.error("JSON error: %s", e)
    return None


def generate_toxicity_responses(
    comment: str,
    highest_label: str,
    prob: float
) -> Optional[str]:
    """Generate strategies for a toxic comment."""
    prompt = (
        f"The comment flagged as '{highest_label}' (prob {prob:.2f}):\"{comment}\""
        "Suggest 2–3 constructive response strategies (bullet points)."
    )
    return generate_response(
        prompt,
        system_message=(
            "You are an expert in online communication and conflict resolution."    
        )
    )


def generate_positive_response(comment: str) -> Optional[str]:
    """Generate an appreciation reply for a positive comment."""
    prompt = f"Positive comment: \"{comment}\"Write a brief, sincere appreciation."  
    return generate_response(
        prompt,
        system_message="You are a friendly and appreciative community assistant."
    )


if __name__ == '__main__':
    # Quick smoke test
    print("Testing LLM handler…")
    sample = "This is a great feature!"
    print("Positive reply:", generate_positive_response(sample))
    print("Toxic reply:", generate_toxicity_responses("such useless content, please die", "threat", 0.6))