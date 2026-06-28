from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np
import pandas as pd


def build_probability_table(
    rows: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    event_col: str = "event_id",
    option_col: str = "option_id",
    odds_col: str | None = "decimal_odds",
    probability_col: str | None = None,
    output_col: str = "truth_probability",
) -> pd.DataFrame:
    """Build event-normalized probabilities from decimal odds or raw weights."""

    table = _as_frame(rows).copy()
    _require_columns(table, [event_col, option_col])

    if probability_col and probability_col in table.columns:
        raw = pd.to_numeric(table[probability_col], errors="coerce")
    elif odds_col and odds_col in table.columns:
        odds = pd.to_numeric(table[odds_col], errors="coerce")
        raw = 1.0 / odds.replace(0, np.nan)
    else:
        raise ValueError(
            f"Provide probability_col or an odds_col present in the table. "
            f"Available columns: {list(table.columns)}"
        )

    table["_raw_probability_weight"] = raw.fillna(0.0).clip(lower=0.0)
    table[output_col] = table.groupby(event_col)["_raw_probability_weight"].transform(_normalise_series)
    return table.drop(columns=["_raw_probability_weight"])


def _normalise_series(values: pd.Series) -> pd.Series:
    total = float(values.sum())
    if total <= 0:
        return pd.Series(np.full(len(values), 1.0 / max(len(values), 1)), index=values.index)
    return values / total


def _as_frame(rows: pd.DataFrame | Iterable[dict[str, Any]]) -> pd.DataFrame:
    if isinstance(rows, pd.DataFrame):
        return rows
    return pd.DataFrame(list(rows))


def _require_columns(table: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in table.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

