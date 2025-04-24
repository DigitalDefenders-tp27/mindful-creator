import re

# --- Text Cleaning Function (pure library) ---
def preprocess_text(text: str) -> str:
    """
    Applies basic cleaning steps to a single string.
    Lowercases, strips URLs, mentions, hashtags, punctuation, extra whitespace.
    """
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\@\w+', '', text)
    text = re.sub(r'\#\w+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()
