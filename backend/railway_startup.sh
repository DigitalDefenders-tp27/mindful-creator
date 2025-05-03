#!/usr/bin/env bash
set -e 

echo "=== Mindful Creator Backend Startup ==="

pip install --upgrade --quiet websockets requests

export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo "PYTHONPATH = $PYTHONPATH"

MODEL_DIR="app/nlp"
mkdir -p "$MODEL_DIR"

download_model () {
  echo "→ Cloning model repo …"
  git clone --depth 1 https://huggingface.co/spaces/Jet-12138/CommentResponse "$MODEL_DIR"
  rm -rf "$MODEL_DIR/.git"
  echo "✓ Model cloned"
}

fallback_model () {
  echo "⚠️  Model download failed, creating placeholder model"
  cat > "$MODEL_DIR/app.py" <<'PY'
def analyse_batch(comments_text: str):
    return {"sentiment_counts": {}, "toxicity_counts": {}, "comments_with_any_toxicity": 0}
PY
  echo '{}' > "$MODEL_DIR/config.json"
}

timeout 300s bash -c download_model || fallback_model


APP_PORT="${PORT:-8000}"
echo "Uvicorn will listen on port $APP_PORT"

exec uvicorn app.main:app \
      --host 0.0.0.0 \
      --port "$APP_PORT" \
      --workers 2 \
      --timeout-keep-alive 30