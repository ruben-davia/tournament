# Prediction Tournament Strategy Framework

Choose picks for a prediction tournament.

The goal is not only to be right. The goal is to finish where the payout matters.

| What we model | Why it matters |
| --- | --- |
| Tournament rules | Points, bonuses, multipliers, paid places |
| Outcome probabilities | What can happen |
| Other players | What the field is likely to pick |
| Monte Carlo runs | How often each strategy reaches each rank |
| Risk | Avoid strategies that win rarely but fail too often |

## Monte Carlo Tournament Run

After running the simulations, the framework evaluates an optimized strategy across tournament rounds.

| Step | Meaning |
| --- | --- |
| Sample outcomes | One possible future tournament |
| Score portfolios | Your picks and opponent picks |
| Rank leaderboard | Your simulated finish |
| Repeat many times | Distribution of possible ranks |

More mass on the left means a better chance of finishing near the top.

![Rank distribution through tournament rounds](docs/assets/readme-rank-distribution-tournament-rounds.gif)

## Pipeline

| Step | Purpose | Output |
| --- | --- | --- |
| Tournament | Define questions, scoring, payouts | Contest config |
| Probabilities | Estimate what can happen | Truth model |
| Field | Estimate what others pick | Opponent model |
| Expert signals | Add reviewed football context | Adjusted assumptions |
| Monte Carlo | Simulate futures and ranks | Rank distributions |
| Backward logic | Revalue choices during live rounds | Adaptive strategy |
| Objective | Match strategy to payout | Final portfolio |

## Modeling Other Players

The field model estimates what the rest of the leaderboard is likely to do.

| Signal | Use |
| --- | --- |
| Popular picks | Detect crowded outcomes |
| Market favorites | Estimate default behavior |
| Common scores | Model repeated score patterns |
| Expert narratives | Catch public bias or real information |
| Current standings | Adapt when the contest is live |

## Choosing A Strategy

The best strategy depends on the payout.

| Objective | Strategy shape |
| --- | --- |
| Paid places | More stable rank distribution |
| Top 1 | More upside and more variance |
| Top X | Balance ceiling and survival |
| Risk control | Avoid fragile portfolios |

![Final rank distribution by strategy](docs/assets/readme-final-rank-distribution-by-strategy.png)

## Stress Testing

A portfolio should survive bad assumptions.

| Scenario | What it checks |
| --- | --- |
| Base | Normal model run |
| Crowd chalk | Field overplays favorites |
| Noisy inputs | Probabilities are less reliable |
| Field learns | Opponents become sharper |
| Sharp field | Harder leaderboard |

![Final rank distribution by scenario](docs/assets/readme-final-rank-distribution-by-scenario.png)

## Quickstart

Run the public example:

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

## AI Skillset

This repo is meant to be used by an AI agent with a human bettor.

| Agent does | Human decides |
| --- | --- |
| Structures the tournament | Final assumptions |
| Sources market data | Data quality |
| Collects expert signals | Signal trust |
| Builds field model | Risk appetite |
| Runs simulations | Final strategy |

Start with [ai_skills/README.md](ai_skills/README.md).

## Install / Tests

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m unittest tests.test_framework tests.test_scoring
```
