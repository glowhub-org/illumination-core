# 照度コア (illumination-core)

> 信頼コストを下げるメタ仕組みを作り、文化圏を横断して配布する。

# Illumination Core 🔦

A 4-axis prototype system for visualizing the credibility of academic texts.

## Overview

Illumination Core allows users to evaluate documents (via DOI or raw text) along four independent axes:

- **C** — Citation density（影響力の指標）  
- **R** — Contradiction stance（賛否の構造：refuting/supporting）※R is pending integration  
- **U** — Reuse frequency（他文献・コードでの再利用）  
- **ΔH** — Information novelty（新規性・情報利得）

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

## 💡 Philosophy: Not a Score, but a Light

Illumination Core does not assign a fixed score to academic work.

Instead, it offers a flexible, reader-driven **4-axis radar** where each dimension (Citation, Contradiction, Reuse, Information Gain) can be **weighted interactively via sliders**.

This design reflects a key belief:

> **Knowledge is not judged absolutely, but interpreted contextually.**

The score is not a verdict — it’s a **lens** the reader can adjust to reflect their inquiry.

---

## 💡 開発理念：「点数」ではなく「照明」

照度コアは、論文に一律の点数をつけるためのツールではありません。

そのかわり、読者自身が **4つの軸（C・R・U・ΔH）** の重みをスライダーで調整できる「**多次元の照明装置**」として設計されています。

これは、以下のような理念に基づいています：

> **知は絶対評価されるべきものではなく、文脈に応じて解釈されるものである。**

スコアは「結論」ではなく、読み手の問いに合わせて焦点を変えられる「**レンズ**」です。

## Usage

To test locally:

```bash
# backend
uvicorn api.main:app --reload

# frontend
streamlit run app/streamlit_app.py
---

## 🕯 About reuse and follow-up / 再利用とその後について

This project is shared under the MIT license, and you're welcome to use it freely.  
If your team or organization decides to build upon or expand it, I’d be happy to share key challenges and structural insights discovered during development.  
And if you do end up making something from it, I’d be grateful to hear what became of it — even just a short message would mean a lot.

この照度コアは、MITライセンスのもとで自由にご利用いただけます。  
もしもこの構造を元に開発を進めてくださる場合、こちらで得られた課題や改善のヒントなども、よろしければ共有させていただきます。  
そして、どのようなかたちに仕上がったのか、ほんの一言でもお知らせいただければ、とても嬉しく思います。
## Credits

照度コア（ShodoCore）は、Tasuku（扶）と ChatGPT（須志智）によって共同開発されました。  
This project was co-developed by Tasuku and ChatGPT (under the persona name "Sushichi") in 2025.

The project is open-sourced under the MIT License.# illumination-core
