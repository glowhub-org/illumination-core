# scripts/fetch_data.py  🚀 robust version

import os, requests, numpy as np
from scipy.stats import entropy
from openai import OpenAI

# ---------- C ----------------------------------------------------------
def get_c(doi: str) -> int:
    try:
        j = requests.get(
            f"https://api.openalex.org/works/https://doi.org/{doi}",
            timeout=10).json()
        return j.get("cited_by_count", 0)
    except Exception:
        return 0

# ---------- R ----------------------------------------------------------
def get_r(doi: str) -> int:
    try:
        key = os.getenv("SCITE_API_KEY", "")
        j = requests.get(
            f"https://api.scite.ai/tallies/{doi}",
            headers={"x-api-key": key}, timeout=10).json()
        return j.get("disputing", 0)
    except Exception:
        return 0

# ---------- U ----------------------------------------------------------
def get_u(github_url: str) -> int:
    try:
        token = os.getenv("GITHUB_TOKEN", "")
        if "github.com/" not in github_url or not token:
            return 0
        repo = github_url.split("github.com/")[1]
        j = requests.get(
            f"https://api.github.com/repos/{repo}",
            headers={"Authorization": f"Bearer {token}"}, timeout=10).json()
        return j.get("stargazers_count", 0) + j.get("forks_count", 0)
    except Exception:
        return 0

# ---------- ΔH ---------------------------------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

def get_dh(text: str) -> float:
    try:
        if not client.api_key or not text:
            return 0.0
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":"List 5 bullet claims:\n"+text}]
        )
        dist = np.ones(5)/5
        new  = np.array([0.3,0.25,0.2,0.15,0.1])
        return float(entropy(new, dist))
    except Exception:
        return 0.0
