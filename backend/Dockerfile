FROM python:3.11-slim

# Set environment variables to prevent interactive prompts during apt-get install
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

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
RUN pip install --no-cache-dir -r requirements.txt

# 下载一次并持久化
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
    ls -la /app/nlp && \
    # Ensure bert-base-uncased is available, if CommentResponse doesn't bundle it directly
    # This step might be redundant if CommentResponse includes BERT, or if TOKENIZER_DIR points correctly
    if [ ! -d "/app/bert-base-uncased" ]; then \
        echo "bert-base-uncased not found, attempting to download..."; \
        python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('bert-base-uncased').save_pretrained('/app/bert-base-uncased')"; \
        ls -la /app/bert-base-uncased; \
    else \
        echo "bert-base-uncased already present."; \
    fi

# ---------- App source ----------
COPY railway_startup.sh .
RUN chmod +x railway_startup.sh

# --- Kaggle API Setup & Download ---
# This step expects kaggle.json to be in the build context (backend directory)
RUN mkdir -p /root/.kaggle
COPY kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json

# Create a directory for the memes and download them
RUN mkdir -p /app/meme_images
WORKDIR /app/meme_images
# Download the dataset. Ensure 'williamscott701/memotion-dataset-7k' is correct.
RUN echo "Current directory before Kaggle download: $(pwd)" && \
    kaggle datasets download -d williamscott701/memotion-dataset-7k --unzip -p . && \
    echo "Contents of /app/meme_images after Kaggle download and unzip:" && \
    ls -laR . && \
    # If images are in a subdirectory (e.g., named 'images'), move them to the current dir
    # and remove the subdirectory.
    if [ -d "images" ]; then \
        echo "'images' subdirectory found. Moving contents..."; \
        mv images/* .; \
        rm -rf images; \
        echo "Contents of /app/meme_images after mv operation:" && \
        ls -laR .; \
    else \
        echo "No 'images' subdirectory found, or it was empty."; \
    fi
WORKDIR /app # Switch back to the main app directory
# --- End Kaggle Download ---

COPY . .
# EXPOSE 8080
ENTRYPOINT ["bash", "railway_startup.sh"]