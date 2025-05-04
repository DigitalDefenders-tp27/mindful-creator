FROM python:3.11-slim
WORKDIR /app

# Install essentials
RUN apt-get update && \
    apt-get install -y git git-lfs procps && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone --depth 1 https://huggingface.co/spaces/Jet-12138/CommentResponse nlp && \
    cd nlp && git lfs pull && rm -rf .git

# Copy application code & 赋可执行权限
COPY . .
RUN chmod +x railway_startup.sh

# 暴露端口（Railway 对 Dockerfile 默认映射 8080）
EXPOSE 8080

# **唯一定义容器启动命令** —— 让脚本跑起来
ENTRYPOINT ["bash", "railway_startup.sh"] 