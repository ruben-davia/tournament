"""Reusable tools for football prediction contests."""

from prediction_framework.backward import BackwardValueModel, fit_backward_value_model
from prediction_framework.diagnostics import add_value_diagnostics
from prediction_framework.field_model import estimate_field_distribution
from prediction_framework.expert_signals import apply_expert_signals, audit_expert_signals
from prediction_framework.probabilities import build_probability_table
from prediction_framework.risk import add_pick_risk_flags, build_risk_capped_portfolio, rank_risk_frontier
from prediction_framework.scoring import (
    MatchContext,
    OutsiderBonus,
    ScoreBreakdown,
    outsider_bonus_from_odds,
    score_prediction,
)
from prediction_framework.simulation import LeaderboardSimulation, simulate_leaderboard
from prediction_framework.sources import build_source_probability_table, compare_source_probabilities
from prediction_framework.strategy import rank_strategies
from prediction_framework.tournament import (
    BettingTournamentResult,
    build_strategy_portfolios,
    field_behavior_weights,
    run_betting_tournament_strategy,
)

__all__ = [
    "BettingTournamentResult",
    "BackwardValueModel",
    "LeaderboardSimulation",
    "MatchContext",
    "OutsiderBonus",
    "ScoreBreakdown",
    "add_value_diagnostics",
    "add_pick_risk_flags",
    "apply_expert_signals",
    "audit_expert_signals",
    "build_probability_table",
    "build_risk_capped_portfolio",
    "build_source_probability_table",
    "build_strategy_portfolios",
    "compare_source_probabilities",
    "estimate_field_distribution",
    "field_behavior_weights",
    "fit_backward_value_model",
    "outsider_bonus_from_odds",
    "rank_risk_frontier",
    "rank_strategies",
    "run_betting_tournament_strategy",
    "score_prediction",
    "simulate_leaderboard",
]
