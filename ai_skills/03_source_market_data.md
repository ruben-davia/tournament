# Skill 03: Source Market Data

## Use When

You need probabilities for matches or tournament questions.

## Method

1. For each contest option, find the most direct market.
2. Use bookmaker odds, for example Winamax, for exact scores, 1X2, totals, BTTS, team totals, and player props.
3. Use prediction markets, for example Polymarket, for outrights and long-range tournament questions.
4. Convert decimal odds to implied probability: `1 / odds`.
5. Normalize within the same market to remove overround.
6. Label each source: `direct`, `proxy`, or `definition_check_required`.
7. Compare sources when both exist.
8. Treat disagreement as uncertainty, not as automatic value.

## Code To Use

- `build_source_probability_table(...)`
- `compare_source_probabilities(...)`
- `build_probability_table(...)` for simple single-source inputs

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
