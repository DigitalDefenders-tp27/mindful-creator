# src/train.py

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torch.optim import AdamW
from transformers import AutoTokenizer, AutoModel, get_linear_schedule_with_warmup
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, roc_auc_score
import pandas as pd
import numpy as np
from tqdm.auto import tqdm # Progress bars
import os
import time # To time epochs
import random

# Import our custom classes
# Ensure these files are in the same directory or accessible via PYTHONPATH
from dataset import CommentDataset, TOXICITY_COLS # Import toxicity cols too
from model import CommentMTLModel #

# --- Configuration ---
# Model & Data Config
PRE_TRAINED_MODEL_NAME = 'bert-base-uncased' #
MAX_LEN = 128 # Should match dataset.py
NUM_SENTIMENT_LABELS = 3 # Should match model.py
NUM_TOXICITY_LABELS = len(TOXICITY_COLS) # Should match model.py

# Paths
DATA_DIR = "../data" # Relative path from src to data
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed_comments.csv") #
OUTPUT_DIR = "../model_output" # Directory to save the trained model and results
MODEL_SAVE_PATH = os.path.join(OUTPUT_DIR, "comment_mtl_bert_best.bin")
RESULTS_SAVE_PATH = os.path.join(OUTPUT_DIR, "training_results.csv")

# Training Hyperparameters
EPOCHS = 3 # Start with a small number (e.g., 1-3) for initial testing
BATCH_SIZE = 16 # Adjust based on GPU memory (16 or 32 is common, may need 8 or 4 for MPS)
LEARNING_RATE = 2e-5 # Common learning rate for fine-tuning BERT
ADAM_EPSILON = 1e-8 # Default AdamW epsilon
MAX_GRAD_NORM = 1.0 # Gradient clipping threshold

# Loss Weights (Adjust to balance tasks, e.g., if one task learns much faster)
SENTIMENT_WEIGHT = 0.5
TOXICITY_WEIGHT = 0.5

# Data Handling
VALIDATION_SPLIT = 0.1 # Use 10% of data for validation
RANDOM_SEED = 42 # For reproducible splits, shuffling, and model initialization
# NOTE: Consider setting num_workers=0 if you encounter multiprocessing issues, especially on macOS
# It will be slower but bypasses potential spawn/fork problems.
NUM_WORKERS = 2

# --- Optional: Use a subset for faster debugging ---
DEBUG_MODE = False # Set to True to use only a small subset of data
DEBUG_SUBSET_SIZE = 2000 # Number of samples to use in debug mode

# --- Set Seed for Reproducibility ---
def set_seed(seed_value):
    random.seed(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed_value)
    # Ensure deterministic algorithms are used where possible
    # Note: some operations on GPU might still be non-deterministic
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seed(RANDOM_SEED)

# --- Helper Function for Loss Calculation (Handles Missing Labels) ---
def calculate_mtl_loss(outputs, sentiment_labels, toxicity_labels,
                       sentiment_loss_fn, toxicity_loss_fn,
                       sentiment_weight, toxicity_weight, device):
    """Calculates combined weighted loss, handling missing labels (-1)."""
    sentiment_logits = outputs['sentiment_logits'] #
    toxicity_logits = outputs['toxicity_logits'] #

    # --- Sentiment Loss ---
    # CrossEntropyLoss handles ignore_index=-1 automatically
    # Ensure labels are long type
    sentiment_loss = sentiment_loss_fn(sentiment_logits, sentiment_labels.long())

    # --- Toxicity Loss ---
    # BCEWithLogitsLoss needs manual handling of missing labels (-1)
    # Ensure labels are float type for BCEWithLogitsLoss
    toxicity_labels_float = toxicity_labels.float()

    # Create a mask for valid toxicity labels (>= 0)
    # Shape: [batch_size, num_toxicity_labels]
    valid_toxicity_mask = toxicity_labels_float >= 0.0

    # Calculate BCE loss per element (reduction='none')
    toxicity_loss_per_element = toxicity_loss_fn(toxicity_logits, toxicity_labels_float)

    # Apply the mask - zero out loss for invalid elements
    masked_toxicity_loss = toxicity_loss_per_element * valid_toxicity_mask.float()

    # Calculate the mean loss ONLY over the valid elements
    # Avoid division by zero if a batch has zero valid toxicity labels
    num_valid_toxicity_elements = valid_toxicity_mask.sum().item()
    if num_valid_toxicity_elements > 0:
        toxicity_loss = masked_toxicity_loss.sum() / num_valid_toxicity_elements
    else:
        # If no valid elements in batch, loss is 0 for this task
        toxicity_loss = torch.tensor(0.0, device=device)

    # --- Combined Weighted Loss ---
    total_loss = (sentiment_weight * sentiment_loss) + (toxicity_weight * toxicity_loss)

    return total_loss, sentiment_loss, toxicity_loss

