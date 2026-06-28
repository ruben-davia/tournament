from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import pandas as pd

from prediction_framework.simulation import simulate_leaderboard


def rank_strategies(
    options: pd.DataFrame | Iterable[dict[str, Any]],
    candidate_picks: pd.DataFrame | Iterable[dict[str, Any]] | None = None,
    **simulation_kwargs: Any,
) -> pd.DataFrame:
    """Return strategy summaries sorted by leaderboard upside."""

    return simulate_leaderboard(options, candidate_picks, **simulation_kwargs).summary

