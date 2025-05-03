#!/usr/bin/env bash
set -e 

echo "=== Mindful Creator Backend Startup ==="

# Install essential dependencies
pip install --upgrade --quiet websockets requests fastapi uvicorn

# Set up Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH = $PYTHONPATH"

# Prepare model directory
MODEL_DIR="app/nlp"
mkdir -p "$MODEL_DIR"

# Install Git LFS if needed
if ! command -v git-lfs &> /dev/null; then
    echo "Installing Git LFS..."
    apt-get update && apt-get install -y git-lfs
    git lfs install
fi

# Download the model (with timeout)
echo "Downloading NLP model (timeout: 300 seconds)..."
if timeout 300s git clone --depth 1 https://huggingface.co/spaces/Jet-12138/CommentResponse "$MODEL_DIR.download"; then
    # Remove git files to save space
    rm -rf "$MODEL_DIR.download/.git"
    
    # Move files to model directory
    echo "Moving model files to $MODEL_DIR"
    cp -r "$MODEL_DIR.download"/* "$MODEL_DIR"/ 
    rm -rf "$MODEL_DIR.download"
    
    # Set model loaded flag
    export MODEL_LOADED=true
    echo "MODEL_LOADED=true" >> .env
    echo "✓ Model downloaded and installed successfully"
else
    echo "⚠️ Model download timed out or failed, creating fallback model"
    # Create basic placeholder model as fallback
    cat > "$MODEL_DIR/app.py" <<EOF
def analyse_batch(comments_text: str):
    return {"sentiment_counts": {}, "toxicity_counts": {}, "comments_with_any_toxicity": 0}
EOF
    echo '{}' > "$MODEL_DIR/config.json"
    export MODEL_LOADED=false
    echo "MODEL_LOADED=false" >> .env
fi

# Get port setting and start server
APP_PORT="${PORT:-8000}"
echo "Starting Uvicorn on port $APP_PORT"

# Diagnostics
echo "Current directory: $(pwd)"
echo "Content of model directory: $(ls -la $MODEL_DIR)"

# Start server
echo "Starting Mindful Creator API..."
exec uvicorn app.main:app \
      --host 0.0.0.0 \
      --port "$APP_PORT" \
      --workers 1 \
      --log-level info