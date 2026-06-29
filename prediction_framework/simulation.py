from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Iterable
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class LeaderboardSimulation:
    summary: pd.DataFrame
    picks: pd.DataFrame
    rank_distribution: pd.DataFrame
    metadata: dict[str, Any]


def simulate_leaderboard(
    options: pd.DataFrame | Iterable[dict[str, Any]],
    candidate_picks: pd.DataFrame | Iterable[dict[str, Any]] | None = None,
    *,
    event_col: str = "event_id",
    option_col: str = "option_id",
    truth_probability_col: str = "truth_probability",
    field_probability_col: str = "field_probability",
    points_col: str = "points_if_hit",
    n_sims: int = 1000,
    n_opponents: int = 100,
    paid_places: int | None = None,
    seed: int = 42,
) -> LeaderboardSimulation:
    """Use when you need rank distributions for candidate portfolios.

    Required option columns are `event_id`, `option_id`, `truth_probability`,
    and `field_probability`; `points_if_hit` is optional and defaults to 1.
    Pass `candidate_picks` when you already have portfolios. Leave it empty to
    compare built-in favorite, contrarian, and balanced baselines.

    Returns a `LeaderboardSimulation` with strategy summary metrics, simulated
    picks, rank distribution buckets, and metadata including seed and paid
    places. This public simulator uses an option-hit abstraction: a pick earns
    `points_if_hit` when its option is sampled as the event truth.
    """

    table = options.copy() if isinstance(options, pd.DataFrame) else pd.DataFrame(list(options))
    required = [event_col, option_col, truth_probability_col, field_probability_col]
    missing = [column for column in required if column not in table.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if points_col not in table.columns:
        table[points_col] = 1.0

    table[points_col] = pd.to_numeric(table[points_col], errors="coerce").fillna(1.0)
    events = list(dict.fromkeys(table[event_col].astype(str).tolist()))
    rng = np.random.default_rng(seed)
    paid_cutoff = max(1, int(paid_places)) if paid_places is not None else max(1, int(np.ceil(n_opponents * 0.10)))

    event_options = {
        event: table[table[event_col].astype(str) == event].reset_index(drop=True)
        for event in events
    }
    actual_by_event = {
        event: _sample_options(frame, truth_probability_col, n_sims, rng)
        for event, frame in event_options.items()
    }
    opponent_scores = np.zeros((n_sims, n_opponents), dtype=float)
    for event, frame in event_options.items():
        actual_idx = actual_by_event[event]
        opponent_idx = _sample_options(frame, field_probability_col, n_sims * n_opponents, rng).reshape(n_sims, n_opponents)
        points = frame[points_col].to_numpy(float)
        opponent_scores += np.where(opponent_idx == actual_idx[:, None], points[opponent_idx], 0.0)

    picks = _candidate_picks(table, candidate_picks, event_col, option_col)
    summary_rows = []
    rank_rows = []
    for strategy, strategy_picks in picks.groupby("strategy", sort=False):
        our_scores = np.zeros(n_sims, dtype=float)
        for event, frame in event_options.items():
            pick_rows = strategy_picks[strategy_picks[event_col].astype(str) == event]
            if pick_rows.empty:
                continue
            picked_option = str(pick_rows.iloc[0][option_col])
            option_values = frame[option_col].astype(str).tolist()
            if picked_option not in option_values:
                continue
            picked_idx = option_values.index(picked_option)
            actual_idx = actual_by_event[event]
            points = float(frame.iloc[picked_idx][points_col])
            our_scores += np.where(actual_idx == picked_idx, points, 0.0)

        ranks = 1 + (opponent_scores > our_scores[:, None]).sum(axis=1)
        rank_rows.extend(_rank_distribution_rows(str(strategy), ranks))
        summary_rows.append(
            {
                "strategy": strategy,
                "mean_points": float(our_scores.mean()),
                "p50_points": float(np.quantile(our_scores, 0.50)),
                "p90_points": float(np.quantile(our_scores, 0.90)),
                "mean_rank": float(ranks.mean()),
                "p_top_1": float((ranks == 1).mean()),
                "p_paid": float((ranks <= paid_cutoff).mean()),
                "p_top_10pct": float((ranks <= max(1, int(np.ceil(n_opponents * 0.10)))).mean()),
            }
        )

    summary = pd.DataFrame(summary_rows).sort_values(
        ["p_paid", "p_top_1", "p_top_10pct", "mean_points"],
        ascending=[False, False, False, False],
    )
    return LeaderboardSimulation(
        summary=summary.reset_index(drop=True),
        picks=picks.reset_index(drop=True),
        rank_distribution=pd.DataFrame(rank_rows),
        metadata={"n_sims": n_sims, "n_opponents": n_opponents, "paid_places": paid_cutoff, "seed": seed, "events": events},
    )


def _candidate_picks(
    table: pd.DataFrame,
    candidate_picks: pd.DataFrame | Iterable[dict[str, Any]] | None,
    event_col: str,
    option_col: str,
) -> pd.DataFrame:
    if candidate_picks is not None:
        picks = candidate_picks.copy() if isinstance(candidate_picks, pd.DataFrame) else pd.DataFrame(list(candidate_picks))
        required = {"strategy", event_col, option_col}
        missing = sorted(required - set(picks.columns))
        if missing:
            raise ValueError(f"Candidate picks are missing columns: {missing}")
        return picks

    rows = []
    for event, frame in table.groupby(event_col, sort=False):
        favorite = frame.sort_values("truth_probability", ascending=False).iloc[0]
        edge = (frame["truth_probability"] - frame["field_probability"]).astype(float)
        contrarian = frame.iloc[int(edge.to_numpy().argmax())]
        balanced_score = frame["truth_probability"].astype(float) / np.maximum(frame["field_probability"].astype(float), 1e-12)
        balanced = frame.iloc[int(balanced_score.to_numpy().argmax())]
        rows.extend(
            [
                {"strategy": "favorite", event_col: event, option_col: favorite[option_col]},
                {"strategy": "contrarian", event_col: event, option_col: contrarian[option_col]},
                {"strategy": "balanced", event_col: event, option_col: balanced[option_col]},
            ]
        )
    return pd.DataFrame(rows)


def _sample_options(frame: pd.DataFrame, probability_col: str, size: int, rng: np.random.Generator) -> np.ndarray:
    probabilities = pd.to_numeric(frame[probability_col], errors="coerce").fillna(0.0).clip(lower=0.0).to_numpy(float)
    total = float(probabilities.sum())
    if total <= 0:
        probabilities = np.full(len(frame), 1.0 / max(len(frame), 1), dtype=float)
    else:
        probabilities = probabilities / total
    return rng.choice(len(frame), size=size, p=probabilities)


def _rank_distribution_rows(strategy: str, ranks: np.ndarray) -> list[dict[str, Any]]:
    buckets = [
        ("1", ranks == 1),
        ("2-5", (ranks >= 2) & (ranks <= 5)),
        ("6-10", (ranks >= 6) & (ranks <= 10)),
        ("11-25", (ranks >= 11) & (ranks <= 25)),
        ("26-50", (ranks >= 26) & (ranks <= 50)),
        ("51+", ranks >= 51),
    ]
    return [
        {"strategy": strategy, "rank_bucket": bucket, "probability": float(mask.mean())}
        for bucket, mask in buckets
        if bool(mask.any())
    ]
