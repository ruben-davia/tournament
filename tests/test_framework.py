import subprocess
import sys
import unittest

import pandas as pd

from prediction_framework import (
    apply_expert_signals,
    build_probability_table,
    build_risk_capped_portfolio,
    build_source_probability_table,
    estimate_field_distribution,
    fit_backward_value_model,
    run_betting_tournament_strategy,
    rank_strategies,
    simulate_leaderboard,
)


class FrameworkPipelineTest(unittest.TestCase):
    def sample_options(self):
        return pd.DataFrame(
            [
                {"event_id": "m1", "option_id": "a", "decimal_odds": 2.0, "popularity_hint": 1.5, "points_if_hit": 6},
                {"event_id": "m1", "option_id": "b", "decimal_odds": 4.0, "popularity_hint": 0.7, "points_if_hit": 9},
                {"event_id": "m2", "option_id": "a", "decimal_odds": 3.0, "popularity_hint": 1.0, "points_if_hit": 6},
                {"event_id": "m2", "option_id": "b", "decimal_odds": 3.0, "popularity_hint": 1.0, "points_if_hit": 6},
            ]
        )

    def test_probability_table_normalizes_by_event(self):
        probabilities = build_probability_table(self.sample_options())

        sums = probabilities.groupby("event_id")["truth_probability"].sum()
        self.assertTrue(((sums - 1.0).abs() < 1e-12).all())

    def test_field_distribution_normalizes_by_event(self):
        probabilities = build_probability_table(self.sample_options())
        field = estimate_field_distribution(probabilities)

        sums = field.groupby("event_id")["field_probability"].sum()
        self.assertTrue(((sums - 1.0).abs() < 1e-12).all())

    def test_simulation_is_reproducible(self):
        field = estimate_field_distribution(build_probability_table(self.sample_options()))

        sim_a = simulate_leaderboard(field, n_sims=250, n_opponents=20, seed=11)
        sim_b = simulate_leaderboard(field, n_sims=250, n_opponents=20, seed=11)
        a = sim_a.summary
        b = sim_b.summary

        pd.testing.assert_frame_equal(a, b)
        self.assertFalse(sim_a.rank_distribution.empty)

    def test_rank_strategies_returns_ranked_summary(self):
        field = estimate_field_distribution(build_probability_table(self.sample_options()))
        summary = rank_strategies(field, n_sims=100, n_opponents=10, seed=5)

        self.assertFalse(summary.empty)
        self.assertIn("strategy", summary.columns)
        self.assertIn("p_top_1", summary.columns)
        self.assertIn("p_paid", summary.columns)

    def test_source_probability_table_blends_and_normalizes(self):
        rows = pd.DataFrame(
            [
                {"event_id": "m1", "option_id": "home", "source": "winamax", "decimal_odds": 2.0, "source_quality": "high", "is_direct_market": True},
                {"event_id": "m1", "option_id": "draw", "source": "winamax", "decimal_odds": 4.0, "source_quality": "high", "is_direct_market": True},
                {"event_id": "m1", "option_id": "home", "source": "polymarket", "source_probability": 0.55, "source_quality": "medium", "is_direct_market": True},
                {"event_id": "m1", "option_id": "draw", "source": "polymarket", "source_probability": 0.45, "source_quality": "medium", "is_direct_market": True},
            ]
        )

        table = build_source_probability_table(rows)

        self.assertAlmostEqual(float(table["truth_probability"].sum()), 1.0)
        self.assertEqual(set(table["option_id"]), {"home", "draw"})
        self.assertTrue((table["source_count"] == 2).all())

    def test_expert_signals_adjust_probabilities_with_cap(self):
        options = pd.DataFrame(
            [
                {"event_id": "m1", "option_id": "home", "label": "Home win", "truth_probability": 0.5},
                {"event_id": "m1", "option_id": "draw", "label": "Draw", "truth_probability": 0.5},
            ]
        )
        signals = pd.DataFrame(
            [
                {"event_id": "m1", "signal_target": "draw", "signal_direction": "up", "confidence": "high", "source_url": "local"},
            ]
        )

        adjusted = apply_expert_signals(options, signals, max_combined_multiplier=1.12)

        self.assertAlmostEqual(float(adjusted["truth_probability"].sum()), 1.0)
        draw_p = float(adjusted.loc[adjusted["option_id"].eq("draw"), "truth_probability"].iloc[0])
        self.assertGreater(draw_p, 0.5)

    def test_risk_capped_portfolio_avoids_low_probability_pick(self):
        options = pd.DataFrame(
            [
                {"event_id": "m1", "option_id": "safe", "truth_probability": 0.22, "field_probability": 0.30, "points_if_hit": 6},
                {"event_id": "m1", "option_id": "thin", "truth_probability": 0.03, "field_probability": 0.01, "points_if_hit": 15},
            ]
        )

        portfolio = build_risk_capped_portfolio(options, min_probability=0.06)

        self.assertEqual(portfolio.iloc[0]["option_id"], "safe")
        self.assertIn("selection_reason", portfolio.columns)

    def test_high_level_tournament_strategy_returns_recommendation(self):
        field = estimate_field_distribution(build_probability_table(self.sample_options()))

        result = run_betting_tournament_strategy(
            field,
            strategies=["market_favorite", "contrarian", "risk_capped"],
            n_sims=200,
            n_opponents=20,
            paid_places=3,
            seed=21,
        )

        self.assertFalse(result.strategy_summary.empty)
        self.assertFalse(result.rank_distributions.empty)
        self.assertFalse(result.recommended_portfolio.empty)
        self.assertIn("p_paid", result.strategy_summary.columns)

    def test_backward_value_model_fits_continuation_values(self):
        rollouts = pd.DataFrame(
            [
                {"checkpoint": 2, "current_rank": 10, "points_gap": 4, "doublettes_left": 2, "terminal_value": 1.0},
                {"checkpoint": 2, "current_rank": 30, "points_gap": -8, "doublettes_left": 1, "terminal_value": 0.0},
                {"checkpoint": 3, "current_rank": 8, "points_gap": 6, "doublettes_left": 1, "terminal_value": 1.0},
                {"checkpoint": 3, "current_rank": 42, "points_gap": -12, "doublettes_left": 0, "terminal_value": 0.0},
            ]
        )

        model = fit_backward_value_model(rollouts)

        self.assertFalse(model.coefficients.empty)
        self.assertIn("continuation_value", model.fitted_values.columns)
        self.assertEqual(model.metadata["method"], "least_squares_backward_monte_carlo")

    def test_example_runs_without_private_data(self):
        result = subprocess.run(
            [sys.executable, "examples/basic_football_pool/run_example.py"],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn("Ranked strategies", result.stdout)


if __name__ == "__main__":
    unittest.main()
