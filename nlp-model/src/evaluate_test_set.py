# src/evaluate_test_set.py

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from transformers import AutoTokenizer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score, classification_report
import pandas as pd
import numpy as np
from tqdm.auto import tqdm # Progress bars
import os
import time

# Import necessary components from your project files
# Make sure dataset.py defines CommentDataset correctly and exports TOXICITY_COLS
from dataset import CommentDataset, TOXICITY_COLS
from model import CommentMTLModel
# Make sure preprocess_data.py defines preprocess_text correctly
from preprocess_data import preprocess_text

# --- Configuration ---
PRE_TRAINED_MODEL_NAME = 'bert-base-uncased'
MAX_LEN = 128
NUM_SENTIMENT_LABELS = 3
NUM_TOXICITY_LABELS = len(TOXICITY_COLS)
BATCH_SIZE = 16

# Paths
DATA_DIR = "../data"
# Adjust Jigsaw test filenames if needed
TEST_TEXT_PATH = os.path.join(DATA_DIR, "jigsaw_test.csv")
TEST_LABELS_PATH = os.path.join(DATA_DIR, "test_labels.csv") # Ensure this file exists and has 'id' and toxicity columns

MODEL_DIR = "../model_output"
MODEL_LOAD_PATH = os.path.join(MODEL_DIR, "comment_mtl_bert_best.bin")

RESULTS_DIR = "../results"
TEST_RESULTS_PATH = os.path.join(RESULTS_DIR, "test_set_evaluation_metrics.txt")
# Removed TEST_PREDICTIONS_PATH as we are not saving per-ID predictions

# --- Ensure results directory exists ---
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- Device Setup ---
print("\n--- Setting Up Device ---")
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Using CUDA GPU: {torch.cuda.get_device_name(0)}")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
    print("Using Apple Silicon GPU (MPS)")
else:
    device = torch.device("cpu")
    print("Using CPU")

# --- 1. Load Tokenizer ---
print("\n--- Loading Tokenizer ---")
try:
    tokenizer = AutoTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)
    print(f"Tokenizer '{PRE_TRAINED_MODEL_NAME}' loaded.")
except Exception as e:
    print(f"Error loading tokenizer: {e}")
    exit()

# --- 2. Load Model ---
print("\n--- Loading Model ---")
try:
    model = CommentMTLModel(
        model_name=PRE_TRAINED_MODEL_NAME,
        num_sentiment_labels=NUM_SENTIMENT_LABELS,
        num_toxicity_labels=NUM_TOXICITY_LABELS
    )
    model.load_state_dict(torch.load(MODEL_LOAD_PATH, map_location=torch.device('cpu')))
    model.to(device)
    model.eval()
    print(f"Model loaded from {MODEL_LOAD_PATH} and moved to {device}.")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_LOAD_PATH}")
    print("Ensure training was completed and the best model was saved.")
    exit()
except Exception as e:
    print(f"An error occurred during model loading: {e}")
    exit()

# --- 3. Load and Preprocess Test Data ---
print("\n--- Loading and Preprocessing Test Data ---")
try:
    df_test_text = pd.read_csv(TEST_TEXT_PATH)
    df_test_labels = pd.read_csv(TEST_LABELS_PATH)

    # Merge text and labels based on 'id'
    # Keep 'id' temporarily for merging, but we won't pass it to the dataset or use it later
    df_test = pd.merge(df_test_text[['id', 'comment_text']], df_test_labels, on='id')

    print(f"Loaded {len(df_test)} test comments.")

    # Rename for consistency with dataset expectations
    df_test.rename(columns={'comment_text': 'text'}, inplace=True)

    print("Cleaning test comments...")
    df_test['text'] = df_test['text'].apply(preprocess_text)

    # Add placeholder for sentiment labels if your dataset expects it
    # Ensure your CommentDataset handles cases where labels might be missing for certain tasks
    if 'sentiment' not in df_test.columns:
         df_test['sentiment'] = -1 # Placeholder

    # Select only columns needed by CommentDataset (text and actual labels)
    # Make sure TOXICITY_COLS are present in df_test from the merge
    required_cols = ['text', 'sentiment'] + TOXICITY_COLS
    # Check if all required columns are present after merge
    missing_cols = [col for col in required_cols if col not in df_test.columns and col != 'sentiment'] # sentiment might be added
    if missing_cols:
        print(f"Error: Missing required label columns in merged test data: {missing_cols}")
        exit()

    # Keep only the columns CommentDataset expects (modify based on your dataset.py)
    df_test_final = df_test[required_cols]

    print("Test data loaded and cleaned.")

