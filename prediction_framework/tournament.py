from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from prediction_framework.risk import build_risk_capped_portfolio, rank_risk_frontier
from prediction_framework.simulation import simulate_leaderboard


DEFAULT_STRATEGIES = (
    "market_favorite",
    "max_expected_points",
    "safe_chalk",
    "contrarian",
    "anti_crowd",
    "field_leverage",
    "expert_aligned",
    "risk_capped",
    "top1_attack",
    "paid_places",
    "adaptive_current_rank",
)


@dataclass(frozen=True)
class BettingTournamentResult:
    strategy_summary: pd.DataFrame
    rank_distributions: pd.DataFrame
    recommended_portfolio: pd.DataFrame
    all_portfolios: pd.DataFrame
    metadata: dict[str, Any]


def run_betting_tournament_strategy(
    options: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    strategies: Iterable[str] = DEFAULT_STRATEGIES,
    event_col: str = "event_id",
    option_col: str = "option_id",
    truth_probability_col: str = "truth_probability",
    field_probability_col: str = "field_probability",
    points_col: str = "points_if_hit",
    expert_support_col: str = "expert_support",
    paid_places: int = 10,
    n_sims: int = 5000,
    n_opponents: int = 100,
    seed: int = 42,
) -> BettingTournamentResult:
    """Run the public end-to-end strategy comparison for a betting tournament.

    Inputs are already-normalized option rows. Use the lower-level source,
    expert-signal, and field-model modules before calling this function.
    """

    table = _as_frame(options).copy()
    _require(table, [event_col, option_col, truth_probability_col, field_probability_col])
    if points_col not in table.columns:
        table[points_col] = 1.0

    portfolios = build_strategy_portfolios(
        table,
        strategies=strategies,
        event_col=event_col,
        option_col=option_col,
        truth_probability_col=truth_probability_col,
        field_probability_col=field_probability_col,
        points_col=points_col,
        expert_support_col=expert_support_col,
    )
    simulation = simulate_leaderboard(
        table,
        portfolios,
        event_col=event_col,
        option_col=option_col,
        truth_probability_col=truth_probability_col,
        field_probability_col=field_probability_col,
        points_col=points_col,
        n_sims=n_sims,
        n_opponents=n_opponents,
        paid_places=paid_places,
        seed=seed,
    )
    summary = rank_risk_frontier(simulation.summary, tolerance=0.01)
    recommended_name = str(summary.iloc[0]["strategy"]) if not summary.empty else ""
    recommended = portfolios[portfolios["strategy"].astype(str).eq(recommended_name)].copy()
    return BettingTournamentResult(
        strategy_summary=summary,
        rank_distributions=simulation.rank_distribution,
        recommended_portfolio=recommended.reset_index(drop=True),
        all_portfolios=portfolios.reset_index(drop=True),
        metadata={
            **simulation.metadata,
            "strategy_families": list(strategies),
            "method": "Monte Carlo leaderboard comparison with paid-place, top-1, and risk-frontier ranking.",
        },
    )


def build_strategy_portfolios(
    options: pd.DataFrame | Iterable[dict[str, Any]],
    *,
    strategies: Iterable[str] = DEFAULT_STRATEGIES,
    event_col: str = "event_id",
    option_col: str = "option_id",
    truth_probability_col: str = "truth_probability",
    field_probability_col: str = "field_probability",
    points_col: str = "points_if_hit",
    expert_support_col: str = "expert_support",
) -> pd.DataFrame:
    """Generate one-pick-per-event portfolios for named strategy families."""

    table = _as_frame(options).copy()
    rows: list[dict[str, Any]] = []
    strategy_set = [str(strategy) for strategy in strategies]
    for strategy in strategy_set:
        if strategy == "risk_capped":
            risk_rows = build_risk_capped_portfolio(
                table,
                event_col=event_col,
                option_col=option_col,
                probability_col=truth_probability_col,
                field_col=field_probability_col,
                points_col=points_col,
                expert_support_col=expert_support_col,
                strategy_name=strategy,
            )
            rows.extend(risk_rows[["strategy", event_col, option_col]].to_dict("records"))
            continue
        for event, group in table.groupby(event_col, sort=False):
            pick = _pick_for_strategy(
                group.copy(),
                strategy=strategy,
                truth_probability_col=truth_probability_col,
                field_probability_col=field_probability_col,
                points_col=points_col,
                expert_support_col=expert_support_col,
            )
            rows.append({"strategy": strategy, event_col: event, option_col: pick[option_col]})
    return pd.DataFrame(rows)


