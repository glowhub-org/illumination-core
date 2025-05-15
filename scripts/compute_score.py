# scripts/compute_score.py

import numpy as np
from typing import Dict

DEFAULT_WEIGHTS: Dict[str, float] = {
    "C": 0.25,
    "R": 0.25,
    "U": 0.25,
    "dH": 0.25
}

def compute_vector(c, r, u, dh, weights: Dict[str, float] = DEFAULT_WEIGHTS):
    norm = {
        "C": np.tanh(c / 100),
        "R": np.tanh(r / 10),
        "U": np.tanh(u / 50),
        "dH": np.tanh(dh / 2),
    }
    score = sum(weights[k] * norm[k] for k in norm)
    return {"score": score, "norm": norm}
