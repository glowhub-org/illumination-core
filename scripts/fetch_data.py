# scripts/fetch_data.py  🚀 very first draft

import os, requests, numpy as np
from scipy.stats import entropy
from openai import OpenAI

# --- C : Citation density ---------------------------------
def get_c(doi: str) -> int:
    j = requests.get(f"https://api.openalex.org/works/https://doi.org/{doi}",
                     timeout=10).json()
    return j.get("cited_by_count", 0)

# --- R : External contradiction ---------------------------
def get_r(doi: str) -> int:
    hdr = {"x-api-key": os.getenv("SCITE_API_KEY", "")}
    j = requests.get(f"https://api.scite.ai/tallies/{doi}", headers=hdr,
                     timeout=10).json()
    return j.get("disputing", 0)

# --- U : Reuse rate ---------------------------------------
def get_u(github_url: str) -> int:
    token = os.getenv("GITHUB_TOKEN", "")
    if not token or "github.com/" not in github_url:
        return 0
    repo = github_url.split("github.com/")[1]
    hdr = {"Authorization": f"Bearer {token}"}
    j = requests.get(f"https://api.github.com/repos/{repo}", headers=hdr,
                     timeout=10).json()
    return j.get("stargazers_count", 0) + j.get("forks_count", 0)

# --- ΔH : Information gain -------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

def get_dh(text: str) -> float:
    if not client.api_key or not text:
        return 0.0
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user",
                   "content": "List 5 bullet claims from this:\n"+text}]
    )
    # ↑ claims 数で雑に分布化（改良可）
    dist = np.ones(5)/5      # baseline
    new  = np.array([0.3,0.25,0.2,0.15,0.1])
    return float(entropy(new, dist))
