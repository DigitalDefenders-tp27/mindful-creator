FROM python:3.11-slim

# Set environment variables to prevent interactive prompts during apt-get install
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1

# Set working directory
WORKDIR /app

# ---------- Install git & git-lfs ----------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    git-lfs \
    procps \
    unzip \
    python3-pip \
    && git lfs install \
    && rm -rf /var/lib/apt/lists/*

# ---------- Python deps ----------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir tenacity>=8.2.0 psycopg2-binary>=2.9.6 httpx>=0.24.0

# ---------- Download BERT model ----------
RUN python - <<PY
from transformers import AutoModel, AutoTokenizer
m = AutoModel.from_pretrained("bert-base-uncased")
t = AutoTokenizer.from_pretrained("bert-base-uncased")
m.save_pretrained("/app/bert-base-uncased")
t.save_pretrained("/app/bert-base-uncased")
PY

# ---------- Clone NLP model (cached layer) ----------
RUN mkdir -p /app/nlp && \
    git clone --depth 1 https://huggingface.co/spaces/Jet-12138/CommentResponse /app/nlp && \
    cd /app/nlp && git lfs pull && rm -rf .git && \
    echo "NLP model cloned to $(pwd)" && \
    ls -la /app/nlp

# --- Kaggle API Setup & Download ---
# This step expects kaggle.json to be in the build context (backend directory)
RUN mkdir -p /root/.kaggle
COPY kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json

# Create a directory for the memes and download them
RUN mkdir -p /app/meme_images
WORKDIR /app/meme_images
# Download the dataset
RUN echo "Current directory before Kaggle download: $(pwd)" && \
    kaggle datasets download -d williamscott701/memotion-dataset-7k --unzip -p . && \
    echo "Contents of /app/meme_images after Kaggle download and unzip:" && \
    ls -laR . && \
    # Check for the new expected path: memotion_dataset_7k/images
    if [ -d "memotion_dataset_7k/images" ]; then \
        echo "Found images in memotion_dataset_7k/images/. Moving contents..."; \
        mv memotion_dataset_7k/images/* .; \
        rm -rf memotion_dataset_7k; \
    # Fallback for a direct 'images' subdirectory
    elif [ -d "images" ]; then \
        echo "Found images in a direct 'images' subdirectory. Moving contents..."; \
        mv images/* .; \
        rm -rf images; \
    else \
        echo "Images are expected to be directly in /app/meme_images."; \
    fi

# Return to the main app directory
WORKDIR /app

# Copy startup script first and make it executable
COPY railway_startup.sh .
RUN chmod +x railway_startup.sh

# Copy the application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/datasets/meme && \
    cp -r /app/meme_images/* /app/datasets/meme/ || true

# Verify Python module structure
RUN ls -la /app && \
    ls -la /app/app || echo "No /app/app directory found" && \
    echo "Final directory structure:" && \
    find /app -type d -maxdepth 2 | sort && \
    echo "Python path: $PYTHONPATH"

# Make sure Python can find our modules
ENV PYTHONPATH=/app:$PYTHONPATH

# Run the application
ENTRYPOINT ["bash", "./railway_startup.sh"]