except FileNotFoundError:
    print(f"Error: Test data file not found at {TEST_TEXT_PATH} or {TEST_LABELS_PATH}")
    exit()
except KeyError as e:
    print(f"Error: Column mismatch during data processing - likely 'id' or label columns missing. Check CSV files. Details: {e}")
    exit()
except Exception as e:
    print(f"An error occurred during data loading/preprocessing: {e}")
    exit()


# --- 4. Create Test Dataset and DataLoader ---
print("\n--- Creating Test Dataset and DataLoader ---")
try:
    test_dataset = CommentDataset(
        # Pass the final DataFrame with only necessary columns
        data=df_test_final,
        tokenizer=tokenizer,
        max_len=MAX_LEN,
        toxicity_cols=TOXICITY_COLS # Ensure CommentDataset uses this list
    )

    test_dataloader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0
    )
    print("Test DataLoader created.")
except Exception as e:
    print(f"Error creating Dataset/DataLoader: {e}")
    print("Check if df_test_final DataFrame has the correct columns needed by CommentDataset ('text', 'sentiment', toxicity columns).")
    exit()


# --- 5. Run Inference ---
print("\n--- Running Inference on Test Set ---")
# Removed all_comment_ids list
all_sentiment_preds = []
all_toxicity_preds = [] # Store probabilities
all_toxicity_labels = [] # Store true labels if available in test set

start_time = time.time()
progress_bar = tqdm(test_dataloader, desc="Evaluating Test Set", leave=False, unit="batch")

with torch.no_grad():
    for batch in progress_bar:
        # Move batch to device
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        # Get labels from the batch (ensure they are returned by your dataset)
        # These might be tensors of -1 if labels are missing for certain tasks/samples
        sentiment_labels = batch['sentiment_labels']
        toxicity_labels = batch['toxicity_labels']

        # Removed reference to batch['comment_id']

        # Forward pass
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)

        # Store predictions and labels for metric calculation
        sentiment_preds = torch.argmax(outputs['sentiment_logits'], dim=1)
        all_sentiment_preds.extend(sentiment_preds.cpu().numpy())

        toxicity_probs = torch.sigmoid(outputs['toxicity_logits'])
        all_toxicity_preds.extend(toxicity_probs.cpu().numpy())

        # Store true labels
        all_toxicity_labels.extend(toxicity_labels.numpy())
        # Removed extension of all_comment_ids

elapsed_time = time.time() - start_time
print(f"\nInference completed in {elapsed_time:.2f}s")

# --- 6. Calculate and Report Metrics ---
print("\n--- Calculating Metrics ---")

# Convert lists to numpy arrays
all_sentiment_preds = np.array(all_sentiment_preds)
all_toxicity_preds_probs = np.array(all_toxicity_preds)
all_toxicity_labels = np.array(all_toxicity_labels)

# Filter out rows where Jigsaw labels are -1 (comments not used for scoring)
# Ensure all_toxicity_labels has the correct shape (N_samples, N_toxicity_labels)
if all_toxicity_labels.ndim == 2:
    valid_toxicity_mask = (all_toxicity_labels >= 0).all(axis=1)
    print(f"Total test samples processed: {len(all_toxicity_labels)}")
    print(f"Valid samples for toxicity scoring (labels >= 0): {valid_toxicity_mask.sum()}")
