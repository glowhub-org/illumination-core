# Dockerfile  ✅ single‑stage, all packages present
FROM python:3.12-slim

WORKDIR /app

# 1) 依存パッケージをインストール
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 2) アプリコードをコピー
COPY . .

# 3) 環境変数
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# 4) FastAPI(8000) と Streamlit(8080) を同時起動
CMD uvicorn api.main:app --host 0.0.0.0 --port 8000 & \
    streamlit run app/streamlit_app.py \
    --server.port 8080 --server.address 0.0.0.0 --server.headless true
