from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from prediction_framework import (  # noqa: E402
    build_probability_table,
    estimate_field_distribution,
    rank_strategies,
)
from prediction_framework.diagnostics import add_value_diagnostics  # noqa: E402


def main() -> int:
    options = pd.DataFrame(
        [
            option("match_1", "Team A vs Team B", "a_1_0", "Team A 1-0", 6.5, 1.30, 6),
            option("match_1", "Team A vs Team B", "a_2_0", "Team A 2-0", 7.0, 1.50, 6),
            option("match_1", "Team A vs Team B", "draw_1_1", "Draw 1-1", 7.5, 1.10, 6),
            option("match_1", "Team A vs Team B", "b_1_0", "Team B 1-0", 11.0, 0.70, 9),
            option("match_2", "Team C vs Team D", "c_2_0", "Team C 2-0", 6.0, 1.60, 6),
            option("match_2", "Team C vs Team D", "c_2_1", "Team C 2-1", 8.0, 1.25, 6),
            option("match_2", "Team C vs Team D", "draw_1_1", "Draw 1-1", 8.5, 0.95, 6),
            option("match_2", "Team C vs Team D", "d_1_0", "Team D 1-0", 13.0, 0.55, 10),
            option("match_3", "Team E vs Team F", "e_1_0", "Team E 1-0", 6.8, 1.35, 6),
            option("match_3", "Team E vs Team F", "e_2_1", "Team E 2-1", 8.2, 1.20, 6),
            option("match_3", "Team E vs Team F", "draw_0_0", "Draw 0-0", 9.5, 0.80, 6),
            option("match_3", "Team E vs Team F", "f_1_0", "Team F 1-0", 12.5, 0.65, 9),
        ]
    )
    probabilities = build_probability_table(options, odds_col="decimal_odds")
    field = estimate_field_distribution(probabilities)
    diagnostics = add_value_diagnostics(field)
    summary = rank_strategies(diagnostics, n_sims=2000, n_opponents=100, seed=7)

    print("\nRanked strategies")
    print(summary.to_string(index=False))
    print("\nTop options by contrarian value")
    columns = ["event_id", "label", "truth_probability", "field_probability", "contrarian_value"]
    print(
        diagnostics.sort_values("contrarian_value", ascending=False)[columns]
        .head(6)
        .to_string(index=False)
    )
    return 0


def option(
    event_id: str,
    event_name: str,
    option_id: str,
    label: str,
    decimal_odds: float,
    popularity_hint: float,
    points_if_hit: int,
) -> dict[str, object]:
    return {
        "event_id": event_id,
        "event_name": event_name,
        "option_id": option_id,
        "label": label,
        "decimal_odds": decimal_odds,
        "popularity_hint": popularity_hint,
        "points_if_hit": points_if_hit,
    }


if __name__ == "__main__":
    raise SystemExit(main())
