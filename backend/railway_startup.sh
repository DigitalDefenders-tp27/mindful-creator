#!/usr/bin/env bash
set -e 

echo "=== Mindful Creator Backend Startup ==="

# Install critical dependencies
echo "Installing critical dependencies..."
pip install --upgrade --quiet websockets requests fastapi uvicorn

# Set up Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH = $PYTHONPATH"

# Create model directory
MODEL_DIR="app/nlp"
mkdir -p "$MODEL_DIR"

# Simple model fallback function
create_fallback_model() {
  echo "⚠️  Creating placeholder model"
  cat > "$MODEL_DIR/app.py" <<'PY'
def analyse_batch(comments_text: str):
    return {"sentiment_counts": {}, "toxicity_counts": {}, "comments_with_any_toxicity": 0}
PY
  echo '{}' > "$MODEL_DIR/config.json"
  echo "MODEL_LOADED=false" >> .env
}

# Create a simple model immediately to ensure app can start
create_fallback_model

# Try to download the actual model in the background, with a timeout
echo "Attempting to download NLP model in background (will timeout after 5 minutes)..."
(
  timeout 300s git clone --depth 1 https://huggingface.co/spaces/Jet-12138/CommentResponse "$MODEL_DIR.download" && \
  rm -rf "$MODEL_DIR.download/.git" && \
  mv "$MODEL_DIR.download"/* "$MODEL_DIR"/ && \
  rm -rf "$MODEL_DIR.download" && \
  echo "MODEL_LOADED=true" >> .env && \
  echo "✓ Model downloaded and installed successfully" || echo "⚠️  Model download timed out or failed, using placeholder"
) &

# Set up environment variables
APP_PORT="${PORT:-8000}"
echo "Uvicorn will listen on port $APP_PORT"
export TIMEOUT=60

# Diagnostics
echo "==== Environment Information ===="
echo "Current directory: $(pwd)"
echo "Directory listing:"
ls -la
echo "Python version:"
python --version
echo "================================="

# Start the app with appropriate settings
echo "Starting Mindful Creator API..."
exec uvicorn app.main:app \
      --host 0.0.0.0 \
      --port "$APP_PORT" \
      --workers 1 \
      --timeout-keep-alive 60