# --- Training Function ---
def train_epoch(model, dataloader, optimizer, scheduler, device,
                sentiment_loss_fn, toxicity_loss_fn,
                sentiment_weight, toxicity_weight):
    model.train() # Set model to training mode
    total_loss, total_sentiment_loss, total_toxicity_loss = 0, 0, 0
    start_time = time.time()

    progress_bar = tqdm(dataloader, desc="Training", leave=False, unit="batch")
    for batch in progress_bar:
        # Move batch to device
        input_ids = batch['input_ids'].to(device) #
        attention_mask = batch['attention_mask'].to(device) #
        sentiment_labels = batch['sentiment_labels'].to(device) #
        toxicity_labels = batch['toxicity_labels'].to(device) #

        # Zero gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(input_ids=input_ids, attention_mask=attention_mask) #

        # Calculate loss (handling missing labels and weights)
        loss, sentiment_loss, toxicity_loss = calculate_mtl_loss(
            outputs, sentiment_labels, toxicity_labels,
            sentiment_loss_fn, toxicity_loss_fn,
            sentiment_weight, toxicity_weight, device
        )

        # Accumulate losses *before* checking requires_grad
        # Use .item() to get Python number and detach from graph
        total_loss += loss.item()
        total_sentiment_loss += sentiment_loss.item()
        total_toxicity_loss += toxicity_loss.item()

        # Check if loss requires grad (it might not if a batch had no valid labels for EITHER task)
        # This check might be overly cautious depending on loss implementation,
        # but ensures backward() is only called on tensors requiring gradients.
        if loss.requires_grad:
            # Backward pass
            loss.backward()

            # Gradient Clipping (prevents exploding gradients)
            torch.nn.utils.clip_grad_norm_(model.parameters(), MAX_GRAD_NORM)

            # Update weights
            optimizer.step()

            # Update learning rate schedule
            scheduler.step()
        else:
             # Handle case where loss calculation resulted in a tensor without grad_fn
             # This might happen if a batch contained only samples with missing labels
             # for both tasks AND loss weights resulted in zero effective contribution.
             pass # No backward pass or optimization step needed

        # Update progress bar description (optional)
        progress_bar.set_postfix({
            'Loss': f"{loss.item():.4f}",
            'Sent': f"{sentiment_loss.item():.4f}",
            'Tox': f"{toxicity_loss.item():.4f}"
        })

    avg_loss = total_loss / len(dataloader)
    avg_sentiment_loss = total_sentiment_loss / len(dataloader)
    avg_toxicity_loss = total_toxicity_loss / len(dataloader)
    elapsed_time = time.time() - start_time
    print(f"\n  Training completed in {elapsed_time:.2f}s")

    return avg_loss, avg_sentiment_loss, avg_toxicity_loss


