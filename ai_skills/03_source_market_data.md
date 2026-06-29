# Skill 03: Source Market Data

## Use When

You need probabilities for matches or tournament questions.

## Code To Use

- `build_probability_table(...)` for one clean source
- `build_source_probability_table(...)` for multiple sources
- `compare_source_probabilities(...)` for source disagreement

## Required Inputs

- one row per event option
- `event_id`
- `option_id`
- source odds or source probabilities
- source quality and direct/proxy label when multiple sources exist

## Method

1. For each contest option, find the most direct market.
2. Use bookmaker odds, for example Winamax, for exact scores, 1X2, totals, BTTS, team totals, and player props.
3. Use prediction markets, for example Polymarket, for outrights and long-range tournament questions.
4. Convert decimal odds to implied probability: `1 / odds`.
5. Normalize within the same market to remove overround.
6. Label each source: `direct`, `proxy`, or `definition_check_required`.
7. Compare sources when both exist.
8. Treat disagreement as uncertainty, not as automatic value.

## Required Columns

- `event_id`
- `option_id`
- `source`
- `decimal_odds` or `source_probability`
- `source_quality`
- `is_direct_market`

## Quality Checks

- same market definition?
- current timestamp?
- enough liquidity or reliable bookmaker line?
- no-vig probabilities sum to 1 by event?
- proxy labels preserved?

## Output

A clean table with `truth_probability`, source count, source list, and uncertainty notes.

## Stop If

- market definition does not match the contest option
- proxy mapping is undocumented
- probabilities cannot be normalized within event
