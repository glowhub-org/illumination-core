# illumination-core
# 照度コア (illumination-core)

> 信頼コストを下げるメタ仕組みを作り、文化圏を横断して配布する。

## 4-Axis Illumination
- **C** Citation density  
- **R** External contradiction  
- **U** Reuse rate  
- **ΔH** Information gain
現状はα版
---

## 🌍 English Overview

### 🎯 Purpose

> **Build a meta-framework that lowers the *cost of trust* and can be shared across cultural and disciplinary borders.**  
> The system makes “shadows” (un-examined gaps, missing replications, one-sided citations) visible and adjustable.

### 🔧 4-Axis Illumination Model

| Axis | Symbol | What it measures | Typical source |
|------|--------|------------------|----------------|
| Citation density | **C** | How often the work is cited | OpenAlex, CrossRef |
| External contradiction | **R** | How many *contrasting* citations or critiques exist | scite.ai, citation-intent models |
| Reuse rate | **U** | How frequently methods / data are reused in later work | text-embedding similarity |
| Information gain | **ΔH** | Novelty or KL-divergence of claims vs. prior knowledge | LLM claim extraction |

### 🚀 Quick Start

```bash
# clone & enter repo
git clone https://github.com/tasuku-9/illumination-core.git
cd illumination-core

# install deps (Python ≥3.9)
pip install -r requirements.txt

# launch dashboard
streamlit run app/streamlit_app.py

illumination-core/
│
├─ app/                  ← Streamlit UI
│   ├─ streamlit_app.py
│   └─ data/             ← demo data JSON
├─ scripts/              ← score calculation & future NLP pipelines
│   ├─ __init__.py
│   └─ compute_score.py
├─ docs/                 ← design notes, screenshots
├─ requirements.txt
└─ README.md


**How to add**

1. Open `README.md` in VS Code.  
2. Scroll to the end (or wherever you like) and paste the above block.  
3. `Ctrl + S` → **+** (Stage) → commit message `add English README section` → ✔ Commit → 🔄 Push.

That’s all—now English readers will instantly grasp what “照度コア (illumination-core)” does.  
Whenever you update the Japanese part, just mirror the change in this English block. Good luck and ping me anytime you want more polish!

If you have any questions, please feel free to open an Issue or PR. But replies can be slow.