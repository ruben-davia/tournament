from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np
import pandas as pd


CONFIDENCE_MULTIPLIER = {"low": 1.03, "medium": 1.07, "high": 1.12}


def apply_expert_signals(
    options: pd.DataFrame | Iterable[dict[str, Any]],
    signals: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    event_col: str = "event_id",
    option_col: str = "option_id",
    label_col: str = "label",
    target_col: str = "signal_target",
    direction_col: str = "signal_direction",
    confidence_col: str = "confidence",
    probability_col: str = "truth_probability",
    output_col: str = "truth_probability",
    max_combined_multiplier: float = 1.25,
) -> pd.DataFrame:
    """Apply reviewed expert signals as bounded probability adjustments.

    A signal target can match an option id, a label substring, or a generic
    option tag column such as `outcome_bucket` when present.
    """

    table = _as_frame(options).copy()
    signal_table = _as_frame(signals).copy()
    if table.empty or signal_table.empty:
        return table
    _require(table, [event_col, option_col, probability_col])
    _require(signal_table, [event_col, target_col, direction_col])

    table["_expert_log_weight"] = 0.0
    for _, signal in signal_table.iterrows():
        event = str(signal[event_col])
        target = str(signal[target_col]).strip().lower()
        direction = str(signal.get(direction_col, "up")).strip().lower()
        confidence = str(signal.get(confidence_col, "low")).strip().lower()
        multiplier = CONFIDENCE_MULTIPLIER.get(confidence, CONFIDENCE_MULTIPLIER["low"])
        signed = np.log(multiplier)
        if direction in {"down", "lower", "negative", "-"}:
            signed = -signed
        mask = table[event_col].astype(str).eq(event) & _target_mask(table, target, option_col, label_col)
        table.loc[mask, "_expert_log_weight"] += signed

    cap = max(float(max_combined_multiplier), 1.0)
    table["_expert_multiplier"] = np.exp(table["_expert_log_weight"].clip(-np.log(cap), np.log(cap)))
    base = pd.to_numeric(table[probability_col], errors="coerce").fillna(0.0).clip(lower=0.0)
    table[output_col] = (base * table["_expert_multiplier"]).groupby(table[event_col]).transform(_normalise)
    table["expert_multiplier"] = table["_expert_multiplier"]
    return table.drop(columns=["_expert_log_weight", "_expert_multiplier"])


def audit_expert_signals(
    signals: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    required_columns: tuple[str, ...] = ("event_id", "signal_target", "signal_direction", "confidence", "source_url"),
) -> pd.DataFrame:
    """Flag expert signals that are not ready to influence probabilities."""

    table = _as_frame(signals).copy()
    rows = []
    allowed_directions = {"up", "down", "higher", "lower", "positive", "negative", "+", "-"}
    allowed_confidence = set(CONFIDENCE_MULTIPLIER)
    for _, row in table.iterrows():
        issues = []
        for column in required_columns:
            if column not in table.columns or not str(row.get(column, "")).strip():
                issues.append(f"missing_{column}")
        if str(row.get("signal_direction", "")).strip().lower() not in allowed_directions:
            issues.append("unknown_direction")
        if str(row.get("confidence", "")).strip().lower() not in allowed_confidence:
            issues.append("unknown_confidence")
        rows.append({**row.to_dict(), "status": "ok" if not issues else "needs_review", "issue": ";".join(issues)})
    return pd.DataFrame(rows)


def _target_mask(table: pd.DataFrame, target: str, option_col: str, label_col: str) -> pd.Series:
    mask = table[option_col].astype(str).str.lower().eq(target)
    if label_col in table.columns:
        mask = mask | table[label_col].astype(str).str.lower().str.contains(target, regex=False, na=False)
    for column in ("outcome_bucket", "result_bucket", "tags"):
        if column in table.columns:
            mask = mask | table[column].astype(str).str.lower().str.contains(target, regex=False, na=False)
    return mask


def _normalise(values: pd.Series) -> pd.Series:
    total = float(values.sum())
    if total <= 0:
        return pd.Series(np.full(len(values), 1.0 / max(len(values), 1)), index=values.index)
    return values / total


def _as_frame(rows: pd.DataFrame | Iterable[dict[str, Any]]) -> pd.DataFrame:
    return rows.copy() if isinstance(rows, pd.DataFrame) else pd.DataFrame(list(rows))


def _require(table: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in table.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
