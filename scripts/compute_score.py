import numpy as np
from typing import Dict

DEFAULT_WEIGHTS: Dict[str, float] = {
    "C": 0.25,
    "R": 0.25,
    "U": 0.25,
    "dH": 0.25
}

def compute_vector(c, r, u, dh, weights: Dict[str, float] = DEFAULT_WEIGHTS):
    # Calculate normalized values for C, R, U, dH
    norm_c = np.tanh(c / 100)
    norm_r = np.tanh(r / 10)
    norm_u = np.tanh(u / 50)
    norm_dh = np.tanh(dh / 2)

    # Store them in a dictionary for easier access
    current_norm_values = {
        "C": norm_c,
        "R": norm_r,
        "U": norm_u,
        "dH": norm_dh
    }

    # Calculate S_raw from the normalized values of C, R, U, dH
    # Ensure S is not negative (it shouldn't be if norms are >=0 and max is used correctly)
    s_value = 1 - max(current_norm_values.values())
    s_value = max(0, s_value) # Ensure non-negativity, just in case

    # The composite score is calculated using only C, R, U, dH and their weights
    # Iterate over the keys present in the input `weights` dictionary
    score = sum(weights[key] * current_norm_values[key] for key in weights if key in current_norm_values)

    return {
        "score": score,
        "norm": {
            "C": norm_c,
            "R": norm_r,
            "U": norm_u,
            "dH": norm_dh,
            "S": s_value  # S is already normalized (0-1 range)
        },
        "raw": { # Store original inputs and the new S value
            "C": c,
            "R": r,
            "U": u,
            "dH": dh,
            "S": s_value
        }
    }
