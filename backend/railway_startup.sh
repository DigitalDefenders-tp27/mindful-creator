#!/bin/bash
set -e

# 定义日志函数
log_info() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1"
}

log_warning() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [WARNING] $1"
}

log_error() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] $1"
}

# 显示系统信息
show_system_info() {
  log_info "===== System Information ====="
  echo "- Memory Usage:"
  if command -v free >/dev/null 2>&1; then
    free -h
  else
    echo "  free command not available"
    if [ -f /proc/meminfo ]; then
      grep -E "MemTotal|MemFree|MemAvailable" /proc/meminfo
    fi
  fi
  
  echo "- Disk Usage:"
  df -h .
  
  echo "- Python Version:"
  python3 --version
  
  echo "- Current Directory: $(pwd)"
  echo "- User: $(whoami)"
  echo "- Environment Variables:"
  printenv | grep -E "PATH|PYTHON|PORT|MODEL"
}

# 启动脚本开始
log_info "===== Mindful Creator Backend Startup ====="
show_system_info

# 检查安装必要的依赖项
log_info "Installing essential dependencies..."
pip install --upgrade --quiet websockets requests fastapi uvicorn
if [ $? -ne 0 ]; then
  log_error "Failed to install dependencies"
else
  log_info "Dependencies installed successfully"
fi

# 设置 Python 路径
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
log_info "PYTHONPATH = $PYTHONPATH"

# 使用Railway提供的PORT环境变量，如果未设置则默认为8000
APP_PORT="${PORT:-8000}"
log_info "PORT env from Railway = ${PORT:-not set}"
log_info "Using port: $APP_PORT"

# 检查和报告模型状态
MODEL_DIR="app/nlp"
log_info "Checking model files in $MODEL_DIR..."

# 创建目录（如果不存在）
if [ ! -d "$MODEL_DIR" ]; then
  log_info "Creating model directory: $MODEL_DIR"
  mkdir -p "$MODEL_DIR"
fi

# 检查关键模型文件
log_info "Model directory contents:"
ls -la "$MODEL_DIR"

REQUIRED_FILES=("app.py" "config.json" "model.py" "pytorch_model.bin")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$MODEL_DIR/$file" ]; then
    MISSING_FILES+=("$file")
  fi
done

if [ ${#MISSING_FILES[@]} -eq 0 ]; then
  log_info "✅ All required model files found"
  MODEL_STATUS="All files present"
  export MODEL_LOADED=true
else
  log_warning "⚠️ Some model files are missing: ${MISSING_FILES[*]}"
  MODEL_STATUS="Missing: ${MISSING_FILES[*]}"
  export MODEL_LOADED=false
fi

# 报告模型状态
log_info "Model status: $MODEL_STATUS"
log_info "MODEL_LOADED=$MODEL_LOADED"
echo "MODEL_LOADED=$MODEL_LOADED" >> .env

# 显示模型目录大小
MODEL_SIZE=$(du -sh "$MODEL_DIR" 2>/dev/null | cut -f1)
log_info "Model directory size: ${MODEL_SIZE:-unknown}"

# 启动前再次检查资源
log_info "Resource usage before starting server:"
show_system_info

# 启动服务器
log_info "Starting Uvicorn server on port ${APP_PORT}..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$APP_PORT" --workers 1 --log-level info