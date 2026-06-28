# Skill: Model The Field

## Use When

Use this when you need to estimate what other contestants will pick.

## Inputs Needed

- truth probabilities
- observed pick data, if available
- popularity hints
- common pick biases
- participant count

## Questions To Ask

- What picks are casual players most likely to choose?
- Are famous teams or common scores over-picked?
- Do participants copy market favorites?
- Is historical pick data available?

## Steps

1. Start with truth probability as baseline.
2. Add popularity hints where justified.
3. Normalize field probability per event.
4. Compare truth probability vs field probability.
5. Mark under-owned and over-owned options.

## Output

A table with `field_probability`, `probability_edge`, and leverage diagnostics.

## Common Mistakes

- Assuming the field is perfectly rational.
- Overfitting to one small observed sample.
- Ignoring obvious public biases.

