# Architecture

The framework separates a prediction contest into five layers.

## 1. Scoring Rules

Scoring rules turn a pick and a real outcome into points.

For football exact-score contests, the default scoring helper supports:

- exact score
- correct result
- correct goal difference
- winner-goals bonus
- outsider or draw bonus
- multiplier picks

The scoring module is intentionally independent from any specific tournament.

## 2. Truth Probabilities

Truth probabilities describe what is likely to happen.

They can come from:

- betting odds
- model outputs
- manual probabilities
- blended sources

The public helper `build_probability_table` normalizes odds or raw probabilities within each event.

## 3. Field Probabilities

Field probabilities describe what other participants are likely to pick.

This is separate from truth. A pick can be:

- likely and popular
- likely but ignored
- unlikely but over-picked
- unlikely and unpopular

The field model estimates crowd behavior from truth probability plus optional popularity hints.

## 4. Leaderboard Simulation

The simulator samples:

1. what happens in each event
2. what opponents pick
3. how many points everyone scores
4. where each strategy lands on the leaderboard

The output is strategy-level.

## 5. Strategy Ranking

Strategies are ranked by contest outcomes:

- average points
- average rank
- probability of finishing first
- probability of finishing in the top 10 percent

The best contest pick depends on probability, ownership, scoring, and payout.
