# app/streamlit_app.py  🔥 保存付き4軸レーダー

import streamlit as st, requests, plotly.graph_objects as go
from scripts.compute_score import compute_vector

API_URL = "http://localhost:8000"

st.title("Illumination‑Core • 4‑Axis Inspector")

# 🔧 ユーザーが軸の重みをスライダーで操作
st.sidebar.markdown("### 軸の重みを調整")

weights = {
    "C": st.sidebar.slider("Citation (C)", 0.0, 1.0, 0.25),
    "R": st.sidebar.slider("Contradiction (R)", 0.0, 1.0, 0.25),
    "U": st.sidebar.slider("Reuse (U)", 0.0, 1.0, 0.25),
    "dH": st.sidebar.slider("Information Gain (ΔH)", 0.0, 1.0, 0.25),
}
# 正規化（合計1に）
total = sum(weights.values())
weights = {k: v/total if total > 0 else 0 for k, v in weights.items()}

tab1, tab2 = st.tabs(["URL / DOI", "Raw text"])

def call_api(payload: dict):
    r = requests.post(f"{API_URL}/score", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

# ========== 📄 URL / DOI タブ ================
with tab1:
    url = st.text_input("Resource URL か DOI を入力")

    if st.button("Analyze") and url:
        try:
            res = call_api({"url": url})
            st.session_state["last_url"] = url
            st.session_state["last_result_url"] = res
        except Exception as e:
            st.error(f"API error: {e}")

    # 結果表示（保存されていれば）
    if "last_result_url" in st.session_state:
        res = st.session_state["last_result_url"]
        score_result = compute_vector(
            res["norm"]["C"], res["norm"]["R"], res["norm"]["U"], res["norm"]["dH"],
            weights=weights
        )
        st.metric("Composite Score", round(score_result["score"], 3))
        radar = go.Figure(go.Scatterpolar(
            r=list(score_result["norm"].values()),
            theta=list(score_result["norm"].keys()),
            fill='toself'))
        st.plotly_chart(radar, use_container_width=True)
        st.json(score_result)

# ========== ✍ Raw Text タブ ================
with tab2:
    text = st.text_area("貼り付けテキスト（最大1万字）", height=200)

    if st.button("Analyze Text") and text:
        try:
            res = call_api({"text": text})
            st.session_state["last_text"] = text
            st.session_state["last_result_text"] = res
        except Exception as e:
            st.error(f"API error: {e}")

    if "last_result_text" in st.session_state:
        res = st.session_state["last_result_text"]
        score_result = compute_vector(
            res["norm"]["C"], res["norm"]["R"], res["norm"]["U"], res["norm"]["dH"],
            weights=weights
        )
        st.metric("ΔH only", round(score_result["norm"]["dH"], 3))
        radar = go.Figure(go.Scatterpolar(
            r=list(score_result["norm"].values()),
            theta=list(score_result["norm"].keys()),
            fill='toself'))
        st.plotly_chart(radar, use_container_width=True)
        st.json(score_result)
