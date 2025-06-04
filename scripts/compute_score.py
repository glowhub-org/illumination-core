# scripts/compute_score.py
# ---------------------------------------------------------------
# 4  + 影ベクトル S を返すユーティリティ

def _normalize(v: dict) -> dict:
    """各軸値を 0-1 に線形正規化（最大値=1）"""
    vmax = max(v.values()) or 1
    return {k: x / vmax for k, x in v.items()}

def compute_vector(c: int, r: int, u: int, dh: float, *, weights: dict | None = None):
    """
    4軸 + 影 S を計算して dict で返す
      - raw  : 入力そのまま & S_raw
      - norm : 0-1 正規化値 & S_norm (=S_raw)
      - score: C,R,U,ΔH の合成スコア（S は合成に含めない）
    """
    raw = {"C": c, "R": r, "U": u, "dH": dh}

    # ---------- 影ベクトル SRaw = 1 - max(正規化C,R,U,ΔH) ----------
    norm4 = _normalize(raw)
    s_raw = 1 - max(norm4.values())
    raw["S"]  = s_raw
    norm4["S"] = s_raw          # すでに 0-1 範囲なのでそのまま

    # ---------- 合成スコア（Sを除く4軸） ----------
    w = weights or {"C": .25, "R": .25, "U": .25, "dH": .25}
    score = sum(norm4[k] * w.get(k, 0) for k in ("C", "R", "U", "dH"))

    return {"score": score, "raw": raw, "norm": norm4}
