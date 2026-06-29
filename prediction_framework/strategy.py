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
    """Use when you only need the ranked strategy summary table.

    This is a convenience wrapper around `simulate_leaderboard(...)`. Use
    `simulate_leaderboard(...)` directly when you also need picks, metadata, or
    rank-distribution rows.
    """

    return simulate_leaderboard(options, candidate_picks, **simulation_kwargs).summary
