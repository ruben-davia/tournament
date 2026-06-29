from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class BackwardValueModel:
    coefficients: pd.DataFrame
    fitted_values: pd.DataFrame
    metadata: dict[str, Any]


def fit_backward_value_model(
    rollouts: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    checkpoint_col: str = "checkpoint",
    feature_cols: tuple[str, ...] = ("current_rank", "points_gap", "doublettes_left"),
    terminal_value_col: str = "terminal_value",
) -> BackwardValueModel:
    """Fit simple Monte Carlo continuation values from final outcomes backward.

    This is a lightweight public version of the advanced idea used in adaptive
    contests: simulate many futures, observe final utility, then estimate what
    each intermediate state is worth before choosing the current action.
    """

    table = rollouts.copy() if isinstance(rollouts, pd.DataFrame) else pd.DataFrame(list(rollouts))
    required = [checkpoint_col, terminal_value_col, *feature_cols]
    missing = [column for column in required if column not in table.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if table.empty:
        return BackwardValueModel(pd.DataFrame(), pd.DataFrame(), {"feature_cols": list(feature_cols)})

    fitted_frames = []
    coefficient_rows = []
    for checkpoint in sorted(table[checkpoint_col].dropna().unique(), reverse=True):
        frame = table[table[checkpoint_col].eq(checkpoint)].copy()
        x = _design_matrix(frame, feature_cols)
        y = pd.to_numeric(frame[terminal_value_col], errors="coerce").fillna(0.0).to_numpy(float)
        coef = np.linalg.lstsq(x, y, rcond=None)[0]
        frame["continuation_value"] = x @ coef
        fitted_frames.append(frame)
        coefficient_rows.extend(
            {
                checkpoint_col: checkpoint,
                "term": term,
                "coefficient": float(value),
            }
            for term, value in zip(("intercept", *feature_cols), coef, strict=True)
        )

    return BackwardValueModel(
        coefficients=pd.DataFrame(coefficient_rows),
        fitted_values=pd.concat(fitted_frames, ignore_index=True),
        metadata={
            "method": "least_squares_backward_monte_carlo",
            "feature_cols": list(feature_cols),
            "terminal_value_col": terminal_value_col,
        },
    )


def _design_matrix(frame: pd.DataFrame, feature_cols: tuple[str, ...]) -> np.ndarray:
    columns = [np.ones(len(frame), dtype=float)]
    for column in feature_cols:
        values = pd.to_numeric(frame[column], errors="coerce").fillna(0.0).to_numpy(float)
        columns.append(values)
    return np.column_stack(columns)
