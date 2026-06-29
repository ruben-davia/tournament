# Skill 05: Model The Field

## Use When

You need to estimate what other contest players will pick.

## Method

1. If public picks exist, aggregate observed ownership by event and option.
2. Exclude the target player and test accounts.
3. If no observed picks exist, build a prior from:
   - truth probability
   - common score bias
   - favorite bias
   - draw avoidance
   - visible teams/players
   - contest EV
   - popularity hints
4. Normalize field probabilities by event.
5. Create field scenarios:
   - chalk/safe
   - mildly sharp
   - contrarian
   - noisy
   - visibility-biased
6. Never use field probability as truth probability.

## Code To Use

- `estimate_field_distribution(...)`

## Output

Table with:

- `event_id`
- `option_id`
- `field_probability`
- `field_source`
- `field_scenario`

## Checks

- probabilities sum to 1 by event
- field source is documented
- observed ownership and model prior are not confused