def field_behavior_weights(profile: str = "trained_public_default") -> dict[str, float]:
    """Return generic opponent-behavior weights inspired by calibrated field work.

    The values are public, generic parameters. They describe how simulated
    opponents may overweight favorites, common scores, visible teams, and EV.
    They do not contain private player names or private observations.
    """

    profiles = {
        "safe_chalk": {"truth": 1.15, "field": 0.85, "ev": 0.35, "anti_crowd": -0.10, "expert": 0.10},
        "sharp_ev": {"truth": 0.80, "field": 0.20, "ev": 1.10, "anti_crowd": 0.15, "expert": 0.20},
        "contrarian": {"truth": 0.45, "field": -0.80, "ev": 0.45, "anti_crowd": 0.75, "expert": 0.05},
        "trained_public_default": {"truth": 0.90, "field": 0.55, "ev": 0.65, "anti_crowd": 0.20, "expert": 0.15},
    }
    if profile not in profiles:
        raise ValueError(f"Unknown field behavior profile: {profile}")
    return profiles[profile]


def _pick_for_strategy(
    group: pd.DataFrame,
    *,
    strategy: str,
    truth_probability_col: str,
    field_probability_col: str,
    points_col: str,
    expert_support_col: str,
) -> pd.Series:
    p = _numeric(group, truth_probability_col, default=0.0)
    field = _numeric(group, field_probability_col, default=0.0)
    points = _numeric(group, points_col, default=1.0)
    expert = _numeric(group, expert_support_col, default=0.0)
    ev = p * points
    leverage = p - field
    ratio = p / np.maximum(field, 1e-9)

    if strategy == "market_favorite":
        score = p
    elif strategy == "max_expected_points":
        score = ev
    elif strategy == "safe_chalk":
        score = 1.2 * p + 0.25 * field + 0.15 * ev
    elif strategy == "contrarian":
        score = 0.60 * p + 1.15 * leverage + 0.20 * np.sqrt(np.maximum(p, 0.0))
    elif strategy == "anti_crowd":
        score = ev - 0.75 * field
    elif strategy == "field_leverage":
        score = ratio + 0.20 * ev
    elif strategy == "expert_aligned":
        score = ev + 0.45 * expert
    elif strategy == "top1_attack":
        score = 0.75 * ev + 0.65 * leverage + 0.40 * np.sqrt(np.maximum(p, 0.0))
    elif strategy == "paid_places":
        score = 1.20 * ev + 0.30 * p - 0.20 * field
    elif strategy == "adaptive_current_rank":
        score = 0.95 * ev + 0.35 * leverage + 0.20 * expert
    else:
        raise ValueError(f"Unknown strategy family: {strategy}")
    idx = int(np.asarray(score, dtype=float).argmax())
    return group.iloc[idx]


def _numeric(frame: pd.DataFrame, column: str, *, default: float) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(default, index=frame.index, dtype=float)
    return pd.to_numeric(frame[column], errors="coerce").fillna(default)


def _as_frame(rows: pd.DataFrame | Iterable[dict[str, Any]]) -> pd.DataFrame:
    return rows.copy() if isinstance(rows, pd.DataFrame) else pd.DataFrame(list(rows))


def _require(table: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in table.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
