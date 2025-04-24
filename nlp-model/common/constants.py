"""Central location for project-wide constants."""
from typing import List, Dict

# Toxicity labels used throughout
TOXICITY_COLS: List[str] = [
    "toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate",
]

# Max sequence length for tokenizer
MAX_LEN: int = 128

# Sentiment label mapping
SENTIMENT_MAP: Dict[int, str] = {0: "Negative", 1: "Neutral", 2: "Positive"}

# Number of classes/tasks
NUM_SENTIMENT_LABELS: int = len(SENTIMENT_MAP)
NUM_TOXICITY_LABELS: int = len(TOXICITY_COLS)

# Threshold for toxicity prediction
TOXICITY_THRESHOLD: float = 0.5

# Model configuration
PRE_TRAINED_MODEL_NAME: str = "bert-base-uncased"
HF_REPO_ID: str = "Aseemks07/comment_mtl_bert_best"
HF_MODEL_FILENAME: str = "comment_mtl_bert_best.bin"
# Local fallback path (relative to project root)
LOCAL_MODEL_PATH: str = "model_output/comment_mtl_bert_best.bin"