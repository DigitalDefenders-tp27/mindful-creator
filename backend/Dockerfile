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

# ---------- Clone NLP model (cached layer) ----------
RUN git clone --depth 1 https://huggingface.co/spaces/Jet-12138/CommentResponse nlp && \
    cd nlp && git lfs pull && rm -rf .git

# ---------- App source ----------
COPY . .
RUN chmod +x railway_startup.sh

# EXPOSE 8080
ENTRYPOINT ["bash", "railway_startup.sh"]