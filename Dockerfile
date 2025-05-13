# Dockerfile  🚀 “バイナリ込み” マルチステージ

FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
# site‑packages + scripts(binaries) の両方をコピー
COPY --from=builder /usr/local/lib/python*/site-packages /usr/local/lib/python*/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

CMD /bin/sh -c "uvicorn api.main:app --host 0.0.0.0 --port 8000 & \
                streamlit run app/streamlit_app.py \
                --server.port 8501 --server.address 0.0.0.0 --server.headless true"
