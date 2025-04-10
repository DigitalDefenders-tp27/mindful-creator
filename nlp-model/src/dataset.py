# src/dataset.py

import torch
import pandas as pd
from torch.utils.data import Dataset
from transformers import BertTokenizer, AutoTokenizer # Use AutoTokenizer for flexibility
import os

# --- Configuration ---
# You might want to move these to a central config file later
DATA_DIR = "../data" # Relative path from src to data
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed_comments.csv")
PRE_TRAINED_MODEL_NAME = 'bert-base-uncased' # Or another BERT variant
MAX_LEN = 128 # Max sequence length for BERT input

# Define toxicity columns - should match preprocess_data.py
TOXICITY_COLS = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']

class CommentDataset(Dataset):
    """
    PyTorch Dataset class for loading comment data for Multi-Task Learning.
    Handles tokenization and label formatting.
    """
    def __init__(self, data, tokenizer, max_len, toxicity_cols):
        """
        Args:
            data_path (str): Path to the processed CSV file.
            tokenizer: Hugging Face tokenizer instance.
            max_len (int): Maximum sequence length for tokenization.
            toxicity_cols (list): List of column names for toxicity labels.
        """
        try:
            self.data = data.copy()
            #self.data = pd.read_csv(data)
            # Drop rows where text might be missing after loading (belt-and-braces)
            self.data = self.data.dropna(subset=['text']).reset_index(drop=True)
            print(f"Loaded dataset with {len(self.data)} samples from {data}")
        except FileNotFoundError:
            print(f"Error: Processed data file not found at {data}")
            # Handle error appropriately, maybe raise exception or exit
            self.data = pd.DataFrame() # Create empty dataframe
            return # Stop initialization if file not found

        self.tokenizer = tokenizer
        self.max_len = max_len
        self.toxicity_cols = toxicity_cols
        self.sentiment_col = 'sentiment' # Name of the sentiment column

    def __len__(self):
        """Returns the number of items in the dataset."""
        return len(self.data)

    def __getitem__(self, index):
        """
        Retrieves one item (comment text and labels) from the dataset
        and prepares it for the model.

        Args:
            index (int): Index of the data point to retrieve.

        Returns:
            dict: A dictionary containing:
                'input_ids': Token IDs for BERT.
                'attention_mask': Attention mask for BERT.
                'sentiment_labels': Sentiment label (0, 1, or 2). -1 if missing.
                'toxicity_labels': Tensor of toxicity labels (0 or 1). -1 if missing.
                'text': The original comment text (optional, useful for debugging).
        """
        if index >= len(self.data):
             raise IndexError(f"Index {index} out of bounds for dataset with length {len(self.data)}")

        comment = self.data.iloc[index]
        text = str(comment['text']) # Ensure text is string

        # Tokenize the text
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,    # Add '[CLS]' and '[SEP]'
            max_length=self.max_len,    # Pad & truncate to max_len
            padding='max_length',       # Pad to max_length
            truncation=True,            # Truncate to max_length if longer
            return_attention_mask=True, # Return attention mask
            return_tensors='pt',        # Return PyTorch tensors
        )

        # --- Prepare Labels ---
        # Sentiment Label: Use long type for CrossEntropyLoss. Use -1 for missing.
        sentiment_label = int(comment[self.sentiment_col])
        sentiment_label_tensor = torch.tensor(sentiment_label, dtype=torch.long)

        # Toxicity Labels: Use float type for BCEWithLogitsLoss. Use -1 for missing.
        # We keep -1 here; the loss function will need to ignore these later.
        toxicity_labels = comment[self.toxicity_cols].values.astype(float)
        toxicity_labels_tensor = torch.tensor(toxicity_labels, dtype=torch.float)

        return {
            # Squeeze removes unnecessary batch dimension added by encode_plus when processing single item
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'sentiment_labels': sentiment_label_tensor,
            'toxicity_labels': toxicity_labels_tensor,
            'text': text # Optional: return text for inspection
        }

# --- Example Usage (Optional - for testing this script directly) ---
if __name__ == '__main__':
    print("Testing CommentDataset...")

    # Initialize tokenizer
    print(f"Loading tokenizer: {PRE_TRAINED_MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)

    # Create dataset instance
    print(f"Creating dataset from: {PROCESSED_DATA_PATH}")
    dataset = CommentDataset(
        data_path=PROCESSED_DATA_PATH,
        tokenizer=tokenizer,
        max_len=MAX_LEN,
        toxicity_cols=TOXICITY_COLS
    )

    # Check if dataset loaded successfully
    if len(dataset) > 0:
        print(f"Dataset loaded successfully with {len(dataset)} items.")

        # Get a sample item
        sample_item = dataset[0] # Get the first item

        print("\nSample Item:")
        print(f" Text: {sample_item['text']}")
        print(f" Input IDs shape: {sample_item['input_ids'].shape}")
        print(f" Attention Mask shape: {sample_item['attention_mask'].shape}")
        print(f" Sentiment Label: {sample_item['sentiment_labels']} (dtype: {sample_item['sentiment_labels'].dtype})")
        print(f" Toxicity Labels: {sample_item['toxicity_labels']} (dtype: {sample_item['toxicity_labels'].dtype})")

        # Test DataLoader
        from torch.utils.data import DataLoader
        print("\nTesting DataLoader...")
        data_loader = DataLoader(dataset, batch_size=2, shuffle=True) # Small batch size for testing
        sample_batch = next(iter(data_loader)) # Get one batch

        print("\nSample Batch (batch_size=2):")
        print(f" Input IDs shape: {sample_batch['input_ids'].shape}") # Should be [2, max_len]
        print(f" Attention Mask shape: {sample_batch['attention_mask'].shape}") # Should be [2, max_len]
        print(f" Sentiment Labels: {sample_batch['sentiment_labels']}") # Should be [2]
        print(f" Toxicity Labels shape: {sample_batch['toxicity_labels'].shape}") # Should be [2, num_toxicity_labels]

    else:
        print("Dataset is empty, likely due to file not found or loading error.")