# --- Evaluation Function ---
def eval_epoch(model, dataloader, device,
               sentiment_loss_fn, toxicity_loss_fn,
               sentiment_weight, toxicity_weight):
    model.eval() # Set model to evaluation mode
    total_loss, total_sentiment_loss, total_toxicity_loss = 0, 0, 0

    all_sentiment_preds = []
    all_sentiment_labels = []
    all_toxicity_preds = []
    all_toxicity_labels = []

    start_time = time.time()
    progress_bar = tqdm(dataloader, desc="Evaluating", leave=False, unit="batch")

    with torch.no_grad(): # Disable gradient calculations
        for batch in progress_bar:
            # Move batch to device
            input_ids = batch['input_ids'].to(device) #
            attention_mask = batch['attention_mask'].to(device) #
            sentiment_labels = batch['sentiment_labels'].to(device) #
            toxicity_labels = batch['toxicity_labels'].to(device) #

            # Forward pass
            outputs = model(input_ids=input_ids, attention_mask=attention_mask) #

            # Calculate loss (handling missing labels and weights)
            loss, sentiment_loss, toxicity_loss = calculate_mtl_loss(
                outputs, sentiment_labels, toxicity_labels,
                sentiment_loss_fn, toxicity_loss_fn,
                sentiment_weight, toxicity_weight, device
            )

            # Accumulate losses
            total_loss += loss.item()
            total_sentiment_loss += sentiment_loss.item()
            total_toxicity_loss += toxicity_loss.item()

            # --- Store predictions and labels for metrics ---
            # Sentiment: Use argmax on logits for prediction
            sentiment_preds = torch.argmax(outputs['sentiment_logits'], dim=1) #
            all_sentiment_preds.extend(sentiment_preds.cpu().numpy())
            all_sentiment_labels.extend(sentiment_labels.cpu().numpy())

            # Toxicity: Apply sigmoid to logits, then threshold for prediction
            toxicity_probs = torch.sigmoid(outputs['toxicity_logits']) #
            # Thresholding (e.g., > 0.5) can be done later during metric calculation if needed
            all_toxicity_preds.extend(toxicity_probs.cpu().numpy()) # Store probabilities
            all_toxicity_labels.extend(toxicity_labels.cpu().numpy()) # Store original labels (incl. -1)

             # Update progress bar description (optional)
            progress_bar.set_postfix({
                'Loss': f"{loss.item():.4f}",
                'Sent': f"{sentiment_loss.item():.4f}",
                'Tox': f"{toxicity_loss.item():.4f}"
             })

    avg_loss = total_loss / len(dataloader)
    avg_sentiment_loss = total_sentiment_loss / len(dataloader)
    avg_toxicity_loss = total_toxicity_loss / len(dataloader)
    elapsed_time = time.time() - start_time
    print(f"\n  Evaluation completed in {elapsed_time:.2f}s")

    # --- Calculate Metrics ---
    metrics = {}

    # Convert lists to numpy arrays
    all_sentiment_preds = np.array(all_sentiment_preds)
    all_sentiment_labels = np.array(all_sentiment_labels)
    all_toxicity_preds_probs = np.array(all_toxicity_preds) # Probabilities
    all_toxicity_labels = np.array(all_toxicity_labels)

    # 1. Sentiment Accuracy (only for valid labels)
    valid_sentiment_mask = all_sentiment_labels != -1
    if valid_sentiment_mask.sum() > 0:
        sentiment_accuracy = accuracy_score(
            all_sentiment_labels[valid_sentiment_mask],
            all_sentiment_preds[valid_sentiment_mask]
        )
        metrics['sentiment_accuracy'] = sentiment_accuracy
    else:
        metrics['sentiment_accuracy'] = 0.0

    # 2. Toxicity Metrics (only for valid labels)
    # Create a mask for rows where toxicity labels are valid (all labels >= 0)
    valid_toxicity_row_mask = (all_toxicity_labels >= 0).all(axis=1)

    if valid_toxicity_row_mask.sum() > 0:
        valid_toxicity_labels = all_toxicity_labels[valid_toxicity_row_mask]
        valid_toxicity_preds_probs = all_toxicity_preds_probs[valid_toxicity_row_mask]

        # Apply threshold to get binary predictions (0 or 1)
        THRESHOLD = 0.5
        valid_toxicity_preds_binary = (valid_toxicity_preds_probs > THRESHOLD).astype(int)

        # Calculate metrics per toxicity label
        toxicity_results = {}
        for i, label_name in enumerate(TOXICITY_COLS): #
            label_labels = valid_toxicity_labels[:, i]
            label_preds_binary = valid_toxicity_preds_binary[:, i]
            label_preds_probs = valid_toxicity_preds_probs[:, i]

            # Calculate Precision, Recall, F1-score (handle zero division)
            precision, recall, f1, _ = precision_recall_fscore_support(
                label_labels, label_preds_binary, average='binary', zero_division=0
            )
            # Calculate Accuracy
            accuracy = accuracy_score(label_labels, label_preds_binary)

            # Calculate ROC AUC (requires probabilities)
            # Handle cases where only one class is present in true labels
            try:
                roc_auc = roc_auc_score(label_labels, label_preds_probs)
            except ValueError:
                roc_auc = 0.0 # Or np.nan, or handle as appropriate

            toxicity_results[f'{label_name}_accuracy'] = accuracy
            toxicity_results[f'{label_name}_precision'] = precision
            toxicity_results[f'{label_name}_recall'] = recall
            toxicity_results[f'{label_name}_f1'] = f1
            toxicity_results[f'{label_name}_roc_auc'] = roc_auc

        metrics.update(toxicity_results) # Add individual toxicity metrics

        # Optional: Calculate overall micro/macro/weighted averages if needed
        micro_precision, micro_recall, micro_f1, _ = precision_recall_fscore_support(
            valid_toxicity_labels, valid_toxicity_preds_binary, average='micro', zero_division=0
        )
        metrics['toxicity_micro_f1'] = micro_f1
        # metrics['toxicity_micro_precision'] = micro_precision # Uncomment if needed
        # metrics['toxicity_micro_recall'] = micro_recall # Uncomment if needed

    else:
        # Add placeholders if no valid toxicity data
        metrics['toxicity_micro_f1'] = 0.0
        for label_name in TOXICITY_COLS: #
            metrics[f'{label_name}_accuracy'] = 0.0
            metrics[f'{label_name}_precision'] = 0.0
            metrics[f'{label_name}_recall'] = 0.0
            metrics[f'{label_name}_f1'] = 0.0
            metrics[f'{label_name}_roc_auc'] = 0.0


    return avg_loss, avg_sentiment_loss, avg_toxicity_loss, metrics


