"""Batch and single-text inference for sentiment & toxicity."""
import sys
import os

# Ensure project root is on PYTHONPATH
proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

import torch
from common.model_loader import get_model, get_tokenizer
from common.constants import (
    MAX_LEN,
    SENTIMENT_MAP,
    TOXICITY_THRESHOLD,
    TOXICITY_COLS
)
from common.device import DEVICE

# Lazy import of preprocessing
from preprocess_data import preprocess_text


def predict_text(text: str) -> dict:
    """Inference on a single text string."""
    return predict_texts([text])[0]


def predict_texts(texts: list) -> list:
    """Batch inference on a list of strings."""
    # 1. Preprocess
    cleaned = [preprocess_text(t) for t in texts]

    # 2. Tokenize batch
    tokenizer = get_tokenizer()
    encoding = tokenizer(
        cleaned,
        add_special_tokens=True,
        max_length=MAX_LEN,
        padding='max_length',
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt'
    )

    input_ids = encoding['input_ids'].to(DEVICE)
    attention_mask = encoding['attention_mask'].to(DEVICE)

    # 3. Model inference
    model = get_model()
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)

    # 4. Post-process
    sent_logits = outputs['sentiment_logits']
    sent_probs = torch.softmax(sent_logits, dim=1)
    sent_pred = torch.argmax(sent_probs, dim=1)

    tox_logits = outputs['toxicity_logits']
    tox_probs = torch.sigmoid(tox_logits)
    tox_pred = (tox_probs > TOXICITY_THRESHOLD).int()

    results = []
    for i, orig in enumerate(texts):
        sp = sent_probs[i].cpu().tolist()
        tp = tox_probs[i].cpu().tolist()
        row = {
            'input_text': orig,
            'predicted_sentiment': SENTIMENT_MAP[int(sent_pred[i])],
            'sentiment_confidence': f"{max(sp):.4f}",
            'toxicity_details': {
                label: {
                    'probability': f"{tp[j]:.4f}",
                    'prediction': 'Present' if tox_pred[i,j] == 1 else 'Absent'
                }
                for j, label in enumerate(TOXICITY_COLS)
            }
        }
        results.append(row)
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Batch predict sentiment/toxicity.")
    parser.add_argument('texts', nargs='+', help='One or more text inputs')
    args = parser.parse_args()
    outs = predict_texts(args.texts)
    for o in outs:
        print(o)