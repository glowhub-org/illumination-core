# app/streamlit_app.py  🚀 分離版

import streamlit as st, requests, json, plotly.graph_objects as go

API_URL = "http://localhost:8000"   # 別プロセスで動く FastAPI

st.title("Illumination‑Core • 4‑Axis Inspector")

tab1, tab2 = st.tabs(["URL / DOI", "Raw text"])

def call_api(payload: dict):
    r = requests.post(f"{API_URL}/score", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

with tab1:
    url = st.text_input("Resource URL か DOI を入力")
    if st.button("Analyze") and url:
        try:
            res = call_api({"url": url})
            st.metric("Composite Score", round(res["score"], 3))
            radar = go.Figure(go.Scatterpolar(
                r=list(res["norm"].values()),
                theta=list(res["norm"].keys()), fill='toself'))
            st.plotly_chart(radar, use_container_width=True)
            st.json(res)
        except Exception as e:
            st.error(f"API error: {e}")

with tab2:
    text = st.text_area("貼り付けテキスト（最大1万字）", height=200)
    if st.button("Analyze Text") and text:
        try:
            res = call_api({"text": text})
            st.metric("ΔH", round(res["norm"]["dH"], 3))
            st.json(res)
        except Exception as e:
            st.error(f"API error: {e}")
