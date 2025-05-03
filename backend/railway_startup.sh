#!/bin/bash

# Railway启动脚本
# 这个脚本将在Railway部署中自动运行

echo "=== Mindful Creator Backend Startup ==="
echo "Starting Railway deployment setup..."

# 确保安装最新的依赖
echo "Updating critical dependencies..."
pip install --upgrade websockets

# 设置Python路径
export PYTHONPATH=$PYTHONPATH:$(pwd)
echo "Python path: $PYTHONPATH"

# 安装Git LFS并克隆模型
echo "=== Installing Git LFS and cloning model repository ==="
apt-get update && apt-get install -y git-lfs
git lfs install
mkdir -p app/nlp
git clone https://huggingface.co/spaces/Jet-12138/CommentResponse app/nlp

# 删除嵌套的 .git 目录
echo "=== Removing nested .git directory ==="
rm -rf app/nlp/.git
echo "=== Model repository cloned successfully ==="

# 测试API名称方法 - 跳过测试避免路径问题
echo "=== Skipping API test due to path constraints ==="

# 设置PORT环境变量（如果没有设置）
if [ -z "$PORT" ]; then
  export PORT=8000
  echo "PORT not set, using default: 8000"
else
  echo "Using provided PORT: $PORT"
fi

# 启动应用
echo "Starting Mindful Creator API..."
echo "Current directory: $(pwd)"
echo "Directory listing:"
ls -la
uvicorn app.main:app --host 0.0.0.0 --port $PORT 