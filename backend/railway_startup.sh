#!/bin/bash
set -e

# Define logging functions
log_info() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [INFO] $1"
}

log_warning() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [WARNING] $1"
}

log_error() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') [ERROR] $1"
}

# Display system information
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

# Startup script begins
log_info "===== Mindful Creator Backend Startup ====="
show_system_info

# Check and install essential dependencies
log_info "Installing essential dependencies..."
pip install --upgrade --quiet websockets requests fastapi uvicorn
if [ $? -ne 0 ]; then
  log_error "Failed to install dependencies"
else
  log_info "Dependencies installed successfully"
fi

# Set Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
log_info "PYTHONPATH = $PYTHONPATH"

# Use the PORT environment variable, must be 8000 for Railway health check
export PORT=8000
log_info "PORT set to $PORT for Railway compatibility"
APP_PORT=$PORT
log_info "Using port: $APP_PORT"

# Check and report model status
MODEL_DIR="app/nlp"
log_info "Checking model files in $MODEL_DIR..."

# Create directory if it doesn't exist
if [ ! -d "$MODEL_DIR" ]; then
  log_info "Creating model directory: $MODEL_DIR"
  mkdir -p "$MODEL_DIR"
fi

# Check key model files
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

# Report model status
log_info "Model status: $MODEL_STATUS"
log_info "MODEL_LOADED=$MODEL_LOADED"
echo "MODEL_LOADED=$MODEL_LOADED" >> .env

# Show model directory size
MODEL_SIZE=$(du -sh "$MODEL_DIR" 2>/dev/null | cut -f1)
log_info "Model directory size: ${MODEL_SIZE:-unknown}"

# Check resources before starting
log_info "Resource usage before starting server:"
show_system_info

# Start the server - ENSURE we use port 8000 for Railway
log_info "Starting Uvicorn server on port 8000 for Railway compatibility..."
# Make sure port is explicitly passed to uvicorn as 8000
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 --log-level info