# Prediction Tournament Strategy Framework

This repo helps choose picks in a prediction tournament where the goal is not only to be right, but to beat the leaderboard. It models the contest rules, the probability of each outcome, how other players are likely to pick, and the payout structure. Then it runs Monte Carlo simulations to compare portfolios and avoid strategies that win rarely but fail too often.

In practice, you use it to answer:

> Given this tournament and this payout table, which strategy gives me the best chance to finish where it matters?

## Tournament Simulation

The framework simulates the tournament many times. In each simulation it samples outcomes, scores your portfolio, scores simulated opponents, ranks the leaderboard, and records where you finish.

The GIF below shows the same rank distribution replayed through tournament rounds. More probability mass on the left means a better chance of finishing near the top.

![Rank distribution through tournament rounds](docs/assets/readme-rank-distribution-tournament-rounds.gif)

Regenerate the README charts with:

```bash
python scripts/generate_readme_charts.py
```

## Pipeline

1. **Define the tournament**: questions, matches, scoring, bonuses, multipliers, paid places.
2. **Build probabilities**: market odds, prediction markets, model probabilities, manual assumptions.
3. **Model the field**: estimate what other players will pick, including popular picks and anti-crowd opportunities.
4. **Add expert signals**: injuries, lineups, tactical notes, and other reviewed information.
5. **Run Monte Carlo**: simulate outcomes, opponents, scores, ranks, and payouts.
6. **Use backward logic when live**: lock known results, simulate remaining rounds, and value decisions from future leaderboard states.
7. **Choose by objective**: paid places, top 1, top X, expected payout, or risk-controlled survival.

## Example Output

A recommendation is judged by its rank distribution, not only by expected points.

![Recommended portfolio final rank distribution](docs/assets/readme-final-rank-distribution-recommended.png)

Different objectives produce different portfolios. A top-1 strategy can be too fragile for a paid-place payout. A safer portfolio can be better when the payout rewards top X.

![Final rank distribution by strategy](docs/assets/readme-final-rank-distribution-by-strategy.png)

The same portfolio should also be tested under different assumptions about the truth model and the field. This is where model risk becomes visible.

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

## What You Bring

You provide normalized inputs. The repo does not include private scrapes, player names, raw market snapshots, or tournament-specific runs.

Useful inputs:

- contest rules and payout structure
- option-level probabilities
- estimated field popularity
- expert or qualitative signals
- current standings for live contests

## Repo Layout

| Path | Purpose |
| --- | --- |
| `prediction_framework/` | reusable Python framework |
| `examples/basic_football_pool/` | small runnable example |
| `scripts/` | pipeline commands and README chart generation |
| `docs/` | method notes, data contracts, adaptation guides |
| `ai_skills/` | operational playbooks for AI agents |
| `apps/` | lightweight Streamlit dashboards |
| `tests/` | public tests |

## Key Modules

| Need | Public code |
| --- | --- |
| Build probabilities | `build_probability_table`, `build_source_probability_table` |
| Compare sources | `compare_source_probabilities` |
| Apply expert signals | `audit_expert_signals`, `apply_expert_signals` |
| Estimate the field | `estimate_field_distribution`, `field_behavior_weights` |
| Generate portfolios | `build_strategy_portfolios` |
| Simulate leaderboard | `simulate_leaderboard` |
| Rank strategies | `run_betting_tournament_strategy`, `rank_risk_frontier` |
| Risk control | `add_pick_risk_flags`, `build_risk_capped_portfolio` |
| Live/backward value | `fit_backward_value_model` |

## AI Agent Use

Use [ai_skills/README.md](ai_skills/README.md) when an AI agent is guiding a bettor through the process:

- understand the tournament
- source market data
- collect expert signals
- model the field
- run simulations
- build risk-capped portfolios
- adapt the method to another contest

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

For README chart generation:

```bash
pip install -e ".[docs]"
```

## Tests

```bash
python -m unittest tests.test_framework tests.test_scoring
```
