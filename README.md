# illumination-core
# 照度コア (illumination-core)

> 信頼コストを下げるメタ仕組みを作り、文化圏を横断して配布する。

# Illumination Core 🔦

A 4-axis prototype system for visualizing the credibility of academic texts.

## Overview

Illumination Core allows users to evaluate documents (via DOI or raw text) along four independent axes:

- **C** — Citation density  
- **R** — Contradictions (e.g. refuting/supporting citations)  
- **U** — Reuse across other texts or codebases  
- **ΔH** — Information novelty (entropy shift)

The scores are rendered as radar charts and can be interactively weighted via sliders.

## Technologies

- **Frontend**: [Streamlit](https://streamlit.io/) UI with slider-controlled weight adjustment  
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/) endpoint for score computation  
- **Data sources**:  
  - OpenAlex for citation metadata  
  - Scite.ai (planned or conditional access)
- **Hosting**: [Fly.io](https://fly.io/)

## Purpose

This is an **educational, non-commercial prototype** exploring methods for visualizing trust and credibility in academic research.

> ⚠ This project is **not affiliated with Scite.ai** or any third-party data provider.  
> API access is either provisional or pending approval where applicable.

## Usage

To test locally:

```bash
# backend
uvicorn api.main:app --reload

# frontend
streamlit run app/streamlit_app.py
