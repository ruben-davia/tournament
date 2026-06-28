from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ColumnSpec:
    """Column names used by the generic probability/field/simulation pipeline."""

    event_id: str = "event_id"
    option_id: str = "option_id"
    label: str = "label"
    truth_probability: str = "truth_probability"
    field_probability: str = "field_probability"
    points_if_hit: str = "points_if_hit"


@dataclass(frozen=True)
class StrategySummary:
    strategy: str
    mean_points: float
    mean_rank: float
    p_top_1: float
    p_top_10pct: float

