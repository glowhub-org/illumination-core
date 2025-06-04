# tests/test_compute_score.py
import pytest
import numpy as np
from scripts.compute_score import compute_vector, DEFAULT_WEIGHTS

def test_compute_vector_basic():
    # Test with some example raw values
    c, r, u, dh = 50, 5, 20, 1.0 # Raw input values

    # Expected normalized values (approximate for tanh)
    # norm_c = np.tanh(50/100) = np.tanh(0.5) approx 0.4621
    # norm_r = np.tanh(5/10)   = np.tanh(0.5) approx 0.4621
    # norm_u = np.tanh(20/50)  = np.tanh(0.4) approx 0.3799
    # norm_dh = np.tanh(1.0/2) = np.tanh(0.5) approx 0.4621

    expected_norm_c = np.tanh(0.5)
    expected_norm_r = np.tanh(0.5)
    expected_norm_u = np.tanh(0.4)
    expected_norm_dh = np.tanh(0.5)

    # Expected S value
    # S = 1 - max(norm_c, norm_r, norm_u, norm_dh)
    # max_val = max(0.4621, 0.4621, 0.3799, 0.4621) = 0.4621
    # expected_s = 1 - 0.4621 = 0.5379
    expected_s = 1 - max(expected_norm_c, expected_norm_r, expected_norm_u, expected_norm_dh)
    expected_s = max(0, expected_s) # ensure non-negativity

    result = compute_vector(c, r, u, dh) # Using default weights

    # Check raw values
    assert result["raw"]["C"] == c
    assert result["raw"]["R"] == r
    assert result["raw"]["U"] == u
    assert result["raw"]["dH"] == dh
    assert result["raw"]["S"] == expected_s

    # Check normalized values (with tolerance for float comparison)
    assert np.isclose(result["norm"]["C"], expected_norm_c)
    assert np.isclose(result["norm"]["R"], expected_norm_r)
    assert np.isclose(result["norm"]["U"], expected_norm_u)
    assert np.isclose(result["norm"]["dH"], expected_norm_dh)
    assert np.isclose(result["norm"]["S"], expected_s)

    # Check overall score (calculated only from C, R, U, dH)
    expected_score = (DEFAULT_WEIGHTS["C"] * expected_norm_c +
                      DEFAULT_WEIGHTS["R"] * expected_norm_r +
                      DEFAULT_WEIGHTS["U"] * expected_norm_u +
                      DEFAULT_WEIGHTS["dH"] * expected_norm_dh)
    assert np.isclose(result["score"], expected_score)

def test_compute_vector_s_value_edge_cases():
    # Test case where S should be 0 (one norm value is 1 or >1)
    # np.tanh approaches 1 as input -> infinity. np.tanh(3) is very close to 1.
    # c=300 -> norm_c = np.tanh(300/100) = np.tanh(3) approx 0.995
    # Let's make one value very high to ensure S is 0
    c, r, u, dh = 1000, 1, 1, 0.1
    norm_c = np.tanh(1000/100) # np.tanh(10) is very close to 1.0
    norm_r = np.tanh(1/10)
    norm_u = np.tanh(1/50)
    norm_dh = np.tanh(0.1/2)

    expected_s_zero = 1 - max(norm_c, norm_r, norm_u, norm_dh)
    expected_s_zero = max(0, expected_s_zero) # Should be 0 or very close

    result_s_zero = compute_vector(c, r, u, dh)
    assert np.isclose(result_s_zero["norm"]["S"], expected_s_zero)
    assert np.isclose(result_s_zero["raw"]["S"], expected_s_zero)
    if not np.isclose(expected_s_zero, 0.0): # If tanh(10) is not exactly 1.0
        assert result_s_zero["norm"]["S"] < 0.01 # Ensure it's very small

    # Test case where S should be 1 (all norm values are 0)
    c, r, u, dh = 0, 0, 0, 0
    norm_c_zero = np.tanh(0) # 0
    norm_r_zero = np.tanh(0) # 0
    norm_u_zero = np.tanh(0) # 0
    norm_dh_zero = np.tanh(0) # 0

    expected_s_one = 1 - max(norm_c_zero, norm_r_zero, norm_u_zero, norm_dh_zero) # 1 - 0 = 1

    result_s_one = compute_vector(c, r, u, dh)
    assert result_s_one["norm"]["S"] == 1.0
    assert result_s_one["raw"]["S"] == 1.0

    # Check score is 0 when all inputs are 0
    assert result_s_one["score"] == 0.0

# Add pytest to requirements if not already there
# Create a simple requirements-dev.txt or update requirements.txt
# For now, assume pytest is available in the environment.
