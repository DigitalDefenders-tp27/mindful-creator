#!/usr/bin/env python3
"""
Memotion Dataset Loader
-----------------------
This script loads the Memotion dataset from Kaggle using kagglehub.
The Memotion dataset contains memes with annotations for sentiment analysis.
"""

# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import os
import sys
import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd

def load_memotion_dataset(file_path=""):
    """
    Load the Memotion dataset from Kaggle.
    
    Args:
        file_path (str): Path to the specific file within the dataset to load
                        If empty, will try common filenames
    
    Returns:
        pandas.DataFrame: The loaded dataset
    """
    print("Loading Memotion dataset...")
    
    dataset_name = "williamscott701/memotion-dataset-7k"
    
    # If no file path is specified, try these common filenames
    possible_files = [
        file_path,  # Try the provided path first
        "labels.csv", 
        "memotion_dataset.csv",
        "train.csv",
        "memotion_dataset_7k.csv"
    ]
    
    # Only use non-empty file paths
    possible_files = [f for f in possible_files if f]
    
    # If no possibilities, use a default
    if not possible_files:
        possible_files = ["labels.csv"]
    
    print(f"Will attempt to load the following files: {', '.join(possible_files)}")
    
    # Try each file path
    for file_path in possible_files:
        try:
            print(f"Attempting to load '{file_path}'...")
            
            # Load the latest version of the dataset
            df = kagglehub.load_dataset(
                KaggleDatasetAdapter.PANDAS,
                dataset_name,
                file_path
            )
            
            print(f"Successfully loaded file '{file_path}' with {len(df)} records")
            return df
        
        except Exception as e:
            print(f"Error loading '{file_path}': {str(e)}")
            # Continue to the next file
    
    # If we reach here, all attempts failed
    print("\nFailed to load any files from the Memotion dataset.")
    print("Note: You may need to authenticate with Kaggle first.")
    print("Instructions:")
    print("1. Create a Kaggle account if you don't have one")
    print("2. Generate an API token from your Kaggle account settings")
    print("3. Place the kaggle.json file in ~/.kaggle/ directory")
    return None

def explore_dataset(df):
    """
    Perform basic exploration of the dataset.
    
    Args:
        df (pandas.DataFrame): The dataset to explore
    """
    if df is None:
        return
    
    print("\n--- Dataset Overview ---")
    print(f"Shape: {df.shape}")
    print("\nFirst 5 records:")
    print(df.head())
    
    print("\nColumn information:")
    for col in df.columns:
        print(f"- {col}: {df[col].dtype}")
    
    print("\nMissing values:")
    print(df.isnull().sum())
    
    # If there are sentiment columns, show their distribution
    sentiment_cols = [col for col in df.columns if 'sentiment' in col.lower()]
    if sentiment_cols:
        print("\nSentiment distribution:")
        for col in sentiment_cols:
            print(f"\n{col}:")
            print(df[col].value_counts())

def save_dataset_sample(df, sample_size=100, output_path="dataset_sample.csv"):
    """
    Save a sample of the dataset to a CSV file.
    
    Args:
        df (pandas.DataFrame): The dataset to sample
        sample_size (int): Number of records to sample
        output_path (str): Path to save the sample
    """
    if df is None:
        return
    
    # Take a random sample
    sample_df = df.sample(min(sample_size, len(df)))
    
    # Save to CSV
    sample_df.to_csv(output_path, index=False)
    print(f"\nSaved {len(sample_df)} sample records to {output_path}")

if __name__ == "__main__":
    try:
        # Use the exact code snippet from the user's template
        # Install dependencies as needed:
        # pip install kagglehub[pandas-datasets]
        import kagglehub
        from kagglehub import KaggleDatasetAdapter

        # Set the path to the file you'd like to load
        file_path = ""

        # Load the latest version
        df = kagglehub.load_dataset(
          KaggleDatasetAdapter.PANDAS,
          "williamscott701/memotion-dataset-7k",
          file_path,
          # Provide any additional arguments like 
          # sql_query or pandas_kwargs. See the 
          # documentation for more information:
          # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
        )

        print("First 5 records:", df.head())
        
        # Save a sample to our datasets directory
        if not os.path.exists("backend/datasets"):
            os.makedirs("backend/datasets")
        
        sample_df = df.sample(min(100, len(df)))
        sample_df.to_csv("backend/datasets/memotion_sample.csv", index=False)
        print(f"Saved {len(sample_df)} sample records to backend/datasets/memotion_sample.csv")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nFalling back to alternative method...")
        
        # Try the fallback function
        df = load_memotion_dataset()
        if df is not None:
            print("First 5 records:")
            print(df.head())
            
            # Save a sample
            if not os.path.exists("backend/datasets"):
                os.makedirs("backend/datasets")
            
            sample_df = df.sample(min(100, len(df)))
            sample_df.to_csv("backend/datasets/memotion_sample.csv", index=False)
            print(f"Saved {len(sample_df)} sample records to backend/datasets/memotion_sample.csv") 