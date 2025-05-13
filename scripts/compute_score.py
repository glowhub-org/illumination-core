# scripts/compute_score.py  🚀 4‑Axis β

from typing import Dict

# 軸ごとのデフォルト重み
DEFAULT_WEIGHTS: Dict[str, float] = {
    "C": 0.35,   # Citation density
    "R": 0.30,   # External contradiction
    "U": 0.20,   # Reuse rate
    "dH": 0.15   # Information gain
}

def _normalize(raw: float, max_val: float = 1.0) -> float:
    """0‑1 正規化（あふれは 1.0 に丸める）"""
    return min(raw / max_val, 1.0) if max_val else 0.0

def compute_vector(c_raw: float, r_raw: float,
                   u_raw: float, dh_raw: float,
                   weights: Dict[str, float] = DEFAULT_WEIGHTS
                   ) -> Dict[str, Dict]:
    """
    4 軸の raw 値を受け取り
      • 正規化 vec_norm
      • 合計スコア score
    を返す
    """
    vec_raw = {"C": c_raw, "R": r_raw, "U": u_raw, "dH": dh_raw}
    vec_norm = {k: _normalize(v) for k, v in vec_raw.items()}
    score = sum(weights[k] * vec_norm[k] for k in vec_norm)
    return {"raw": vec_raw, "norm": vec_norm, "score": score}
