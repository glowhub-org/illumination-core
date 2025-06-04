# 照度コア - Illumination Core
# Developed by Tasuku + ChatGPT (Sushichi), 2025

# app/streamlit_app.py  🔥 保存付き5軸レーダー

import streamlit as st, requests, plotly.graph_objects as go
# ------------------------------------------------------------
# repo 直下を import パスに追加
import pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
if str(root) not in sys.path:
    sys.path.append(str(root))
# ------------------------------------------------------------
from scripts.compute_score import compute_vector

API_URL = "http://localhost:8000"   # ← ローカル開発用

st.title("Illumination-Core • 5-Axis Inspector")

# ──────────────────────────────────────
# 軸ウェイト（S はまだ合成に入れない）
st.sidebar.markdown("### 軸の重みを調整")
weights = {
    "C":  st.sidebar.slider("Citation (C)",        0.0, 1.0, 0.25),
    "R":  st.sidebar.slider("Contradiction (R)",   0.0, 1.0, 0.25),
    "U":  st.sidebar.slider("Reuse (U)",           0.0, 1.0, 0.25),
    "dH": st.sidebar.slider("Information Gain (ΔH)", 0.0, 1.0, 0.25),
}
total = sum(weights.values())
weights = {k: v/total if total else 0 for k, v in weights.items()}

tab_url, tab_text = st.tabs(["URL / DOI", "Raw text"])

def call_api(payload: dict):
    r = requests.post(f"{API_URL}/score", json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

# ========== URL / DOI ==========
with tab_url:
    url = st.text_input("Resource URL か DOI を入力")

    if st.button("Analyze") and url:
        try:
            res = call_api({"url": url})
            st.session_state["url_res"] = res
        except Exception as e:
            st.error(f"API error: {e}")

    if "url_res" in st.session_state:
        res = st.session_state["url_res"]

        # 4 軸合成スコア
        score = compute_vector(
            res["norm"]["C"], res["norm"]["R"],
            res["norm"]["U"], res["norm"]["dH"],
            weights=weights
        )
        st.metric("Composite Score", round(score["score"], 3))
        st.write(f"影 (S): **{res['raw']['S']:.2f}**")

        # 5 軸レーダー
        theta = ["C", "R", "U", "ΔH", "S"]
        r_vals = [
            res["norm"]["C"], res["norm"]["R"],
            res["norm"]["U"], res["norm"]["dH"],
            res["norm"]["S"]
        ]
        radar = go.Figure(go.Scatterpolar(
            r=r_vals, theta=theta, fill='toself',
            line=dict(color='rgba(150,150,150,0.5)')
        ))
        st.plotly_chart(radar, use_container_width=True)
        st.json(res)

# ========== Raw text ==========
with tab_text:
    text = st.text_area("貼り付けテキスト（最大1万字）", height=200)

    if st.button("Analyze Text") and text:
        try:
            res = call_api({"text": text})
            st.session_state["text_res"] = res
        except Exception as e:
            st.error(f"API error: {e}")

    if "text_res" in st.session_state:
        res = st.session_state["text_res"]
        st.metric("ΔH (raw)", round(res["raw"]["dH"], 3))
        st.write(f"影 (S): **{res['raw']['S']:.2f}**")

        theta = ["C", "R", "U", "ΔH", "S"]
        r_vals = [
            res["norm"]["C"], res["norm"]["R"],
            res["norm"]["U"], res["norm"]["dH"],
            res["norm"]["S"]
        ]
        radar = go.Figure(go.Scatterpolar(
            r=r_vals, theta=theta, fill='toself',
            line=dict(color='rgba(150,150,150,0.5)')
        ))
        st.plotly_chart(radar, use_container_width=True)
        st.json(res)