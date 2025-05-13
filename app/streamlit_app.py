# app/streamlit_app.py  🚀 4‑Axis UI β（完全版）

# ===== 1) プロジェクトルートを PYTHONPATH に追加 ======================
import sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent   # → /app
if str(root) not in sys.path:
    sys.path.append(str(root))

# ===== 2) FastAPI を同居スレッドで 1 回だけ起動 =======================
import threading, uvicorn, streamlit as st
if "api_thread_started" not in st.session_state:
    from api.main import app as fastapi_app             # api/main.py
    def run_api():
        uvicorn.run(fastapi_app,
                    host="0.0.0.0", port=8000, log_level="error")
    threading.Thread(target=run_api, daemon=True).start()
    st.session_state["api_thread_started"] = True
# ======================================================================

# ===== 3) 通常の Streamlit 処理 =======================================
import requests, json, plotly.graph_objects as go

API_URL = "http://localhost:8000"   # ← 同居 FastAPI への内部呼び出し

st.title("Illumination‑Core • 4‑Axis Inspector")

tab1, tab2 = st.tabs(["URL / DOI", "Raw text"])

# ---------- URL / DOI -------------------------------------------------
with tab1:
    url = st.text_input("Resource URL か DOI を入力")
    if st.button("Analyze", key="url_btn") and url:
        try:
            r = requests.post(f"{API_URL}/score", json={"url": url}, timeout=20)
            r.raise_for_status()
            res = r.json()
            st.metric("Composite Score", round(res["score"], 3))

            radar = go.Figure(go.Scatterpolar(
                r=list(res["norm"].values()),
                theta=list(res["norm"].keys()),
                fill='toself'))
            st.plotly_chart(radar, use_container_width=True)
            st.json(res)

        except Exception as e:
            st.error(f"API error: {e}\n\n{r.text if 'r' in locals() else ''}")

# ---------- Raw text --------------------------------------------------
with tab2:
    text = st.text_area("貼り付けテキスト（最大1万字）", height=200)
    if st.button("Analyze", key="text_btn") and text:
        try:
            r = requests.post(f"{API_URL}/score", json={"text": text}, timeout=30)
            r.raise_for_status()
            res = r.json()
            st.metric("ΔH (Information gain)", round(res["norm"]["dH"], 3))
            st.json(res)
        except Exception as e:
            st.error(f"API error: {e}\n\n{r.text if 'r' in locals() else ''}")
