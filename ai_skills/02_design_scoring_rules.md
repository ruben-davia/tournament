# Skill: Design Scoring Rules

## Use When

Use this when contest rules need to be converted into deterministic scoring logic.

## Inputs Needed

- full written rules
- examples of scored picks
- bonus and multiplier rules
- tie-breaker rules, if any

## Questions To Ask

- What earns full points?
- What earns partial points?
- Can a wrong result still earn points?
- Are bonuses added before or after multipliers?
- Are there per-player limits on multipliers?

## Steps

1. Convert the rules into cases.
2. Write one example per case.
3. Map cases to framework scoring helpers or note custom logic needed.
4. Define test cases before simulation.

## Output

A scoring spec with examples and expected point totals.

## Common Mistakes

- Encoding rules only in prose.
- Forgetting edge cases such as draws or tied odds.
- Applying multipliers in the wrong order.

