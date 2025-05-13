# --- add upper folder into PYTHONPATH --------------------
import sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent   # = /app
if str(root) not in sys.path:
    sys.path.append(str(root))
# ---------------------------------------------------------
# --- FastAPI 同居サーバ -------------------------------------------------
import threading, uvicorn
from api.main import app as fastapi_app
def run_api(): uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, log_level="error")
threading.Thread(target=run_api, daemon=True).start()
# -----------------------------------------------------------------------
# app/streamlit_app.py  🚀 4‑Axis UI β

import streamlit as st, requests, json
import plotly.graph_objects as go

API_URL = "http://localhost:8000"              # ← 必ず localhost:8000 に

st.title("Illumination‑Core • 4‑Axis Inspector")

tab1, tab2 = st.tabs(["URL / DOI", "Raw text"])

with tab1:
    url = st.text_input("Resource URL か DOI を入力")
    if st.button("Analyze", key="url_btn") and url:
        res = requests.post(f"{API_URL}/score",
                            json={"url": url}).json()
        st.metric("Composite Score", round(res["score"], 3))
        radar = go.Figure(go.Scatterpolar(
            r=list(res["norm"].values()),
            theta=list(res["norm"].keys()), fill='toself'))
        st.plotly_chart(radar, use_container_width=True)
        st.json(res)

with tab2:
    text = st.text_area("貼り付けテキスト（最大〜1万字）", height=200)
    if st.button("Analyze", key="text_btn") and text:
        res = requests.post(f"{API_URL}/score_raw",
                            json={"text": text}).json()
        st.metric("ΔH (Information gain)", round(res["norm"]["dH"], 3))
        st.json(res)
