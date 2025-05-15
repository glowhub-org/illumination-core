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
※ Note: Illumination Core does not currently support full-text search or document recommendation.  
It is designed to evaluate documents provided by the user (via DOI or pasted text).  
Future versions may include search and filtering tools based on custom illumination profiles.

※ 現時点では、照度コアには論文の検索・推薦機能は搭載されていません。  
ユーザーが指定した DOI または本文に対して照度分析を行う構成となっています。  
将来的には、照度設定に応じた論文検索やランキング機能の追加も検討中です。


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

Beyond evaluation, Illumination Core can also serve as a cognitive tool for academic exploration and creative thinking.

By adjusting the axis weights, users can shift the focus depending on their current intellectual mode:

- **Focused reading**: emphasize ΔH (novelty) to discover new ideas
- **Reliability-oriented**: emphasize C (citations) and U (reuse) to find well-established work
- **Brainstorming / creative synthesis**: emphasize ΔH and U to locate high-potential, reusable research
- **Critical review**: emphasize R (contradictions) to explore points of tension in the field

In this way, the system acts not as a judgment engine, but as a **personalizable lens for thought**, adaptable to your current cognitive needs.

---

照度コアは単なる評価ツールではなく、学術的な探究や創造的思考のための**認知補助ツール**としても活用できます。

ユーザー自身の知的モードに応じて軸の重みを調整することで、論文の“照らし方”を変えることができます：

- **集中して読みたいとき**：ΔH（新規性）を強調して、新たな着想を得る
- **信頼性重視のとき**：C（引用密度）とU（再利用）を強めにして、定評ある研究にアクセスする
- **発想モードのとき**：ΔHとUを上げて、応用可能性や再構成しやすい研究を拾う
- **批判的レビューや議論整理のとき**：R（反証や矛盾）を強調して、分野内の緊張点を掘り起こす

このように照度コアは、「読む価値」を押しつけるのではなく、「どう読みたいか」に合わせて灯を調整できる**柔軟な思考のレンズ**です。

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
