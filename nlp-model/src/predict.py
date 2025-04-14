# src/predict.py

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer
import numpy as np
import os
import matplotlib.pyplot as plt # Import matplotlib

# Import necessary components from your project files
# Ensure these files are in the same directory or adjust import paths
from model import CommentMTLModel # Needs CommentMTLModel class [cite: uploaded:src/model.py]
from preprocess_data import preprocess_text # Needs the cleaning function [cite: uploaded:src/preprocess_data.py]
# TOXICITY_COLS might be defined in dataset.py or you can define it here
try:
    from dataset import TOXICITY_COLS
except ImportError:
    # Define fallback if not found (ensure this matches training)
    TOXICITY_COLS = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    print("Warning: Could not import TOXICITY_COLS from dataset.py, using default list.")


# --- Configuration ---
PRE_TRAINED_MODEL_NAME = 'bert-base-uncased'
MAX_LEN = 128 # Should match training MAX_LEN
NUM_SENTIMENT_LABELS = 3
NUM_TOXICITY_LABELS = len(TOXICITY_COLS)
MODEL_DIR = "../model_output" # Relative path to model directory
MODEL_LOAD_PATH = os.path.join(MODEL_DIR, "comment_mtl_bert_best.bin")
SENTIMENT_MAP = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
TOXICITY_THRESHOLD = 0.5 # Threshold to decide if a toxicity probability is considered 'present'

# --- Device Setup ---
print("--- Setting Up Device ---")
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Using CUDA GPU: {torch.cuda.get_device_name(0)}")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
    print("Using Apple Silicon GPU (MPS)")
else:
    device = torch.device("cpu")
    print("Using CPU")

# --- Load Tokenizer ---
print("\n--- Loading Tokenizer ---")
try:
    tokenizer = AutoTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)
    print(f"Tokenizer '{PRE_TRAINED_MODEL_NAME}' loaded.")
except Exception as e:
    print(f"Error loading tokenizer: {e}")
    exit()

# --- Load Model ---
print("\n--- Loading Model ---")
try:
    model = CommentMTLModel(
        model_name=PRE_TRAINED_MODEL_NAME,
        num_sentiment_labels=NUM_SENTIMENT_LABELS,
        num_toxicity_labels=NUM_TOXICITY_LABELS
    )
    # Load state dict - use map_location='cpu' if model was trained on GPU but loading on CPU
    model.load_state_dict(torch.load(MODEL_LOAD_PATH, map_location=device))
    model.to(device) # Move model to the target device
    model.eval() # Set model to evaluation mode IMPORTANT!
    print(f"Model loaded from {MODEL_LOAD_PATH} and moved to {device}.")
except FileNotFoundError:
    print(f"Error: Model file not found at {MODEL_LOAD_PATH}")
    exit()
except Exception as e:
    print(f"An error occurred during model loading: {e}")
    exit()

# --- Chart Generation Functions ---
'''
def generate_sentiment_pie_chart(sentiment_probs, sentiment_map):
    """Generates and displays a pie chart for sentiment probabilities."""
    labels = [sentiment_map.get(i, f"Unknown_{i}") for i in range(len(sentiment_probs))]
    sizes = sentiment_probs * 100 # Convert probs to percentages

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99']) # Red, Blue, Green-ish
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Sentiment Prediction Distribution')
    plt.show()

def generate_toxicity_bar_chart(toxicity_probs, toxicity_cols):
    """Generates and displays a bar chart for toxicity probabilities."""
    fig, ax = plt.subplots(figsize=(10, 6)) # Adjust figure size if needed
    y_pos = np.arange(len(toxicity_cols))
    ax.barh(y_pos, toxicity_probs, align='center', color='skyblue')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(toxicity_cols)
    ax.invert_yaxis()  # Labels read top-to-bottom
    ax.set_xlabel('Probability')
    ax.set_title('Toxicity Type Probabilities')
    ax.set_xlim(0, 1) # Probabilities range from 0 to 1

    # Add probability values on bars
    for index, value in enumerate(toxicity_probs):
        plt.text(value + 0.01, index, f'{value:.3f}')

    plt.tight_layout() # Adjust layout
    plt.show()
'''

