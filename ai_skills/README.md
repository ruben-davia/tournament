# AI Skills

These skills are operating procedures for an AI agent using this repo.

Use the smallest skill that matches the task. Choose the full pipeline only when the whole workflow is needed.

## Skill Map

| Need | Skill |
| --- | --- |
| Understand a new contest | `01_understand_tournament.md` |
| Turn rules into scoring inputs | `02_design_scoring_rules.md` |
| Find and normalize market data | `03_source_market_data.md` |
| Collect injuries/lineups/expert signals | `04_collect_expert_signals.md` |
| Estimate what others will pick | `05_model_the_field.md` |
| Simulate contest and leaderboard | `06_simulate_tournament.md` |
| Build risk-capped portfolios | `07_build_risk_capped_portfolio.md` |
| Adapt to another tournament | `08_adapt_to_new_tournament.md` |

## Core Rule

Always keep these separate:

- **truth**: what is likely to happen
- **field**: what others are likely to pick
- **strategy**: what we should pick given payout, rank, and risk
