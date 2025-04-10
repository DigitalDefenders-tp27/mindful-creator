import pandas as pd
import re
import os

# --- Configuration ---
DATA_DIR = "../data" # Relative path from src to data
SENTIMENT140_PATH = os.path.join(DATA_DIR, "sentiment140.csv")
JIGSAW_PATH = os.path.join(DATA_DIR, "jigsaw_train.csv")
OUTPUT_PATH = os.path.join(DATA_DIR, "processed_comments.csv")

# Define toxicity columns from Jigsaw
TOXICITY_COLS = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']

# --- Text Cleaning Function ---
def preprocess_text(text):
    """Applies basic cleaning steps to text."""
    if not isinstance(text, str):
        return "" # Handle potential non-string data
    text = text.lower() # Lowercase
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE) # Remove URLs
    text = re.sub(r'\@\w+', '', text) # Remove mentions
    text = re.sub(r'\#\w+', '', text) # Remove hashtags (or keep the word if preferred)
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation (adjust if needed)
    text = re.sub(r'\s+', ' ', text).strip() # Remove extra whitespace
    return text

# --- Load and Process Sentiment140 ---
print("Processing Sentiment140...")
try:
    # Sentiment140 often has no header, specific encoding issues
    df_sent = pd.read_csv(
        SENTIMENT140_PATH,
        encoding='latin-1', # Common encoding for this dataset
        header=None,       # No header row
        names=['sentiment_raw', 'id', 'date', 'query', 'user', 'text'] # Assign column names
    )
    print(f"Loaded Sentiment140: {len(df_sent)} rows")

    # Select relevant columns
    df_sent = df_sent[['sentiment_raw', 'text']]

    # Preprocess text
    df_sent['text'] = df_sent['text'].apply(preprocess_text)

    # Map sentiment: 0 -> 0 (Negative), 4 -> 2 (Positive)
    # We'll use -1 for missing labels later
    df_sent['sentiment'] = df_sent['sentiment_raw'].map({0: 0, 4: 2})

    # Add toxicity columns, mark as missing (-1) since Sentiment140 doesn't have them
    for col in TOXICITY_COLS:
        df_sent[col] = -1 # Indicate missing label for toxicity task

    # Keep only necessary columns
    df_sent = df_sent[['text', 'sentiment'] + TOXICITY_COLS]
    print(f"Processed Sentiment140: {len(df_sent)} rows")

except FileNotFoundError:
    print(f"Error: Sentiment140 file not found at {SENTIMENT140_PATH}")
    df_sent = pd.DataFrame() # Create empty dataframe to proceed

# --- Load and Process Jigsaw ---
print("\nProcessing Jigsaw...")
try:
    df_jigsaw = pd.read_csv(JIGSAW_PATH)
    print(f"Loaded Jigsaw: {len(df_jigsaw)} rows")

    # Select relevant columns (use 'comment_text' as 'text')
    df_jigsaw = df_jigsaw[['comment_text'] + TOXICITY_COLS]
    df_jigsaw.rename(columns={'comment_text': 'text'}, inplace=True)

    # Preprocess text
    df_jigsaw['text'] = df_jigsaw['text'].apply(preprocess_text)

    # Define sentiment based on toxicity (as discussed)
    # If any toxicity flag is 1 -> Negative (0)
    # If all toxicity flags are 0 -> Neutral (1) - Our assumption
    is_toxic = df_jigsaw[TOXICITY_COLS].sum(axis=1) > 0
    df_jigsaw['sentiment'] = is_toxic.apply(lambda x: 0 if x else 1)

     # Ensure toxicity labels are integers (0 or 1)
    for col in TOXICITY_COLS:
        df_jigsaw[col] = df_jigsaw[col].astype(int)

    print(f"Processed Jigsaw: {len(df_jigsaw)} rows")

except FileNotFoundError:
    print(f"Error: Jigsaw file not found at {JIGSAW_PATH}")
    df_jigsaw = pd.DataFrame() # Create empty dataframe

# --- Combine Datasets ---
print("\nCombining datasets...")
if not df_sent.empty or not df_jigsaw.empty:
    df_combined = pd.concat([df_sent, df_jigsaw], ignore_index=True)

    # Remove rows with empty text after preprocessing
    df_combined.dropna(subset=['text'], inplace=True)
    df_combined = df_combined[df_combined['text'].str.len() > 0]

    # Shuffle the dataset
    df_combined = df_combined.sample(frac=1).reset_index(drop=True)

    print(f"Combined dataset size: {len(df_combined)}")
    print("\nSample rows:")
    print(df_combined.head())
    print("\nLabel distribution check:")
    print("Sentiment:")
    print(df_combined['sentiment'].value_counts(dropna=False))
    print("\nToxicity (showing 'toxic' prevalence, -1 means no label):")
    print(df_combined['toxic'].value_counts(dropna=False))


    # --- Save Processed Data ---
    df_combined.to_csv(OUTPUT_PATH, index=False)
    print(f"\nProcessed data saved to {OUTPUT_PATH}")
else:
    print("\nCould not combine datasets as one or both source files were missing or empty.")