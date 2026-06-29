# Skill 06: Simulate Tournament

## Use When

You need to compare strategies by leaderboard outcome.

## Code To Use

- `simulate_leaderboard(...)` for full simulation output
- `rank_strategies(...)` for summary only
- `run_betting_tournament_strategy(...)` for the public end-to-end workflow
- `fit_backward_value_model(...)` when the tournament is live and state matters

## Required Inputs

- options with `truth_probability`, `field_probability`, and points
- candidate portfolios or strategy families
- number of opponents, paid places, simulations, and seed

## Method

1. Load truth probabilities.
2. Load field probabilities.
3. Load scoring and points.
4. Define candidate portfolios.
5. Set objective:
   - `paid_places` for top-X payout
   - `top_1` for winner upside
   - balanced if both matter
6. Use enough simulations with a fixed seed.
7. Compare truth and field scenarios.
8. Rank by paid-place probability first when payout has top X, then top-1 upside and risk.

## Output

- `p_paid`
- `p_top_1`
- `p_top_10pct`
- `mean_rank`
- `mean_points`
- scenario comparison

## Stop If

- paid places do not match the payout table
- candidate picks omit required events
- known live results are not locked before adaptive simulation

## Checks

- seed is recorded
- paid places match payout
- candidate picks cover every event
- known results are locked in adaptive mode
