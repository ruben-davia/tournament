from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import numpy as np
import pandas as pd


def add_pick_risk_flags(
    options: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    event_col: str = "event_id",
    probability_col: str = "truth_probability",
    field_col: str = "field_probability",
    expert_support_col: str = "expert_support",
    low_probability_threshold: float = 0.06,
    crowded_threshold: float = 0.30,
) -> pd.DataFrame:
    """Attach practical risk flags used before building a portfolio."""

    table = _as_frame(options).copy()
    flags = []
    for _, row in table.iterrows():
        row_flags = []
        p = _float(row.get(probability_col))
        field = _float(row.get(field_col))
        expert = _float(row.get(expert_support_col, np.nan))
        if p < low_probability_threshold:
            row_flags.append("low_probability")
        if field >= crowded_threshold:
            row_flags.append("crowded")
        if not np.isnan(expert) and expert < 0:
            row_flags.append("expert_conflict")
        if str(row.get("is_proxy_market", "")).strip().lower() in {"1", "true", "yes"}:
            row_flags.append("proxy_market")
        flags.append(";".join(row_flags))
    table["risk_flags"] = flags
    table["risk_level"] = table["risk_flags"].map(_risk_level)
    return table


def build_risk_capped_portfolio(
    options: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    event_col: str = "event_id",
    option_col: str = "option_id",
    probability_col: str = "truth_probability",
    field_col: str = "field_probability",
    points_col: str = "points_if_hit",
    expert_support_col: str = "expert_support",
    min_probability: float = 0.06,
    max_field_probability: float | None = None,
    expert_conflict_floor: float = -0.5,
    anticrowd_weight: float = 0.35,
    upside_weight: float = 0.20,
    risk_penalty: float = 0.50,
    strategy_name: str = "risk_capped",
) -> pd.DataFrame:
    """Choose one option per event using EV, anti-crowd value, and risk caps."""

    table = add_pick_risk_flags(
        options,
        event_col=event_col,
        probability_col=probability_col,
        field_col=field_col,
        expert_support_col=expert_support_col,
        low_probability_threshold=min_probability,
    )
    rows = []
    for event, group in table.groupby(event_col, sort=False):
        candidates = group[pd.to_numeric(group[probability_col], errors="coerce").fillna(0.0).ge(min_probability)].copy()
        if max_field_probability is not None and not candidates.empty:
            less_crowded = candidates[pd.to_numeric(candidates[field_col], errors="coerce").fillna(0.0).le(max_field_probability)].copy()
            if not less_crowded.empty:
                candidates = less_crowded
        if expert_support_col in candidates.columns and not candidates.empty:
            aligned = candidates[pd.to_numeric(candidates[expert_support_col], errors="coerce").fillna(0.0).ge(expert_conflict_floor)].copy()
            if not aligned.empty:
                candidates = aligned
        if candidates.empty:
            candidates = group.copy()

        p = pd.to_numeric(candidates[probability_col], errors="coerce").fillna(0.0)
        field = _numeric_series(candidates, field_col, default=0.0)
        points = _numeric_series(candidates, points_col, default=1.0)
        expert = _numeric_series(candidates, expert_support_col, default=0.0)
        severe = candidates["risk_level"].eq("high").astype(float)
        candidates["_risk_capped_score"] = (
            p * points
            + anticrowd_weight * (p - field)
            + upside_weight * np.sqrt(np.maximum(p, 0.0))
            + 0.10 * expert
            - risk_penalty * severe
        )
        pick = candidates.sort_values(["_risk_capped_score", probability_col], ascending=False).iloc[0]
        rows.append(
            {
                "strategy": strategy_name,
                event_col: event,
                option_col: pick[option_col],
                "risk_capped_score": float(pick["_risk_capped_score"]),
                "risk_flags": pick.get("risk_flags", ""),
                "risk_level": pick.get("risk_level", ""),
                "selection_reason": _selection_reason(pick, probability_col, field_col),
            }
        )
    return pd.DataFrame(rows)


def rank_risk_frontier(
    summary: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    paid_col: str = "p_paid",
    top1_col: str = "p_top_1",
    regret_col: str = "regret_vs_baseline",
    concentration_col: str = "single_match_concentration",
    tolerance: float = 0.01,
) -> pd.DataFrame:
    """Use after simulation to choose among near-optimal strategies.

    The frontier first keeps strategies within `tolerance` of the best
    paid-place probability, then ranks them by top-1 upside and risk penalties.
    Pass a strategy summary table with `p_paid` and `p_top_1`; missing regret
    or concentration columns default to zero.
    """

    table = _as_frame(summary).copy()
    if table.empty:
        return table
    for column in (paid_col, top1_col, regret_col, concentration_col):
        if column not in table.columns:
            table[column] = 0.0
        table[column] = pd.to_numeric(table[column], errors="coerce").fillna(0.0)
    best_paid = float(table[paid_col].max())
    table["frontier_qualified"] = table[paid_col].ge(best_paid - float(tolerance))
    table["frontier_score"] = (
        4.0 * table[paid_col]
        + 1.5 * table[top1_col]
        - 0.8 * table[regret_col].clip(lower=0.0)
        - 0.4 * table[concentration_col].clip(lower=0.0)
    )
    return table.sort_values(["frontier_qualified", "frontier_score", paid_col, top1_col], ascending=False).reset_index(drop=True)


def _selection_reason(row: pd.Series, probability_col: str, field_col: str) -> str:
    return (
        f"p={_float(row.get(probability_col)):.3f}; "
        f"field={_float(row.get(field_col)):.3f}; "
        f"risk={row.get('risk_level', '')}; "
        f"flags={row.get('risk_flags', '') or 'none'}"
    )


def _risk_level(flags: str) -> str:
    values = {flag for flag in str(flags).split(";") if flag}
    if {"low_probability", "expert_conflict"} <= values:
        return "high"
    if "low_probability" in values or "expert_conflict" in values:
        return "medium"
    if values:
        return "low"
    return "none"


def _float(value: Any) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError):
        return float("nan")
    return out if np.isfinite(out) else float("nan")


def _numeric_series(frame: pd.DataFrame, column: str, *, default: float) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(default, index=frame.index, dtype=float)
    return pd.to_numeric(frame[column], errors="coerce").fillna(default)


def _as_frame(rows: pd.DataFrame | Iterable[dict[str, Any]]) -> pd.DataFrame:
    return rows.copy() if isinstance(rows, pd.DataFrame) else pd.DataFrame(list(rows))
