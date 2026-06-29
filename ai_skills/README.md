# AI Skills

These skills are operating procedures for an AI agent using this repo.

Use the smallest skill that matches the task. Choose the full pipeline only when the whole workflow is needed.

## Skill Map

| Need | Skill | Main functions | Expected artifact |
| --- | --- | --- | --- |
| Understand a new contest | `01_understand_tournament.md` | none | contest summary, decision calendar, open questions |
| Turn rules into scoring inputs | `02_design_scoring_rules.md` | `score_prediction(...)`, `outsider_bonus_from_odds(...)` | scoring examples and tests |
| Find and normalize market data | `03_source_market_data.md` | `build_probability_table(...)`, `build_source_probability_table(...)`, `compare_source_probabilities(...)` | truth probability table |
| Collect injuries/lineups/expert signals | `04_collect_expert_signals.md` | `audit_expert_signals(...)`, `apply_expert_signals(...)` | reviewed signal table and adjusted probabilities |
| Estimate what others will pick | `05_model_the_field.md` | `estimate_field_distribution(...)`, `add_value_diagnostics(...)` | field probability table |
| Simulate contest and leaderboard | `06_simulate_tournament.md` | `simulate_leaderboard(...)`, `rank_strategies(...)` | strategy summary and rank distributions |
| Build risk-capped portfolios | `07_build_risk_capped_portfolio.md` | `add_pick_risk_flags(...)`, `build_risk_capped_portfolio(...)`, `rank_risk_frontier(...)` | selected portfolio with risk reasons |
| Adapt to another tournament | `08_adapt_to_new_tournament.md` | full pipeline | runnable example and data contract |

## Core Rule

Always keep these separate:

- **truth**: what is likely to happen
- **field**: what others are likely to pick
- **strategy**: what we should pick given payout, rank, and risk

## Agent Routing

When the user asks a concrete question, route to the narrowest skill:

- odds or probabilities -> Skill 03
- injuries, previews, or qualitative signals -> Skill 04
- opponent behavior or ownership -> Skill 05
- rank distributions or payout odds -> Skill 06
- downside control or final portfolio choice -> Skill 07
- live tournament state -> Skill 06 plus `fit_backward_value_model(...)`

For function-level routing, use [../docs/function-map.md](../docs/function-map.md).
