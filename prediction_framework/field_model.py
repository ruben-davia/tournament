from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np
import pandas as pd


def estimate_field_distribution(
    rows: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    event_col: str = "event_id",
    truth_probability_col: str = "truth_probability",
    popularity_col: str | None = "popularity_hint",
    output_col: str = "field_probability",
    chalk_weight: float = 1.0,
    popularity_weight: float = 1.0,
) -> pd.DataFrame:
    """Estimate how the field will pick each option.

    The field model is deliberately simple for the public framework: start with
    truth probability, optionally blend in a popularity/crowd hint, then
    normalize within each event.
    """

    table = rows.copy() if isinstance(rows, pd.DataFrame) else pd.DataFrame(list(rows))
    if event_col not in table.columns:
        raise ValueError(f"Missing required column: {event_col}")
    if truth_probability_col not in table.columns:
        raise ValueError(f"Missing required column: {truth_probability_col}")

    truth = pd.to_numeric(table[truth_probability_col], errors="coerce").fillna(0.0).clip(lower=0.0)
    weights = np.power(np.maximum(truth.to_numpy(float), 1e-12), chalk_weight)

    if popularity_col and popularity_col in table.columns:
        popularity = pd.to_numeric(table[popularity_col], errors="coerce").fillna(1.0).clip(lower=0.0)
        weights *= np.power(np.maximum(popularity.to_numpy(float), 1e-12), popularity_weight)

    table["_field_weight"] = weights
    table[output_col] = table.groupby(event_col)["_field_weight"].transform(_normalise_series)
    return table.drop(columns=["_field_weight"])


def _normalise_series(values: pd.Series) -> pd.Series:
    total = float(values.sum())
    if total <= 0:
        return pd.Series(np.full(len(values), 1.0 / max(len(values), 1)), index=values.index)
    return values / total

