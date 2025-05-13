# Dockerfile  🚀 FastAPI ↔︎ Streamlit 分離

FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python*/site-packages /usr/local/lib/python*/site-packages
COPY . .
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app
# 2 本同時起動。Streamlit は 8501、FastAPI は 8000
CMD uvicorn api.main:app --host 0.0.0.0 --port 8000 & \
    streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
