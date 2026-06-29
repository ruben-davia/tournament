from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class MatchContext:
    home: str
    away: str
    outsider_team: str | None = None
    bonus_outsider: int = 0
    bonus_draw: int = 0


@dataclass(frozen=True)
class ScoreBreakdown:
    base_points: int
    bonus_points: int
    total_before_multiplier: int
    total_points: int
    exact_score: bool
    correct_result: bool
    correct_goal_difference: bool
    correct_winner_goals: bool
    predicted_outcome: str
    actual_outcome: str
    bonus_reason: str | None = None
    multiplier: int = 1


@dataclass(frozen=True)
class OutsiderBonus:
    outsider_side: str | None
    bonus_outsider: int
    bonus_draw: int


def score_prediction(
    predicted_home: int,
    predicted_away: int,
    actual_home: int,
    actual_away: int,
    context: MatchContext,
    *,
    multiplier: int = 1,
) -> ScoreBreakdown:
    """Score one football exact-score prediction.

    Default rules:
    - exact score: 6 points
    - correct result plus correct goal difference: 4 points
    - correct result plus winner goals: 4 points
    - correct result only: 3 points
    - wrong result: 0 points
    """

    _validate_score(predicted_home, predicted_away, actual_home, actual_away)
    if multiplier < 1:
        raise ValueError(f"multiplier must be >= 1, got {multiplier}")

    predicted_outcome = _outcome(predicted_home, predicted_away)
    actual_outcome = _outcome(actual_home, actual_away)
    exact_score = predicted_home == actual_home and predicted_away == actual_away
    correct_result = predicted_outcome == actual_outcome
    correct_goal_difference = (
        correct_result
        and (predicted_home - predicted_away) == (actual_home - actual_away)
    )

    winner_side = actual_outcome if actual_outcome in {"home", "away"} else None
    if winner_side == "home":
        correct_winner_goals = predicted_home == actual_home
    elif winner_side == "away":
        correct_winner_goals = predicted_away == actual_away
    else:
        correct_winner_goals = False

    base_points = _base_points(
        exact_score=exact_score,
        correct_result=correct_result,
        correct_goal_difference=correct_goal_difference,
        correct_winner_goals=correct_winner_goals,
    )
    bonus_points, bonus_reason = _bonus_points(
        predicted_outcome=predicted_outcome,
        actual_outcome=actual_outcome,
        context=context,
    )
    total_before_multiplier = base_points + bonus_points
    total_points = total_before_multiplier * multiplier

    return ScoreBreakdown(
        base_points=base_points,
        bonus_points=bonus_points,
        total_before_multiplier=total_before_multiplier,
        total_points=total_points,
        exact_score=exact_score,
        correct_result=correct_result,
        correct_goal_difference=correct_goal_difference,
        correct_winner_goals=correct_winner_goals,
        predicted_outcome=predicted_outcome,
        actual_outcome=actual_outcome,
        bonus_reason=bonus_reason,
        multiplier=multiplier,
    )


def outsider_bonus_from_odds(home_odds: float, away_odds: float) -> OutsiderBonus:
    """Infer simple outsider and draw bonuses from home/away decimal odds.

    Use this helper when a football scoring rule gives extra points for calling
    the less likely team or a draw. Equal or invalid odds return no bonus.
    """

    if home_odds <= 0 or away_odds <= 0 or home_odds == away_odds:
        return OutsiderBonus(outsider_side=None, bonus_outsider=0, bonus_draw=0)

    if home_odds > away_odds:
        outsider_side = "home"
        outsider_odds = home_odds
    else:
        outsider_side = "away"
        outsider_odds = away_odds

    bonus_outsider = max(0, _round_half_up((outsider_odds - 1.5) * 2))
    bonus_draw = max(1, bonus_outsider // 2) if bonus_outsider > 0 else 0
    return OutsiderBonus(
        outsider_side=outsider_side,
        bonus_outsider=bonus_outsider,
        bonus_draw=bonus_draw,
    )


def _base_points(
    *,
    exact_score: bool,
    correct_result: bool,
    correct_goal_difference: bool,
    correct_winner_goals: bool,
) -> int:
    if exact_score:
        return 6
    if not correct_result:
        return 0
    if correct_goal_difference or correct_winner_goals:
        return 4
    return 3


def _bonus_points(
    *,
    predicted_outcome: str,
    actual_outcome: str,
    context: MatchContext,
) -> tuple[int, str | None]:
    if predicted_outcome != actual_outcome:
        return 0, None
    if actual_outcome == "draw" and context.bonus_draw > 0:
        return context.bonus_draw, "draw"
    outsider_side = _team_side(context.outsider_team, context)
    if outsider_side == actual_outcome and context.bonus_outsider > 0:
        return context.bonus_outsider, "outsider"
    return 0, None


def _team_side(team: str | None, context: MatchContext) -> str | None:
    if team is None:
        return None
    if team == context.home:
        return "home"
    if team == context.away:
        return "away"
    return None


def _outcome(home_goals: int, away_goals: int) -> str:
    if home_goals > away_goals:
        return "home"
    if away_goals > home_goals:
        return "away"
    return "draw"


def _validate_score(*scores: int) -> None:
    for score in scores:
        if not isinstance(score, int):
            raise TypeError(f"scores must be integers, got {score!r}")
        if score < 0:
            raise ValueError(f"scores must be non-negative, got {score}")


def _round_half_up(value: float) -> int:
    return math.floor(value + 0.5)
