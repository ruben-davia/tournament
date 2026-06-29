# Prediction Tournament Strategy Framework

The goal is to win a prediction tournament, or finish where the payout matters. A tournament is defined by picks, scoring rules, opponents, and a gain function attached to final rank:

```math
s^* = \arg\max_{s \in S} \mathbb{E}[G(R_s)]
```

`s` is a portfolio, `R_s` is its simulated final rank, and `G(rank)` is the payout or utility of that rank.

The framework searches for this portfolio by combining scoring rules, outcome probabilities, field modeling, expert signals, Monte Carlo simulation, and backward strategy updates when the tournament is live.

The examples are football-oriented. The method applies to any point-based prediction contest where the objective is paid places, top X, top 1, expected payout, or controlled risk.

## Monte Carlo Tournament Simulation

Monte Carlo estimates the rank distribution of each portfolio. It creates many possible versions of the tournament and samples outcomes, opponent picks, scores, ranks, and payout.

Backward strategy updates the decision problem when the tournament is live: known results are locked, the current leaderboard is used, and remaining picks are valued from the new state.

The GIF is a simulated output for an optimized strategy. Each frame shows the rank probability mass after a tournament round. More mass on the left means a better chance to finish near the top.

![Rank distribution through tournament rounds](docs/assets/readme-rank-distribution-tournament-rounds.gif)

The simulation helps identify:

- which portfolio fits the payout
- where the strategy wins
- where it fails
- how sensitive it is to field assumptions

## Three Models

A prediction contest has three different models:

- **Truth**: what is likely to happen.
- **Field**: what other players are likely to pick.
- **Strategy**: what you should pick given payout and risk.

Tournament value comes from probability, ownership, scoring, and payout. A useful pick improves the full rank distribution against the field.

## Pipeline

1. Define the tournament: matches, questions, scoring, bonuses, paid places.
2. Build probabilities: market odds, model probabilities, manual assumptions.
3. Model the field: estimate popular, crowded, and under-owned picks.
4. Add expert signals: injuries, lineups, tactical notes, context.
5. Simulate the leaderboard: outcomes, opponents, scores, ranks, payouts.
6. Use backward logic when live: lock known results and value remaining choices.
7. Choose a strategy: match the portfolio to the payout objective.

## Modeling Other Players

The field model estimates what other players are likely to pick.

It uses signals such as:

- popular picks
- market favorites
- common score patterns
- expert narratives
- current standings
- remaining risk appetite

A correct crowded pick can add little separation. A lower-owned pick can be valuable when its probability is still strong.

## Choosing A Strategy

Strategy selection maps the payout objective to the right risk profile.

- Paid places: prioritize survival and stable top-X probability.
- Top 1: accept more variance for more upside.
- Top X: balance ceiling and downside.
- Risk control: avoid fragile portfolios with narrow win paths.

![Final rank distribution by strategy](docs/assets/readme-final-rank-distribution-by-strategy.png)

## Stress Testing

Stress testing checks whether the portfolio remains strong when assumptions move.

Compare scenarios where:

- the field is more chalky than expected
- input probabilities are noisy
- opponents become sharper
- expert signals conflict with markets
- the payout makes downside more expensive

![Final rank distribution by scenario](docs/assets/readme-final-rank-distribution-by-scenario.png)

## Quickstart

Public example command:

```bash
python examples/basic_football_pool/run_example.py
```

Minimal Python use:

```python
from prediction_framework import run_betting_tournament_strategy

result = run_betting_tournament_strategy(
    options,
    paid_places=10,
    n_sims=10000,
    n_opponents=125,
    seed=42,
)

print(result.strategy_summary)
print(result.recommended_portfolio)
```

`options` is one row per possible pick:

- `event_id`
- `option_id`
- `truth_probability`
- `field_probability`
- `points_if_hit`

Public examples use synthetic inputs. Bring your own market probabilities, expert signals, or field assumptions.

## AI Skillset

This repo is designed as code plus a working skillset for an AI agent and a human bettor.

The agent helps:

- understand the tournament
- source and normalize data
- collect expert signals
- model the field
- simulate tournaments
- build risk-capped portfolios
- adapt the method to another contest

The human keeps judgment on:

- assumptions
- data quality
- signal trust
- final risk appetite

Start with [ai_skills/README.md](ai_skills/README.md).

## Install / Tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m unittest tests.test_framework tests.test_scoring
```
