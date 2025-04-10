# src/model.py

import torch
import torch.nn as nn
from transformers import BertModel, AutoModel # Use AutoModel for flexibility

# --- Configuration ---
PRE_TRAINED_MODEL_NAME = 'bert-base-uncased'
# These should match the dataset and preprocessing steps
NUM_SENTIMENT_LABELS = 3  # 0: Negative, 1: Neutral, 2: Positive
NUM_TOXICITY_LABELS = 6 # toxic, severe_toxic, obscene, threat, insult, identity_hate

class CommentMTLModel(nn.Module):
    """
    Multi-Task Learning model using a BERT base and separate heads for
    sentiment classification and toxicity multi-label classification.
    """
    def __init__(self, model_name, num_sentiment_labels, num_toxicity_labels, dropout_prob=0.1):
        """
        Args:
            model_name (str): Name of the pre-trained BERT model from Hugging Face.
            num_sentiment_labels (int): Number of classes for sentiment analysis.
            num_toxicity_labels (int): Number of classes for toxicity detection.
            dropout_prob (float): Dropout probability for the classification heads.
        """
        super(CommentMTLModel, self).__init__()

        print(f"Initializing model with BERT base: {model_name}")
        # Load the pre-trained BERT model
        self.bert = AutoModel.from_pretrained(model_name)

        # Dropout layer for regularization - applied after BERT output, before heads
        self.dropout = nn.Dropout(dropout_prob)

        # --- Sentiment Head ---
        # Takes BERT's pooled output (for [CLS] token) and maps it to sentiment logits
        # BERT hidden size is typically 768 for 'bert-base-uncased'
        self.sentiment_classifier = nn.Linear(self.bert.config.hidden_size, num_sentiment_labels)

        # --- Toxicity Head ---
        # Takes BERT's pooled output and maps it to toxicity logits (multi-label)
        self.toxicity_classifier = nn.Linear(self.bert.config.hidden_size, num_toxicity_labels)

        print("Model heads initialized:")
        print(f"  Sentiment Head Output Dim: {num_sentiment_labels}")
        print(f"  Toxicity Head Output Dim: {num_toxicity_labels}")

    def forward(self, input_ids, attention_mask):
        """
        Forward pass of the model.

        Args:
            input_ids (torch.Tensor): Tensor of input token IDs (batch_size, seq_length).
            attention_mask (torch.Tensor): Tensor of attention masks (batch_size, seq_length).

        Returns:
            dict: A dictionary containing the raw output logits for each task:
                'sentiment_logits': Logits for sentiment classification (batch_size, num_sentiment_labels).
                'toxicity_logits': Logits for toxicity multi-label classification (batch_size, num_toxicity_labels).
        """
        # Pass input through BERT model
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        # Get the pooled output - BERT often provides a pooled output representing the entire sequence,
        # typically derived from the [CLS] token's final hidden state after further processing.
        # Alternatively, you could use outputs.last_hidden_state[:, 0, :] which is the [CLS] token's
        # hidden state directly. Pooler output is simpler here.
        pooled_output = outputs.pooler_output

        # Apply dropout for regularization
        pooled_output = self.dropout(pooled_output)

        # Pass the pooled output through the task-specific heads
        sentiment_logits = self.sentiment_classifier(pooled_output)
        toxicity_logits = self.toxicity_classifier(pooled_output)

        return {
            'sentiment_logits': sentiment_logits,
            'toxicity_logits': toxicity_logits
        }

# --- Example Usage (Optional - for testing this script directly) ---
if __name__ == '__main__':
    from transformers import AutoTokenizer
    from dataset import CommentDataset # Assuming dataset.py is in the same directory or python path
    from torch.utils.data import DataLoader

    print("Testing CommentMTLModel...")

    # --- 1. Prepare dummy input using the Dataset and DataLoader ---
    print("Loading tokenizer and creating dummy data...")
    tokenizer = AutoTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)
    # Create a dummy CSV for testing if needed, or use a small subset of your real data
    # For simplicity, let's assume processed_comments.csv exists and works
    try:
        dataset = CommentDataset(
            data="../data/processed_comments.csv", # Adjust path if necessary
            tokenizer=tokenizer,
            max_len=128,
            toxicity_cols=['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate'] # Match dataset.py
        )
        if len(dataset) == 0:
             raise ValueError("Dataset is empty. Cannot proceed with model test.")

        # Use DataLoader to get a batch
        # Ensure dataset.py exists and PROCESSED_DATA_PATH points correctly relative to model.py
        data_loader = DataLoader(dataset, batch_size=4) # Use a small batch size like 4
        sample_batch = next(iter(data_loader))
        input_ids = sample_batch['input_ids']
        attention_mask = sample_batch['attention_mask']
        print(f"Dummy batch shapes: input_ids {input_ids.shape}, attention_mask {attention_mask.shape}")

        # --- 2. Initialize the Model ---
        print("\nInitializing model...")
        model = CommentMTLModel(
            model_name=PRE_TRAINED_MODEL_NAME,
            num_sentiment_labels=NUM_SENTIMENT_LABELS,
            num_toxicity_labels=NUM_TOXICITY_LABELS
        )

        # --- 3. Perform a Forward Pass ---
        print("Performing forward pass...")
        # Set model to evaluation mode for inference test (disables dropout)
        model.eval()
        with torch.no_grad(): # Disable gradient calculations for inference
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)

        print("\nForward pass output:")
        print(f"  Sentiment Logits Shape: {outputs['sentiment_logits'].shape}") # Should be [batch_size, num_sentiment_labels]
        print(f"  Toxicity Logits Shape: {outputs['toxicity_logits'].shape}")   # Should be [batch_size, num_toxicity_labels]
        print("\nModel test completed.")

    except FileNotFoundError:
        print("\nError: Cannot test model - processed_comments.csv not found relative to model.py.")
        print("Make sure the path in CommentDataset inside the test block is correct.")
    except Exception as e:
        print(f"\nAn error occurred during model testing: {e}")