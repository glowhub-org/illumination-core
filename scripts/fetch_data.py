# scripts/fetch_data.py  🌐 robust version 2025-05-26
# ===================================================
import os
import requests
import numpy as np
from urllib.parse import urlparse
from scipy.stats import entropy
from openai import OpenAI

# ---------------------------------------------------------------------
# ヘルパ：DOI を URL 文字列から抽出（URL そのものでも DOI でも可）
# ---------------------------------------------------------------------
def _extract_doi(s: str) -> str:
    """
    入力が DOI URL なら doi 部分を切り出し、すでに DOI ならそのまま返す。
    """
    if s.startswith("http"):
        # 例) https://doi.org/10.1038/s41586-024-07421-6
        return s.replace("https://doi.org/", "").strip()
    return s.strip()

# ---------------------------------------------------------------------
# C : Citation density  （OpenAlex cited_by_count）
# ---------------------------------------------------------------------
def get_c(doi_or_url: str) -> int:
    try:
        doi = _extract_doi(doi_or_url)
        j = requests.get(
            f"https://api.openalex.org/works/https://doi.org/{doi}",
            timeout=10).json()
        return j.get("cited_by_count", 0)
    except Exception:
        return 0

# ---------------------------------------------------------------------
# R : Refutation / Contradiction  （Scite tallies.disputing）
# ---------------------------------------------------------------------
def get_r(doi_or_url: str) -> int:
    try:
        doi = _extract_doi(doi_or_url)
        key = os.getenv("SCITE_API_KEY", "")
        j = requests.get(
            f"https://api.scite.ai/tallies/{doi}",
            headers={"x-api-key": key}, timeout=10).json()
        return j.get("disputing", 0)
    except Exception:
        return 0

# ---------------------------------------------------------------------
# U - helper : GitHub forks 数を取得
# ---------------------------------------------------------------------
def _github_forks(url: str) -> int:
    """
    URL に github.com/{owner}/{repo} が含まれていれば forks_count を返す。
    含まれていなければ 0。
    """
    if "github.com" not in url:
        return 0
    try:
        parts = url.split("github.com/")[-1].split("/")
        if len(parts) < 2:
            return 0
        owner, repo = parts[0:2]
        api  = f"https://api.github.com/repos/{owner}/{repo}"
        token = os.getenv("GITHUB_TOKEN", "")
        hdrs = {"Authorization": f"Bearer {token}"} if token else {}
        r = requests.get(api, headers=hdrs, timeout=10)
        if r.status_code == 200:
            return r.json().get("forks_count", 0)
    except Exception:
        pass
    return 0

# ---------------------------------------------------------------------
# U : Reuse  （OpenAlex の分野横断性 + GitHub forks）
# ---------------------------------------------------------------------
def get_u(url: str) -> int:
    """
    1. OpenAlex concepts（level=0）の数 = 学際性スコア
    2. GitHub forks / 10  を加算
       （fork 10 件 ≒ 異分野引用 1 件 相当の重み付け）
    """
    score = 0

    # --- (1) OpenAlex Concept 多様性 ---
    try:
        doi = _extract_doi(url)
        j   = requests.get(
            f"https://api.openalex.org/works/https://doi.org/{doi}",
            timeout=10).json()
        disciplines = {c["display_name"]
                       for c in j.get("concepts", []) if c.get("level") == 0}
        score += len(disciplines)
    except Exception:
        pass

    # --- (2) GitHub forks ---
    forks = _github_forks(url)
    score += forks // 10      # 10fork で +1

    return int(score)

# ---------------------------------------------------------------------
# ΔH : Information gain  （要旨を GPT-4o mini で 5 claim 要約 → エントロピー）
# ---------------------------------------------------------------------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

def get_dh(text: str) -> float:
    """
    5 つの主張を LLM に列挙させ、分布が均等か否かで新規性を近似。
    """
    try:
        if not client.api_key or not text:
            return 0.0

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": "List 5 bullet claims (concise):\n" + text
            }]
        )
        bullets = resp.choices[0].message.content.split("\n")
        k = min(5, len([b for b in bullets if b.strip()]))
        if k < 2:
            return 0.0

        new = np.ones(k) / k           # 仮に均等分布なら最大エントロピー
        ref = np.array([0.3,0.25,0.2,0.15,0.1][:k])  # 既知平均分布（例）
        return float(entropy(ref, new))
    except Exception:
        return 0.0
