import subprocess
import sys
import unittest

import pandas as pd

from prediction_framework import (
    build_probability_table,
    estimate_field_distribution,
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

        a = simulate_leaderboard(field, n_sims=250, n_opponents=20, seed=11).summary
        b = simulate_leaderboard(field, n_sims=250, n_opponents=20, seed=11).summary

        pd.testing.assert_frame_equal(a, b)

    def test_rank_strategies_returns_ranked_summary(self):
        field = estimate_field_distribution(build_probability_table(self.sample_options()))
        summary = rank_strategies(field, n_sims=100, n_opponents=10, seed=5)

        self.assertFalse(summary.empty)
        self.assertIn("strategy", summary.columns)
        self.assertIn("p_top_1", summary.columns)

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