# --- Main Execution Guard ---
# This ensures the following code only runs when the script is executed directly
# and not when imported by spawned processes in multiprocessing.
if __name__ == '__main__':

    # --- Ensure output directory exists ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- Device Setup ---
    print("\n--- Setting Up Device ---")
    # Check for CUDA (NVIDIA GPU)
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print(f"Using CUDA GPU: {torch.cuda.get_device_name(0)}")
    # Check for MPS (Apple Silicon GPU)
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
        print("Using Apple Silicon GPU (MPS)")
        # Optional: Clear cache if encountering MPS memory issues
        # torch.mps.empty_cache()
    # Fallback to CPU
    else:
        device = torch.device("cpu")
        print("CUDA/MPS not available. Using CPU")


    # --- 1. Load and Split Data ---
    print("\n--- Loading and Splitting Data ---")
    try:
        df = pd.read_csv(PROCESSED_DATA_PATH)
        # Basic cleaning: drop rows where 'text' might be NaN
        df = df.dropna(subset=['text']).reset_index(drop=True) # provides text col
        print(f"Loaded {len(df)} comments from {PROCESSED_DATA_PATH}")

        if DEBUG_MODE:
            print(f"DEBUG MODE: Using subset of {DEBUG_SUBSET_SIZE} samples.")
            if DEBUG_SUBSET_SIZE >= len(df):
                 print("Warning: Debug subset size is larger than total data. Using all data.")
            df = df.sample(n=min(DEBUG_SUBSET_SIZE, len(df)), random_state=RANDOM_SEED).reset_index(drop=True)

        # Split data into Train and Validation sets
        df_train, df_val = train_test_split(
            df,
            test_size=VALIDATION_SPLIT,
            random_state=RANDOM_SEED
        )
        # Clean up original df to save memory
        del df
        print(f"Training set size: {len(df_train)}")
        print(f"Validation set size: {len(df_val)}")

    except FileNotFoundError:
        print(f"Error: Processed data file not found at {PROCESSED_DATA_PATH}")
        print("Please ensure 'preprocess_data.py' has been run successfully.")
        exit() # Exit if data is missing
    except Exception as e:
        print(f"An error occurred during data loading/splitting: {e}")
        exit()


    # --- 2. Initialize Tokenizer, Datasets, DataLoaders ---
    print("\n--- Initializing Tokenizer, Datasets, DataLoaders ---")
    try:
        tokenizer = AutoTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)

        train_dataset = CommentDataset(
            data=df_train, # Pass DataFrame directly
            tokenizer=tokenizer,
            max_len=MAX_LEN,
            toxicity_cols=TOXICITY_COLS #
        )
        # Clean up df_train
        del df_train

        val_dataset = CommentDataset(
            data=df_val, # Pass DataFrame directly
            tokenizer=tokenizer,
            max_len=MAX_LEN,
            toxicity_cols=TOXICITY_COLS #
        )
        # Clean up df_val
        del df_val

        train_dataloader = DataLoader(
            train_dataset,
            batch_size=BATCH_SIZE,
            shuffle=True, # Shuffle training data
            num_workers=NUM_WORKERS, # Use background workers
            pin_memory=True # Helps speed up data transfer to GPU if using CUDA
        )

        val_dataloader = DataLoader(
            val_dataset,
            batch_size=BATCH_SIZE,
            shuffle=False, # No need to shuffle validation data
            num_workers=NUM_WORKERS,
            pin_memory=True
        )
        print("Tokenizer, Datasets, and DataLoaders created.")
    except Exception as e:
        print(f"An error occurred during tokenizer/dataset/dataloader initialization: {e}")
        exit()

    # --- 3. Initialize Model ---
    print("\n--- Initializing Model ---")
    try:
        model = CommentMTLModel(
            model_name=PRE_TRAINED_MODEL_NAME,
            num_sentiment_labels=NUM_SENTIMENT_LABELS, #
            num_toxicity_labels=NUM_TOXICITY_LABELS #
        )
        model.to(device) # Move model to GPU or CPU
        print(f"Model '{PRE_TRAINED_MODEL_NAME}' loaded and moved to {device}.")
    except Exception as e:
        print(f"An error occurred during model initialization: {e}")
        exit()

    # --- 4. Define Loss Functions ---
    print("\n--- Defining Loss Functions ---")
    # Sentiment: Multi-class classification. Ignore index -1 (missing label)
    sentiment_loss_fn = nn.CrossEntropyLoss(ignore_index=-1).to(device)

    # Toxicity: Multi-label classification. Handle -1 manually in calculate_mtl_loss.
    # Use BCEWithLogitsLoss for numerical stability. Calculate loss per element.
    toxicity_loss_fn = nn.BCEWithLogitsLoss(reduction='none').to(device)

    print("Loss functions defined (CrossEntropyLoss for sentiment, BCEWithLogitsLoss for toxicity).")

    # --- 5. Define Optimizer and Scheduler ---
    print("\n--- Defining Optimizer and Scheduler ---")
    # AdamW is recommended for Transformers
    optimizer = AdamW(model.parameters(), lr=LEARNING_RATE, eps=ADAM_EPSILON)

    # Calculate total training steps for scheduler
    # Consider potential partial last batch if drop_last=False (default) in DataLoader
    # num_update_steps_per_epoch = len(train_dataloader) # This is correct
    num_update_steps_per_epoch = -(-len(train_dataset) // BATCH_SIZE) # More robust way to calculate steps per epoch
    total_steps = num_update_steps_per_epoch * EPOCHS

    # Learning rate scheduler (linear decay with optional warmup)
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=0, # Optional: e.g., int(0.1 * total_steps)
        num_training_steps=total_steps
    )
    print(f"Optimizer: AdamW (LR={LEARNING_RATE}). Scheduler: Linear warmup/decay over {total_steps} steps.")


    # --- 6. Main Training Loop ---
    print("\n--- Starting Training ---")

    best_val_loss = float('inf') # Keep track of best validation loss for checkpointing
    training_stats = [] # Store stats for each epoch

    for epoch in range(EPOCHS):
        epoch_start_time = time.time()
        print(f"\nEpoch {epoch + 1}/{EPOCHS}")
        print("-" * 30)

        # --- Training ---
        avg_train_loss, avg_train_sent_loss, avg_train_tox_loss = train_epoch(
            model, train_dataloader, optimizer, scheduler, device,
            sentiment_loss_fn, toxicity_loss_fn,
            SENTIMENT_WEIGHT, TOXICITY_WEIGHT
        )

        # --- Evaluation ---
        avg_val_loss, avg_val_sent_loss, avg_val_tox_loss, val_metrics = eval_epoch(
            model, val_dataloader, device,
            sentiment_loss_fn, toxicity_loss_fn,
            SENTIMENT_WEIGHT, TOXICITY_WEIGHT
        )

        epoch_time = time.time() - epoch_start_time
        print(f"\n--- Epoch {epoch + 1} Summary ---")
        print(f"Time               : {epoch_time:.2f}s")
        print(f"Avg Train Loss     : {avg_train_loss:.4f} | Sent: {avg_train_sent_loss:.4f} | Tox: {avg_train_tox_loss:.4f}")
        print(f"Avg Val Loss       : {avg_val_loss:.4f} | Sent: {avg_val_sent_loss:.4f} | Tox: {avg_val_tox_loss:.4f}")
        print(f"Val Sentiment Acc  : {val_metrics.get('sentiment_accuracy', 0.0):.4f}")
        print(f"Val Toxicity F1(m): {val_metrics.get('toxicity_micro_f1', 0.0):.4f}")
        # Optionally print more toxicity metrics if needed
        # print(f"Val Toxic F1: {val_metrics.get('toxic_f1', 0.0):.4f}")


        # Store epoch stats
        stats = {
            'epoch': epoch + 1,
            'train_loss': avg_train_loss,
            'train_sentiment_loss': avg_train_sent_loss,
            'train_toxicity_loss': avg_train_tox_loss,
            'val_loss': avg_val_loss,
            'val_sentiment_loss': avg_val_sent_loss,
            'val_toxicity_loss': avg_val_tox_loss,
            'val_time_seconds': epoch_time
        }
        stats.update(val_metrics) # Add all calculated validation metrics
        training_stats.append(stats)


        # --- Checkpoint Saving ---
        # Save the model if validation loss has improved
        if avg_val_loss < best_val_loss:
            print(f"Validation loss improved ({best_val_loss:.4f} --> {avg_val_loss:.4f}). Saving model...")
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            # Consider also saving tokenizer state if needed, although usually static for fine-tuning
            # tokenizer.save_pretrained(OUTPUT_DIR)
            best_val_loss = avg_val_loss
            print(f"Best model saved to {MODEL_SAVE_PATH}")
        else:
            print(f"Validation loss ({avg_val_loss:.4f}) did not improve from best ({best_val_loss:.4f}).")


    print("\n--- Training Finished ---")

    # --- 7. Save Training Stats ---
    try:
        stats_df = pd.DataFrame(training_stats)
        stats_df.set_index('epoch', inplace=True)
        stats_df.to_csv(RESULTS_SAVE_PATH)
        print(f"\nTraining results saved to {RESULTS_SAVE_PATH}")
    except Exception as e:
        print(f"Error saving training results: {e}")

    # --- Optional: Load best model and perform final evaluation/testing ---
    # print("\n--- Loading Best Model for Final Check ---")
    # model.load_state_dict(torch.load(MODEL_SAVE_PATH))
    # model.to(device)
    # # ... potentially run eval_epoch again on validation or a separate test set ...

    print("\nScript completed.")