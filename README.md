# Football Prediction Framework

Reusable Python framework for football prediction contests.

It helps answer a practical question:

> In a prediction pool, what should I pick if I care about beating the leaderboard, not only picking the most likely result?

The framework is built for two audiences:

- **Bettors and pool players** who want a structured way to compare picks.
- **Data people** who want reusable building blocks for probabilities, field modelling, simulations, and strategy ranking.

## What It Does

Most prediction contests have two separate problems:

1. **Truth**: what is likely to happen?
2. **Field behavior**: what are other people likely to pick?

The best contest pick is not always the most likely outcome. A less popular pick can be better if it still has enough probability and gives you more leaderboard upside.

This framework turns that idea into a simple pipeline:

```text
rules -> probabilities -> field model -> leaderboard simulation -> strategy ranking
```

## Quickstart

Run the included example with fake public data:

```bash
python examples/basic_football_pool/run_example.py
```

Expected output:

- ranked strategies such as `favorite`, `balanced`, and `contrarian`
- options with truth probability, estimated field probability, and contrarian value

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Minimal Python Usage

```python
import pandas as pd
from prediction_framework import build_probability_table, estimate_field_distribution, rank_strategies

options = pd.DataFrame([
    {"event_id": "match_1", "option_id": "home_1_0", "label": "Home 1-0", "decimal_odds": 6.5, "points_if_hit": 6},
    {"event_id": "match_1", "option_id": "draw_1_1", "label": "Draw 1-1", "decimal_odds": 7.5, "points_if_hit": 6},
    {"event_id": "match_1", "option_id": "away_1_0", "label": "Away 1-0", "decimal_odds": 11.0, "points_if_hit": 9},
])
probabilities = build_probability_table(options, odds_col="decimal_odds")
field = estimate_field_distribution(probabilities)
summary = rank_strategies(field, n_sims=5000, n_opponents=100, seed=42)

print(summary)
```

## Expected Input Shape

The quickest path is a CSV like this:

| column | meaning |
| --- | --- |
| `event_id` | Match or contest question id. |
| `option_id` | Stable id for a pick option. |
| `label` | Human-readable option name. |
| `decimal_odds` | Market-like decimal odds, used to build truth probabilities. |
| `popularity_hint` | Optional crowd/popularity signal. |
| `points_if_hit` | Points earned if the option is correct. |

See [docs/data-contracts.md](docs/data-contracts.md) for the full contract and [docs/market-inputs.md](docs/market-inputs.md) for probability inputs.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `prediction_framework/` | Generic reusable library. |
| `examples/basic_football_pool/` | Small runnable example with anonymous in-memory data. |
| `scripts/` | CLI pipeline commands. |
| `apps/` | Lightweight Streamlit dashboards. |
| `ai_skills/` | Agent playbooks that explain when to use each part of the framework. |
| `docs/` | Architecture, quickstart, data contracts, publishing notes. |
| `tests/` | Public unit and smoke tests. |

## CLI Pipeline

All public scripts accept `--config`, `--input-dir`, `--output-dir`, `--seed`, and `--n-sims`.

```bash
python scripts/build_probabilities.py --input-dir data/raw --output-dir data/work
python scripts/build_field_model.py --input-dir data/work --output-dir data/work
python scripts/run_strategy.py --input-dir data/work --output-dir data/out --n-sims 5000
```

## Dashboards

```bash
streamlit run apps/strategy_dashboard.py
streamlit run apps/market_dashboard.py
streamlit run apps/field_model_dashboard.py
```

## Adapting It To Another Tournament

Start with [docs/adapting-a-new-tournament.md](docs/adapting-a-new-tournament.md).

If you use an AI agent, start with [ai_skills/README.md](ai_skills/README.md). Those files are written as operating playbooks: when to use the skill, what inputs to ask for, what to produce, and common mistakes.
