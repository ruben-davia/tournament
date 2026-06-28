from __future__ import annotations

import numpy as np
import pandas as pd


def add_value_diagnostics(
    rows: pd.DataFrame,
    *,
    truth_probability_col: str = "truth_probability",
    field_probability_col: str = "field_probability",
    points_col: str = "points_if_hit",
) -> pd.DataFrame:
    out = rows.copy()
    truth = pd.to_numeric(out[truth_probability_col], errors="coerce").fillna(0.0)
    field = pd.to_numeric(out[field_probability_col], errors="coerce").fillna(0.0)
    points = pd.to_numeric(out.get(points_col, 1.0), errors="coerce").fillna(1.0)

    out["probability_edge"] = truth - field
    out["leverage_ratio"] = truth / np.maximum(field, 1e-12)
    out["expected_points"] = truth * points
    out["contrarian_value"] = out["expected_points"] * out["leverage_ratio"]
    return out

