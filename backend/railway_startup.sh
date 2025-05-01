#!/bin/bash

# Railway启动脚本
# 这个脚本将在Railway部署中自动运行

echo "=== Mindful Creator Backend Startup ==="
echo "Starting Railway deployment setup..."

# 确保安装最新的依赖
echo "Updating critical dependencies..."
pip install --upgrade gradio_client
pip install --upgrade websockets

# 创建临时目录用于gradio_client（如果不存在）
export GRADIO_TEMP_DIR="/tmp/gradio_client_cache"
echo "Setting GRADIO_TEMP_DIR to: $GRADIO_TEMP_DIR"
mkdir -p $GRADIO_TEMP_DIR

# 设置gradio_client临时目录
export GRADIO_CLIENT_TEMP_DIR=$GRADIO_TEMP_DIR
echo "Setting GRADIO_CLIENT_TEMP_DIR to: $GRADIO_CLIENT_TEMP_DIR"

# 调试Space API端点
echo "=== Debugging Space API endpoints ==="
python -m backend.debug_space_connection
echo "=== End of Space API debug ==="

# 运行Space连接测试
echo "Testing Space CLI connection..."
python -m backend.tests.test_space_cli

# 检查测试结果
if [ $? -ne 0 ]; then
  echo "⚠️ Space CLI connection test failed. API will fall back to simulated values."
else
  echo "✅ Space CLI connection test successful!"
fi

# 启动应用
echo "Starting Mindful Creator API..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT 