# src/llm_handler.py (Corrected for Python 3.9 compatibility)

import requests
import json
import os
import configparser
from typing import Union, Optional # Import Union and Optional

# --- Configuration ---
CONFIG_FILE_PATH = 'config.ini' # Path to your config file

# --- Load Configuration ---
config = configparser.ConfigParser()
API_KEY = None
MODEL_NAME = "openrouter/optimus-alpha" # Default model (Update from Traceback if needed: google/gemini-2.5-pro-exp-03-25:free)
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

try:
    if not os.path.exists(CONFIG_FILE_PATH):
        print(f"Warning: Config file not found at {CONFIG_FILE_PATH}. API calls will fail unless key is set via environment or set_api_key().")
    else:
        config.read(CONFIG_FILE_PATH)
        API_KEY = config.get('API_KEYS', 'OPENROUTER_API_KEY', fallback=None)
        MODEL_NAME = config.get('SETTINGS', 'MODEL_NAME', fallback=MODEL_NAME) # Read model name

        if not API_KEY:
            print(f"Warning: OPENROUTER_API_KEY not found in {CONFIG_FILE_PATH} under [API_KEYS].")
        else:
             print("OpenRouter API Key loaded from config file.")
        print(f"Using model: {MODEL_NAME}") # Print the actual model being used

except configparser.Error as e:
    print(f"Error reading config file {CONFIG_FILE_PATH}: {e}")

# Fallback/Override: Check environment variable if not found in config (optional)
if not API_KEY:
    API_KEY = os.environ.get("OPENROUTER_API_KEY")
    if API_KEY:
        print("OpenRouter API Key loaded from environment variable as fallback.")


def set_api_key(key: str):
    """Allows setting the API key programmatically if needed (overrides config/env)."""
    global API_KEY
    API_KEY = key
    print("OpenRouter API Key set programmatically.")

# Use Union[str, None] for Python 3.9 compatibility
def _call_openrouter_api(prompt: str, system_message: str = "You are a helpful assistant.") -> Union[str, None]:
    """Helper function to call the OpenRouter Chat Completions API."""
    if not API_KEY:
        print("Error: OpenRouter API Key not set.")
        return None

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        # Add optional headers from example if needed
        #"HTTP-Referer": YOUR_SITE_URL,
        #"X-Title": YOUR_SITE_NAME
    }

    # *** SIMPLIFIED PAYLOAD STRUCTURE ***
    data = {
        "model": MODEL_NAME, # Read from config [cite: uploaded:src/config.ini]
        "messages": [
            {"role": "system", "content": system_message},
            {
                "role": "user",
                "content": prompt # Use the prompt string directly
            }
        ],
        "max_tokens": 10000 # Keep or adjust as needed
    }

    try:
        # Send data as JSON using json= parameter (requests handles json.dumps)
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=60) # Timeout added
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        result = response.json()

        # Process response (check the actual structure returned by OpenRouter/Gemini)
        if "choices" in result and len(result["choices"]) > 0:
             message = result["choices"][0].get("message", {})
             content = message.get("content")
             if content and isinstance(content, str):
                 return content.strip()
             else:
                print(f"Warning: No valid string content found in LLM response message: {message}")
                return None
        else:
            print(f"Warning: 'choices' not found or empty in LLM response: {result}")
            return None

    # Exception handling
    except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
            return None
    except requests.exceptions.RequestException as req_err:
            print(f"Error calling OpenRouter API: {req_err}")
            return None
    except json.JSONDecodeError as json_err:
            print(f"Error decoding JSON response from OpenRouter: {json_err}")
            # It's helpful to see the raw text that failed to parse
            response_text = response.text if 'response' in locals() else 'N/A'
            print(f"Response body (raw): {response_text}")
            return None

# Use Union[str, None] for Python 3.9 compatibility
def generate_toxicity_responses(comment: str, highest_toxicity_label: str, probability: float) -> Union[str, None]:
    """
    Generates response strategies for a comment identified as toxic.
    (Implementation unchanged from previous version)
    """
    system_message = (
        "You are an expert in online communication and conflict resolution. "
        "Your goal is to provide constructive response strategies for handling potentially harmful comments."
    )
    prompt = (
        f"The following comment has been flagged for '{highest_toxicity_label}' with a probability of {probability:.2f}:\n\n"
        f'"{comment}"\n\n'
        "Please provide 2-3 distinct, constructive response strategies for addressing this comment in an online community context. "
        "Consider options like direct but neutral replies, ignoring, reporting/moderation actions, or educational responses. "
        "Focus on de-escalation and maintaining a healthy community environment. Format the strategies clearly (e.g., using bullet points)."
    )

    print(f"Generating toxicity response strategies for label: {highest_toxicity_label}")
    response = _call_openrouter_api(prompt, system_message)
    return response

# Use Union[str, None] for Python 3.9 compatibility
def generate_positive_response(comment: str) -> Union[str, None]:
    """
    Generates an appreciative response for a positive, non-toxic comment.
    (Implementation unchanged from previous version)
    """
    system_message = "You are a friendly and appreciative community assistant."
    prompt = (
        f'The following comment has been identified as positive and non-toxic:\n\n'
        f'"{comment}"\n\n'
        "Please write a short, sincere response to acknowledge and appreciate the user's positive contribution. "
        "Keep it brief and encouraging."
    )

    print("Generating positive appreciative response.")
    response = _call_openrouter_api(prompt, system_message)
    return response


# --- Example Usage (Optional - for testing this script directly) ---
if __name__ == '__main__':
    if not API_KEY:
         # Use f-string for cleaner formatting
         print(f"\nPlease set the OPENROUTER_API_KEY in {CONFIG_FILE_PATH} or environment variable to run tests.")
    else:
         print("\n--- Testing Toxicity Response ---")
         test_toxic_comment = "You are an idiot, your ideas are worthless!"
         toxic_strategies = generate_toxicity_responses(test_toxic_comment, "insult", 0.95)
         if toxic_strategies:
              print("Strategies:\n", toxic_strategies)
         else:
             print("Failed to get toxicity strategies.")


         print("\n--- Testing Positive Response ---")
         test_positive_comment = "This is a fantastic tutorial, thank you so much for sharing!"
         positive_reply = generate_positive_response(test_positive_comment)
         if positive_reply:
             print("Appreciation:\n", positive_reply)
         else:
             print("Failed to get positive reply.")