"""Reusable tools for football prediction contests."""

from prediction_framework.field_model import estimate_field_distribution
from prediction_framework.probabilities import build_probability_table
from prediction_framework.scoring import (
    MatchContext,
    OutsiderBonus,
    ScoreBreakdown,
    outsider_bonus_from_odds,
    score_prediction,
)
from prediction_framework.simulation import LeaderboardSimulation, simulate_leaderboard
from prediction_framework.strategy import rank_strategies

__all__ = [
    "LeaderboardSimulation",
    "MatchContext",
    "OutsiderBonus",
    "ScoreBreakdown",
    "build_probability_table",
    "estimate_field_distribution",
    "outsider_bonus_from_odds",
    "rank_strategies",
    "score_prediction",
    "simulate_leaderboard",
]

