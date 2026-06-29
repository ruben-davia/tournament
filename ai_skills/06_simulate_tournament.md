# Skill 06: Simulate Tournament

## Use When

You need to compare strategies by leaderboard outcome.

## Method

1. Load truth probabilities.
2. Load field probabilities.
3. Load scoring and points.
4. Define candidate portfolios.
5. Set objective:
   - `paid_places` for top-X payout
   - `top_1` for winner upside
   - balanced if both matter
6. Run enough simulations with a fixed seed.
7. Re-run across truth and field scenarios.
8. Rank by paid-place probability first when payout has top X, then top-1 upside and risk.

## Code To Use

- `simulate_leaderboard(..., paid_places=X)`
- `rank_strategies(...)`
- `rank_risk_frontier(...)`

## Output Metrics

- `p_paid`
- `p_top_1`
- `p_top_10pct`
- `mean_rank`
- `mean_points`
- scenario comparison

## Checks

- seed is recorded
- paid places match payout
- candidate picks cover every event
- known results are locked in adaptive mode
