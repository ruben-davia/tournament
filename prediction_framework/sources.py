from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np
import pandas as pd


QUALITY_WEIGHTS = {"high": 1.0, "medium": 0.65, "low": 0.35, "proxy": 0.20}


def build_source_probability_table(
    rows: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    event_col: str = "event_id",
    option_col: str = "option_id",
    source_col: str = "source",
    odds_col: str | None = "decimal_odds",
    probability_col: str | None = "source_probability",
    quality_col: str = "source_quality",
    direct_col: str = "is_direct_market",
    output_col: str = "truth_probability",
) -> pd.DataFrame:
    """Blend source probabilities into one event-normalized truth table.

    Each source is first normalized inside `(event, source)`. Sources are then
    blended by quality. Proxy markets get lower default weight than direct
    markets.
    """

    table = _as_frame(rows).copy()
    _require(table, [event_col, option_col, source_col])
    raw = pd.Series(np.nan, index=table.index, dtype=float)
    if probability_col and probability_col in table.columns:
        raw = pd.to_numeric(table[probability_col], errors="coerce")
    if odds_col and odds_col in table.columns:
        odds = pd.to_numeric(table[odds_col], errors="coerce")
        odds_probability = 1.0 / odds.replace(0, np.nan)
        raw = raw.fillna(odds_probability)
    if raw.isna().all():
        raise ValueError("Provide source_probability or decimal_odds.")

    table["_raw_source_probability"] = raw.fillna(0.0).clip(lower=0.0)
    table["source_normalized_probability"] = table.groupby([event_col, source_col])[
        "_raw_source_probability"
    ].transform(_normalise)
    table["source_weight"] = table.apply(
        lambda row: source_quality_weight(
            row.get(quality_col, "medium"),
            is_direct_market=_truthy(row.get(direct_col, True)),
        ),
        axis=1,
    )
    table["_weighted_probability"] = table["source_normalized_probability"] * table["source_weight"]

    group_cols = [event_col, option_col]
    keep_cols = [column for column in table.columns if column not in {"_raw_source_probability", "_weighted_probability"}]
    blended = (
        table.groupby(group_cols, as_index=False)
        .agg(
            source_probability_weight=("_weighted_probability", "sum"),
            source_count=(source_col, "nunique"),
            source_list=(source_col, lambda values: "; ".join(sorted(set(map(str, values))))),
            average_source_weight=("source_weight", "mean"),
        )
    )
    labels = table.drop_duplicates(group_cols)[[column for column in keep_cols if column not in {source_col, probability_col or "", odds_col or "", quality_col}]]
    labels = labels.loc[:, ~labels.columns.duplicated()]
    out = blended.merge(labels, on=group_cols, how="left")
    out[output_col] = out.groupby(event_col)["source_probability_weight"].transform(_normalise)
    return out.drop(columns=["source_probability_weight"])


def compare_source_probabilities(
    rows: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    event_col: str = "event_id",
    option_col: str = "option_id",
    source_col: str = "source",
    probability_col: str = "source_normalized_probability",
) -> pd.DataFrame:
    """Return disagreement diagnostics between normalized source probabilities."""

    table = _as_frame(rows).copy()
    _require(table, [event_col, option_col, source_col, probability_col])
    pivot = table.pivot_table(
        index=[event_col, option_col],
        columns=source_col,
        values=probability_col,
        aggfunc="mean",
    )
    rows_out = []
    for key, row in pivot.iterrows():
        values = pd.to_numeric(row.dropna(), errors="coerce").dropna()
        if values.empty:
            continue
        rows_out.append(
            {
                event_col: key[0],
                option_col: key[1],
                "source_count": int(len(values)),
                "min_probability": float(values.min()),
                "max_probability": float(values.max()),
                "source_disagreement": float(values.max() - values.min()),
                "mean_probability": float(values.mean()),
            }
        )
    return pd.DataFrame(rows_out)


def source_quality_weight(value: Any, *, is_direct_market: bool = True) -> float:
    quality = str(value or "medium").strip().lower()
    weight = QUALITY_WEIGHTS.get(quality, QUALITY_WEIGHTS["medium"])
    if not is_direct_market:
        weight = min(weight, QUALITY_WEIGHTS["proxy"])
    return float(weight)


def _normalise(values: pd.Series) -> pd.Series:
    total = float(values.sum())
    if total <= 0:
        return pd.Series(np.full(len(values), 1.0 / max(len(values), 1)), index=values.index)
    return values / total


def _truthy(value: Any) -> bool:
    return str(value).strip().lower() not in {"0", "false", "no", "proxy", "non", ""}


def _as_frame(rows: pd.DataFrame | Iterable[dict[str, Any]]) -> pd.DataFrame:
    return rows.copy() if isinstance(rows, pd.DataFrame) else pd.DataFrame(list(rows))


def _require(table: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in table.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
