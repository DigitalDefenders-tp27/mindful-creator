#!/bin/bash

# Railway启动脚本
# 这个脚本将在Railway部署中自动运行

echo "=== Mindful Creator Backend Startup ==="
echo "Starting Railway deployment setup..."

# 确保安装最新的依赖
echo "Updating critical dependencies..."
pip install --upgrade websockets

# 安装Git LFS并克隆模型
echo "=== Installing Git LFS and cloning model repository ==="
apt-get update && apt-get install -y git-lfs
git lfs install
mkdir -p backend/app/nlp
git clone https://huggingface.co/spaces/Jet-12138/CommentResponse backend/app/nlp

# 删除嵌套的 .git 目录
echo "=== Removing nested .git directory ==="
rm -rf backend/app/nlp/.git
echo "=== Model repository cloned successfully ==="

# 测试API名称方法
echo "=== Testing API name '/predict' method ==="
python -m backend.tests.test_api_name
API_TEST_RESULT=$?

if [ $API_TEST_RESULT -eq 0 ]; then
  echo "✅ API name '/predict' test successful!"
else
  echo "⚠️ API name '/predict' test failed. May fall back to simulated values."
fi

# 启动应用
echo "Starting Mindful Creator API..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT 