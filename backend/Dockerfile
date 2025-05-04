FROM python:3.11-slim
WORKDIR /app

# Install essentials
RUN apt-get update && \
    apt-get install -y git git-lfs procps && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download model
RUN mkdir -p app/app/nlp && \
    git clone --depth 1 https://huggingface.co/spaces/Jet-12138/CommentResponse app/app/nlp || \
    (echo "Model download failed, creating empty dir" && mkdir -p app/app/nlp)

# Copy application code
COPY . .

# Expose port - use the PORT env var, defaulting to 8000
EXPOSE 8000

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8000

# Make sure Railway sees the correct port in logs
RUN echo "Railway will detect port: $PORT"

# Start command - use railway_startup.sh
CMD ["sh", "railway_startup.sh"] 