# --- Prediction Function ---
def predict_text(text):
    """
    Takes raw text, preprocesses, tokenizes, predicts sentiment and toxicity.
    Returns predictions in a dictionary.
    """
    if not text or not isinstance(text, str):
        return {"error": "Invalid input text"}

    # 1. Preprocess
    cleaned_text = preprocess_text(text) # Use the same function as training [cite: uploaded:src/preprocess_data.py]
    if not cleaned_text:
        return {"error": "Text empty after preprocessing"}

    # 2. Tokenize
    encoding = tokenizer.encode_plus(
        cleaned_text,
        add_special_tokens=True, # Add '[CLS]' and '[SEP]'
        max_length=MAX_LEN,
        padding='max_length', # Pad/truncate to max_length
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt', # Return PyTorch tensors
    )

    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    # 3. Predict
    with torch.no_grad(): # Disable gradient calculations
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)

        # 4. Process Outputs
        # Sentiment
        sentiment_logits = outputs['sentiment_logits']
        sentiment_probs_squeezed = F.softmax(sentiment_logits, dim=1).squeeze()
        
        # Use the squeezed tensor for index, confidence, AND the list for charting
        sentiment_pred_idx = torch.argmax(sentiment_probs_squeezed).item()
        predicted_sentiment = SENTIMENT_MAP.get(sentiment_pred_idx, "Unknown")
        sentiment_confidence = sentiment_probs_squeezed.max().item()
        sentiment_probs_list = sentiment_probs_squeezed.cpu().numpy() # NOW creates a 1D numpy array

        # Toxicity
        toxicity_logits = outputs['toxicity_logits']
        # Squeeze toxicity probs too, just to be safe and consistent
        toxicity_probs_squeezed = torch.sigmoid(toxicity_logits).squeeze() # Shape becomes [6]
        toxicity_probs_list = toxicity_probs_squeezed.cpu().numpy() # Use the squeezed version
        toxicity_predictions = (toxicity_probs_list > TOXICITY_THRESHOLD).astype(int)

        toxicity_results = {}
        for i, label in enumerate(TOXICITY_COLS):
            toxicity_results[label] = {
                "probability": f"{toxicity_probs_list[i]:.4f}",
                "prediction": "Present" if toxicity_predictions[i] == 1 else "Absent"
            }

    return {
        "input_text": text,
        "cleaned_text": cleaned_text,
        "predicted_sentiment": predicted_sentiment,
        "sentiment_confidence": f"{sentiment_confidence:.4f}",
        "toxicity_details": toxicity_results,
        "raw_sentiment_probs": sentiment_probs_list, # Added for pie chart
        "raw_toxicity_probs": toxicity_probs_list   # Added for bar chart
    }

# --- Main Loop for Interactive Input ---
'''
if __name__ == "__main__":
    print("\n--- Interactive Prediction ---")
    print("Enter text below to get predictions. Type 'quit' to exit.")

    while True:
        try:
            user_input = input("Enter text: ")
            if user_input.lower() == 'quit':
                break

            if not user_input:
                print("Please enter some text.")
                continue

            results = predict_text(user_input)

            if "error" in results:
                print(f"Error: {results['error']}")
            else:
                print("\n--- Prediction Results ---")
                print(f"Input Text: {results['input_text']}")
                # print(f"Cleaned Text: {results['cleaned_text']}") # Optional: show cleaned text
                print(f"Predicted Sentiment: {results['predicted_sentiment']} (Confidence: {results['sentiment_confidence']})")
                print("Toxicity Predictions:")
                for label, details in results['toxicity_details'].items():
                    print(f"  - {label:<15}: {details['prediction']} (Prob: {details['probability']})")
                print("-" * 26)

                # --- Generate Charts ---
                print("Generating charts...")
                # Sentiment Pie Chart
                generate_sentiment_pie_chart(results['raw_sentiment_probs'], SENTIMENT_MAP)

                # Toxicity Bar Chart
                generate_toxicity_bar_chart(results['raw_toxicity_probs'], TOXICITY_COLS)
                print("Charts displayed.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # Optionally add more robust error handling or logging

    print("\nExiting prediction script.") '''