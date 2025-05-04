FROM python:3.11-slim
WORKDIR /app

# Install system tools for monitoring and logging
RUN apt-get update && \
    apt-get install -y --no-install-recommends git git-lfs procps && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

# Add build info function
RUN echo '#!/bin/bash \n\
    echo "🔍 System Info:" \n\
    echo "- Memory: $(free -h)" \n\
    echo "- Disk: $(df -h /)" \n\
    echo "- CPU: $(grep "model name" /proc/cpuinfo | head -1)" \n\
    ' > /usr/local/bin/sysinfo && \
    chmod +x /usr/local/bin/sysinfo

# Show initial system info
RUN echo "📦 Build started" && sysinfo

COPY requirements.txt .
RUN echo "📥 Installing dependencies..." && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    echo "✅ Dependencies installed" && sysinfo

# Cache model download status to a file for later checking
RUN echo "⏬ Downloading NLP model (this may take several minutes)..." && \
    mkdir -p app/app/nlp && \
    echo "MODEL_DOWNLOAD_START=$(date +%s)" > /tmp/model_status.log && \
    git clone --depth 1 https://huggingface.co/spaces/Jet-12138/CommentResponse app/app/nlp || \
    (echo "❌ Model download failed. Creating empty model directory." && mkdir -p app/app/nlp) && \
    echo "MODEL_DOWNLOAD_END=$(date +%s)" >> /tmp/model_status.log

# Show model download status
RUN cd app/app/nlp && \
    if [ -f "pytorch_model.bin" ]; then \
        echo "✅ Model files:" && \
        du -sh * | sort -hr && \
        echo "⏱️ Download duration: $(($(grep END /tmp/model_status.log | cut -d= -f2) - $(grep START /tmp/model_status.log | cut -d= -f2))) seconds"; \
    else \
        echo "⚠️ Model file pytorch_model.bin not found"; \
    fi && \
    if [ -d ".git" ]; then rm -rf .git; fi && \
    sysinfo

COPY . .

# Show final build info
RUN echo "🏁 Build completed" && \
    ls -la && \
    echo "📁 Application files:" && \
    find . -type f -not -path "*/\.*" -not -path "*/app/nlp/*" | wc -l && \
    echo "📦 Model directory size:" && \
    du -sh app/app/nlp || echo "Model directory not found" && \
    sysinfo

EXPOSE 8000
CMD ["sh", "railway_startup.sh"]