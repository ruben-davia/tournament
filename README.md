# Prediction Tournament Strategy Framework

A reusable framework for choosing portfolios in prediction tournaments.

The examples are football-oriented. The method applies to any point-based prediction contest.

Use it to simulate a contest, model opponents, compare strategies, and choose the portfolio that fits the payout objective.

It is built for tournaments where:

- many players submit picks
- payouts depend on leaderboard rank
- the best decision depends on what other players are likely to do

It uses:

- scoring rules
- outcome probabilities
- opponent behavior
- expert signals
- payout structure

It produces:

- simulated tournaments
- rank distributions
- strategy comparisons
- stress tests
- risk-capped portfolios

Strategies can be ranked for paid places, top X, top 1, expected payout, or controlled risk.

## Monte Carlo Tournament Simulation

Monte Carlo creates many possible versions of the tournament. Each simulation samples outcomes, opponent picks, scores, ranks, and payout.

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

The field model is the part that asks: "What will everyone else do?"

It uses signals such as:

- popular picks
- market favorites
- common score patterns
- expert narratives
- current standings
- remaining risk appetite

A correct crowded pick can add little separation. A lower-owned pick can be valuable when its probability is still strong.

## Choosing A Strategy

Different payouts need different strategies.

- Paid places: prioritize survival and stable top-X probability.
- Top 1: accept more variance for more upside.
- Top X: balance ceiling and downside.
- Risk control: avoid fragile portfolios with narrow win paths.

![Final rank distribution by strategy](docs/assets/readme-final-rank-distribution-by-strategy.png)

## Stress Testing

Use multiple assumption sets.

The same strategy should be tested against different assumptions:

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
