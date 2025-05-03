FROM python:3.11-slim
WORKDIR /app
    
RUN apt-get update && \
    apt-get install -y --no-install-recommends git git-lfs && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN echo "⏬  Downloading NLP model ..." && \
    git clone --depth 1 https://huggingface.co/spaces/Jet-12138/CommentResponse app/app/nlp && \
    cd app/app/nlp && git lfs pull && \
    rm -rf .git && \
    echo "✓ Model downloaded"

COPY . .

EXPOSE 8080
CMD ["sh", "railway_startup.sh"]