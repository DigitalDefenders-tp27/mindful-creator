FROM python:3.11-slim
WORKDIR /app

# ---------- Install git & git-lfs ----------
RUN apt-get update && \
    apt-get install -y --no-install-recommends git git-lfs procps && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

# ---------- Python deps ----------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 下载一次并持久化
RUN python - << 'PY'
from transformers import AutoModel, AutoTokenizer
m = AutoModel.from_pretrained("bert-base-uncased")
t = AutoTokenizer.from_pretrained("bert-base-uncased")
m.save_pretrained("/app/bert-base-uncased")
t.save_pretrained("/app/bert-base-uncased")
PY

# ---------- Clone NLP model (cached layer) ----------
RUN mkdir -p /app/nlp && \
    git clone --depth 1 https://huggingface.co/spaces/Jet-12138/CommentResponse /app/nlp && \
    cd /app/nlp && git lfs pull && rm -rf .git && \
    echo "NLP model cloned to $(pwd)" && \
    ls -la /app/nlp

# ---------- App source ----------
COPY railway_startup.sh .
RUN chmod +x railway_startup.sh

COPY . .
# EXPOSE 8080
ENTRYPOINT ["bash", "railway_startup.sh"]