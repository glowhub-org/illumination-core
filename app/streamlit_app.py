#照度コア - Illumination Core
# Developed by Tasuku + ChatGPT (Sushichi), 2025

# app/streamlit_app.py  🔥 保存付き4軸レーダー

import streamlit as st, requests, plotly.graph_objects as go
from scripts.compute_score import compute_vector
# --- make repo root importable --------------------------------------
import pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent  # <- リポジトリ直下
if str(root) not in sys.path:
    sys.path.append(str(root))
# --------------------------------------------------------------------

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
        st.text(f"影 (S): {res['raw']['S']:.2f}") # Display S value

        # Prepare for radar chart
        theta_values = ["C", "R", "U", "ΔH", "S"]
        # Use norm values from the API response 'res' for the radar chart for accuracy
        r_values = [
            res["norm"]["C"],
            res["norm"]["R"],
            res["norm"]["U"],
            res["norm"]["dH"],
            res["norm"]["S"]
        ]

        # Define colors for radar chart sectors
        radar_colors = ['#1f77b4',  # Muted Blue (Plotly default blue)
                        '#ff7f0e',  # Safety Orange (Plotly default orange)
                        '#2ca02c',  # Cooked Asparagus Green (Plotly default green)
                        '#d62728',  # Brick Red (Plotly default red)
                        'grey']     # Grey for S

        radar = go.Figure(go.Scatterpolar(
            r=r_values,
            theta=theta_values,
            fill='toself',
            marker=dict(colors=radar_colors) # Specify colors for each sector
        ))
        st.plotly_chart(radar, use_container_width=True)
        st.json(res) # Show the full API response

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
        st.text(f"影 (S): {res['raw']['S']:.2f}") # Display S value

        # Prepare for radar chart
        theta_values = ["C", "R", "U", "ΔH", "S"]
        # Use norm values from the API response 'res' for the radar chart for accuracy
        r_values = [
            res["norm"]["C"],
            res["norm"]["R"],
            res["norm"]["U"],
            res["norm"]["dH"],
            res["norm"]["S"]
        ]

        # Define colors for radar chart sectors
        radar_colors = ['#1f77b4',  # Muted Blue (Plotly default blue)
                        '#ff7f0e',  # Safety Orange (Plotly default orange)
                        '#2ca02c',  # Cooked Asparagus Green (Plotly default green)
                        '#d62728',  # Brick Red (Plotly default red)
                        'grey']     # Grey for S

        radar = go.Figure(go.Scatterpolar(
            r=r_values,
            theta=theta_values,
            fill='toself',
            marker=dict(colors=radar_colors) # Specify colors for each sector
        ))
        st.plotly_chart(radar, use_container_width=True)
        st.json(res) # Show the full API response
