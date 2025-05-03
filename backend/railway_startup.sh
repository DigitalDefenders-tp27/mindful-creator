#!/bin/bash

# Railway startup script

echo "=== Mindful Creator Backend Startup ==="
echo "Starting Railway deployment setup..."

echo "Updating critical dependencies..."
pip install --upgrade websockets requests

export PYTHONPATH=$PYTHONPATH:$(pwd)
echo "Python path: $PYTHONPATH"

mkdir -p app/nlp

MODEL_LOADED=false

function run_with_timeout() {
  local timeout=$1
  local command="${@:2}"
  
  ( $command ) & pid=$!
  
  ( sleep $timeout && kill -SIGTERM $pid 2>/dev/null ) & watcher=$!
  
  wait $pid 2>/dev/null
  status=$?
  
  pkill -P $watcher 2>/dev/null
  wait $watcher 2>/dev/null
  
  return $status
}

echo "=== Installing Git LFS and cloning model repository ==="
apt-get update && apt-get install -y git-lfs
git lfs install

echo "Attempting to download NLP model (timeout: 300s)..."
if run_with_timeout 300 git clone https://huggingface.co/spaces/Jet-12138/CommentResponse app/nlp; then
  rm -rf app/nlp/.git
  echo "=== Model repository cloned successfully ==="
  MODEL_LOADED=true
else
  echo "=== WARNING: Model download timed out or failed ==="
  echo "=== Will fallback to synthetic data analysis ==="
  
  echo "Creating minimal model structure..."
  echo '{}' > app/nlp/config.json
  touch app/nlp/pytorch_model.bin
  
  cat > app/nlp/app.py << EOF
from typing import Dict
def analyse_batch(comments_text: str) -> Dict:
    """Fallback implementation that returns empty results"""
    return {"sentiment_counts": {}, "toxicity_counts": {}, "comments_with_any_toxicity": 0}
EOF

  cat > app/nlp/model.py << EOF
import torch.nn as nn
class CommentMTLModel(nn.Module):
    """Stub model implementation"""
    def __init__(self, model_name, num_sentiment_labels, num_toxicity_labels, dropout_prob=0.1):
        super(CommentMTLModel, self).__init__()
    def forward(self, input_ids, attention_mask, token_type_ids=None):
        return {}
EOF

  cat > app/nlp/__init__.py << EOF
"""Fallback NLP module"""
EOF
fi

# 测试API名称方法 - 跳过测试避免路径问题
echo "=== Skipping API test due to path constraints ==="

# 设置PORT环境变量（如果没有设置）
if [ -z "$PORT" ]; then
  export PORT=8000
  echo "PORT not set, using default: 8000"
else
  echo "Using provided PORT: $PORT"
fi

# 设置超时环境变量，使应用程序响应更快
export TIMEOUT=20
export MODEL_LOADED=$MODEL_LOADED

# 启动应用，设置适当的超时和工作线程
echo "Starting Mindful Creator API..."
echo "Current directory: $(pwd)"
echo "Directory listing:"
ls -la

# 增加工作线程和超时设置
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2 --timeout-keep-alive 30 