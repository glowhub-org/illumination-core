import streamlit as st
import pandas as pd
from scripts.compute_score import load, calc

st.title("照度コア α – Illumination Dashboard")

df_raw = load("data/shadow_sample.json")

st.sidebar.header("Dial Weights")
w_c = st.sidebar.slider("C  (Citation density)", 0.0, 1.0, 0.5, 0.05)
w_r = st.sidebar.slider("R  (External contradiction)", 0.0, 1.0, 0.5, 0.05)

df = calc(df_raw.copy(), w_c, w_r)
st.write("### Illumination Scores")
st.dataframe(df)

st.bar_chart(df.set_index("title")["illumination"])
