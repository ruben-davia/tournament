# Skill 01: Understand Tournament

## Use When

You receive a new contest, rules PDF, website, or user explanation.

## Method

1. Identify contest type: match scores, special questions, bracket, player awards, or mixed.
2. List every decision the player must submit.
3. Find lock timing: all-at-once, matchday-by-matchday, or before each match.
4. Extract payout objective: winner-take-all, top X paid, points-only, or rank prize table.
5. Extract scoring: exact score, result, goal difference, outsider/draw bonus, multipliers, tie-breaks.
6. Mark unknowns. Ask or document assumptions before using them.

## Output

Produce:

- `contest_summary`
- `decision_calendar`
- `scoring_items`
- `payout_objective`
- `open_questions`

## Checks

- Can the simulator know when each pick is locked?
- Is top X defined from payout places?
- Are bonuses deterministic from input data?
- Are private/player-specific files excluded from public output?
