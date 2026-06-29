from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from prediction_framework import (  # noqa: E402
    apply_expert_signals,
    build_risk_capped_portfolio,
    build_source_probability_table,
    estimate_field_distribution,
    run_betting_tournament_strategy,
)
from prediction_framework.diagnostics import add_value_diagnostics  # noqa: E402


def main() -> int:
    market_rows = pd.DataFrame(
        [
            option("match_1", "Team A vs Team B", "a_1_0", "Team A 1-0", "bookmaker", 6.5, None, "high", True, 1.30, 6),
            option("match_1", "Team A vs Team B", "a_2_0", "Team A 2-0", "bookmaker", 7.0, None, "high", True, 1.50, 6),
            option("match_1", "Team A vs Team B", "draw_1_1", "Draw 1-1", "bookmaker", 7.5, None, "high", True, 1.10, 6),
            option("match_1", "Team A vs Team B", "b_1_0", "Team B 1-0", "bookmaker", 11.0, None, "high", True, 0.70, 9),
            option("match_1", "Team A vs Team B", "draw_1_1", "Draw 1-1", "prediction_market", None, 0.24, "medium", False, 1.10, 6),
            option("match_2", "Team C vs Team D", "c_2_0", "Team C 2-0", "bookmaker", 6.0, None, "high", True, 1.60, 6),
            option("match_2", "Team C vs Team D", "c_2_1", "Team C 2-1", "bookmaker", 8.0, None, "high", True, 1.25, 6),
            option("match_2", "Team C vs Team D", "draw_1_1", "Draw 1-1", "bookmaker", 8.5, None, "high", True, 0.95, 6),
            option("match_2", "Team C vs Team D", "d_1_0", "Team D 1-0", "bookmaker", 13.0, None, "high", True, 0.55, 10),
            option("match_2", "Team C vs Team D", "d_1_0", "Team D 1-0", "prediction_market", None, 0.18, "medium", False, 0.55, 10),
            option("match_3", "Team E vs Team F", "e_1_0", "Team E 1-0", "bookmaker", 6.8, None, "high", True, 1.35, 6),
            option("match_3", "Team E vs Team F", "e_2_1", "Team E 2-1", "bookmaker", 8.2, None, "high", True, 1.20, 6),
            option("match_3", "Team E vs Team F", "draw_0_0", "Draw 0-0", "bookmaker", 9.5, None, "high", True, 0.80, 6),
            option("match_3", "Team E vs Team F", "f_1_0", "Team F 1-0", "bookmaker", 12.5, None, "high", True, 0.65, 9),
            option("match_3", "Team E vs Team F", "draw_0_0", "Draw 0-0", "prediction_market", None, 0.20, "medium", False, 0.80, 6),
        ]
    )
    probabilities = build_source_probability_table(market_rows)
    expert_signals = pd.DataFrame(
        [
            {
                "event_id": "match_3",
                "source_name": "reviewed_preview",
                "source_url": "local://example",
                "published_at": "2026-01-01",
                "signal_target": "draw",
                "signal_direction": "up",
                "confidence": "medium",
                "note": "Example low-tempo signal.",
            }
        ]
    )
    adjusted = apply_expert_signals(probabilities, expert_signals, max_combined_multiplier=1.10)
    field = estimate_field_distribution(adjusted)
    diagnostics = add_value_diagnostics(field)
    result = run_betting_tournament_strategy(
        diagnostics,
        strategies=[
            "market_favorite",
            "max_expected_points",
            "contrarian",
            "anti_crowd",
            "field_leverage",
            "expert_aligned",
            "risk_capped",
            "top1_attack",
            "paid_places",
        ],
        n_sims=2000,
        n_opponents=100,
        paid_places=10,
        seed=7,
    )
    risk_portfolio = build_risk_capped_portfolio(diagnostics, min_probability=0.06, strategy_name="risk_capped")

    print("\nRanked strategies")
    print(result.strategy_summary.to_string(index=False))
    print("\nRecommended portfolio")
    print(result.recommended_portfolio.to_string(index=False))
    print("\nRisk-capped portfolio")
    print(risk_portfolio[["event_id", "option_id", "selection_reason"]].to_string(index=False))
    print("\nRank distribution sample")
    print(result.rank_distributions.head(12).to_string(index=False))
    print("\nTop options by contrarian value")
    columns = ["event_id", "label", "truth_probability", "field_probability", "contrarian_value", "source_count"]
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
    source: str,
    decimal_odds: float,
    source_probability: float | None,
    source_quality: str,
    is_direct_market: bool,
    popularity_hint: float,
    points_if_hit: int,
) -> dict[str, object]:
    return {
        "event_id": event_id,
        "event_name": event_name,
        "option_id": option_id,
        "label": label,
        "source": source,
        "decimal_odds": decimal_odds,
        "source_probability": source_probability,
        "source_quality": source_quality,
        "is_direct_market": is_direct_market,
        "popularity_hint": popularity_hint,
        "points_if_hit": points_if_hit,
    }


if __name__ == "__main__":
    raise SystemExit(main())
