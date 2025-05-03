#!/usr/bin/env bash
set -e 

echo "=== Mindful Creator Backend Startup ==="

# Install essential dependencies
pip install --upgrade --quiet websockets requests fastapi uvicorn

# Set up Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH = $PYTHONPATH"

# Prepare model directory with minimal placeholder to ensure app starts quickly
MODEL_DIR="app/nlp"
mkdir -p "$MODEL_DIR"

# Create basic placeholder model
echo "Creating minimal model placeholder"
cat > "$MODEL_DIR/app.py" <<EOF
def analyse_batch(comments_text: str):
    return {"sentiment_counts": {}, "toxicity_counts": {}, "comments_with_any_toxicity": 0}
EOF
echo '{}' > "$MODEL_DIR/config.json"

# Model can be downloaded later - this keeps startup fast
echo "Skipping model download for fast startup"

# Get port setting and start server
APP_PORT="${PORT:-8000}"
echo "Starting Uvicorn on port $APP_PORT"

# Diagnostics
echo "Current directory: $(pwd)"
echo "Content of model directory: $(ls -la $MODEL_DIR)"

# Start server with minimal configuration for reliable startup
exec uvicorn app.main:app \
      --host 0.0.0.0 \
      --port "$APP_PORT" \
      --workers 1 \
      --log-level info