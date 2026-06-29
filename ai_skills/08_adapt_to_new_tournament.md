# Skill 08: Adapt To New Tournament

## Use When

Someone wants to reuse the framework for another contest.

## Code To Use

Use the full pipeline:

- `build_probability_table(...)` or `build_source_probability_table(...)`
- `estimate_field_distribution(...)`
- `simulate_leaderboard(...)` or `run_betting_tournament_strategy(...)`
- `build_risk_capped_portfolio(...)` when risk control matters

## Required Inputs

- contest rules
- scoring and payout objective
- option table
- truth probabilities or market inputs
- field model assumptions

## Method

1. Use Skill 01 to map rules and payout.
2. Use Skill 02 to encode scoring.
3. Use Skill 03 to build truth inputs.
4. Use Skill 04 for uncertain or high-leverage events.
5. Use Skill 05 to estimate field behavior.
6. Use Skill 06 to simulate leaderboard.
7. Use Skill 07 to choose a portfolio.
8. Document what is direct data, proxy data, model assumption, and private/local data.

## Minimal Public Example

Keep examples anonymous:

- `Team A`, `Team B`
- fake odds
- fake field hints
- no raw CSV scrape
- no private names

## Output

- runnable example
- data contract
- README note explaining objective
- tests proving scoring, probability normalization, field normalization, and reproducible simulation

## Stop If

- private data would need to be committed
- tournament-specific names leak into generic framework code
- no public example can run without external data