else:
    print("Warning: Unexpected shape for all_toxicity_labels. Skipping toxicity metrics calculation.")
    valid_toxicity_mask = np.array([False] * len(all_toxicity_labels)) # Create a mask of all False


if valid_toxicity_mask.sum() > 0:
    valid_toxicity_labels = all_toxicity_labels[valid_toxicity_mask]
    valid_toxicity_preds_probs = all_toxicity_preds_probs[valid_toxicity_mask]

    # Apply threshold to get binary predictions for metrics like Accuracy, F1
    THRESHOLD = 0.5
    valid_toxicity_preds_binary = (valid_toxicity_preds_probs > THRESHOLD).astype(int)

    # Calculate overall metrics
    micro_f1 = precision_recall_fscore_support(valid_toxicity_labels, valid_toxicity_preds_binary, average='micro', zero_division=0)[2]
    macro_f1 = precision_recall_fscore_support(valid_toxicity_labels, valid_toxicity_preds_binary, average='macro', zero_division=0)[2]
    weighted_f1 = precision_recall_fscore_support(valid_toxicity_labels, valid_toxicity_preds_binary, average='weighted', zero_division=0)[2]

    print("\n--- Overall Toxicity Metrics (on valid test samples) ---")
    print(f"Micro F1-Score    : {micro_f1:.4f}")
    print(f"Macro F1-Score    : {macro_f1:.4f}")
    print(f"Weighted F1-Score : {weighted_f1:.4f}")

    # Calculate metrics per toxicity label
    print("\n--- Per-Label Toxicity Metrics ---")
    report = classification_report(
        valid_toxicity_labels,
        valid_toxicity_preds_binary,
        target_names=TOXICITY_COLS,
        zero_division=0,
        digits=4
    )
    print(report)

    # Calculate ROC AUC per label
    print("\n--- Per-Label ROC AUC ---")
    roc_auc_results = {}
    for i, label_name in enumerate(TOXICITY_COLS):
        # Check if there are both classes present for the label
        if len(np.unique(valid_toxicity_labels[:, i])) > 1:
             try:
                 roc_auc = roc_auc_score(valid_toxicity_labels[:, i], valid_toxicity_preds_probs[:, i])
                 roc_auc_results[label_name] = roc_auc
                 print(f"{label_name:<15}: {roc_auc:.4f}")
             except Exception as e: # Catch potential errors during calculation
                 print(f"{label_name:<15}: Error calculating ROC AUC - {e}")
                 roc_auc_results[label_name] = np.nan
        else:
            print(f"{label_name:<15}: Cannot compute ROC AUC (only one class present in labels)")
            roc_auc_results[label_name] = np.nan


    # --- Save Metrics to File ---
    print(f"\n--- Saving Metrics to {TEST_RESULTS_PATH} ---")
    try:
        with open(TEST_RESULTS_PATH, 'w') as f:
            f.write("--- Overall Toxicity Metrics (on valid test samples) ---\n")
            f.write(f"Micro F1-Score    : {micro_f1:.4f}\n")
            f.write(f"Macro F1-Score    : {macro_f1:.4f}\n")
            f.write(f"Weighted F1-Score : {weighted_f1:.4f}\n\n")
            f.write("--- Per-Label Toxicity Metrics ---\n")
            f.write(report)
            f.write("\n\n--- Per-Label ROC AUC ---\n")
            for label, score in roc_auc_results.items():
                score_str = f"{score:.4f}" if not np.isnan(score) else "N/A"
                f.write(f"{label:<15}: {score_str}\n")
        print("Metrics saved.")
    except Exception as e:
        print(f"Error saving metrics to file: {e}")

    # --- Removed the section for saving predictions ---

else:
    print("No valid samples found in the test set for toxicity scoring (all labels might be -1 or data shape issue).")

# Note: Sentiment metrics calculation would go here if sentiment labels were available and valid.
print("\nEvaluation script finished.")