# Skill: Prepare Probability Inputs

## Use When

Use this when odds, model outputs, or manual probabilities need to become framework inputs.

## Inputs Needed

- raw odds or probability source
- event ids
- option ids
- option labels
- source timestamp

## Questions To Ask

- Are odds decimal, fractional, or American?
- Do probabilities already sum to 1 per event?
- Are multiple sources being blended?
- Is there overround/vig to remove?

## Steps

1. Create an options table.
2. Normalize one probability distribution per event.
3. Preserve source columns for auditability.
4. Save the result as probabilities input.

## Output

A table with `event_id`, `option_id`, `label`, and `truth_probability`.

## Common Mistakes

- Normalizing across the whole file instead of per event.
- Mixing options from different markets in one event.
- Dropping source metadata too early.

