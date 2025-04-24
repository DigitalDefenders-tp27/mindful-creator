"""
Standalone script to read raw CSVs, clean them, combine into one
processed_comments.csv, exactly once (or whenever you want to refresh).
"""
import os
import pandas as pd
from preprocess_data import preprocess_text

# Paths
DATA_DIR         = "../data"
SENT140_PATH     = os.path.join(DATA_DIR, "sentiment140.csv")
JIGSAW_PATH      = os.path.join(DATA_DIR, "jigsaw_train.csv")
OUTPUT_PATH      = os.path.join(DATA_DIR, "processed_comments.csv")

# Toxicity columns
TOXICITY_COLS = ['toxic','severe_toxic','obscene','threat','insult','identity_hate']

def process_sentiment140() -> pd.DataFrame:
    df = pd.read_csv(
        SENT140_PATH,
        encoding='latin-1', header=None,
        names=['sentiment_raw','id','date','query','user','text']
    )
    df = df[['sentiment_raw','text']].dropna()
    df['text'] = df['text'].apply(preprocess_text)
    df['sentiment'] = df['sentiment_raw'].map({0: 0, 4: 2})
    for col in TOXICITY_COLS:
        df[col] = -1
    return df[['text','sentiment'] + TOXICITY_COLS]

def process_jigsaw() -> pd.DataFrame:
    df = pd.read_csv(JIGSAW_PATH)
    df = df[['comment_text'] + TOXICITY_COLS].rename(columns={'comment_text':'text'})
    df['text'] = df['text'].apply(preprocess_text)
    df['sentiment'] = (df[TOXICITY_COLS].sum(axis=1) == 0).astype(int)  # 1 if all zeros, else 0
    return df[['text','sentiment'] + TOXICITY_COLS]

def main():
    print("Processing Sentiment140…")
    df1 = process_sentiment140()
    print(f" → {len(df1)} rows")

    print("Processing Jigsaw…")
    df2 = process_jigsaw()
    print(f" → {len(df2)} rows")

    print("Combining and shuffling…")
    df = pd.concat([df1, df2], ignore_index=True)
    df = df[df['text'].str.len()>0].sample(frac=1, random_state=42).reset_index(drop=True)
    print(f"→ Combined: {len(df)} rows")

    print(f"Saving to {OUTPUT_PATH}")
    df.to_csv(OUTPUT_PATH, index=False)
    print("Done.")

if __name__ == "__main__":
    main()
