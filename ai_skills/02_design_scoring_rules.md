# Skill 02: Design Scoring Rules

## Use When

Rules are known and must become code/config.

## Method

1. Define each event type: exact score, 1X2, outright, numeric total, custom question.
2. Define points for each hit condition.
3. Define bonus rules separately from base points.
4. Define multipliers as a strategy choice, not as truth probability.
5. Write a minimal scoring table with examples.
6. Add tests for edge cases before running strategy.

## Required Tests

- exact score
- correct result but wrong score
- correct goal difference if relevant
- draw bonus
- outsider bonus
- multiplier/doublette
- miss gives zero or expected fallback

## Output

Produce:

- scoring config
- scoring examples
- unit tests
- notes for ambiguous rules

## Common Errors

- mixing 90-minute and extra-time results
- treating a bonus as probability
- hardcoding one tournament name in generic scoring code
