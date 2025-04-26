import os
import torch
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer

from common.constants import (
    PRE_TRAINED_MODEL_NAME,
    HF_REPO_ID,
    HF_MODEL_FILENAME,
    LOCAL_MODEL_PATH,
    NUM_SENTIMENT_LABELS,
    NUM_TOXICITY_LABELS
)
from common.device import DEVICE
from model import CommentMTLModel

# singleton holders
_model = None
_tokenizer = None

def _resolve_model_path() -> str:
    """Use local checkpoint if present; otherwise download from HF hub."""
    if os.path.exists(LOCAL_MODEL_PATH):
        return LOCAL_MODEL_PATH
    return hf_hub_download(repo_id=HF_REPO_ID, filename=HF_MODEL_FILENAME)

def get_tokenizer() -> AutoTokenizer:
    """Return a singleton HF tokenizer."""
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)
    return _tokenizer

def get_model() -> CommentMTLModel:
    """Return a singleton, eval‑mode CommentMTLModel on DEVICE."""
    global _model
    if _model is None:
        m = CommentMTLModel(
            model_name=PRE_TRAINED_MODEL_NAME,
            num_sentiment_labels=NUM_SENTIMENT_LABELS,
            num_toxicity_labels=NUM_TOXICITY_LABELS
        )
        ckpt = _resolve_model_path()
        state = torch.load(ckpt, map_location=DEVICE)
        m.load_state_dict(state)
        m.to(DEVICE)
        m.eval()
        _model = m
    return _model

if __name__ == "__main__":
    print("Loading tokenizer and model…")
    get_tokenizer()
    get_model()
    print("✅ Model & tokenizer ready.")
