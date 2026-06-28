# Skill: Run Strategy Simulation

## Use When

Use this after scoring, truth probabilities, and field probabilities are ready.

## Inputs Needed

- options table
- truth probabilities
- field probabilities
- points per option
- number of opponents
- number of simulations
- seed

## Questions To Ask

- Is the target first place, top tier, or expected value?
- How many opponents are in the contest?
- Should strategies be safe, balanced, or contrarian?
- Are there constraints such as one multiplier per round?

## Steps

1. Validate probability sums per event.
2. Generate or load candidate strategies.
3. Simulate outcomes and opponent picks.
4. Rank strategies by leaderboard metrics.
5. Export the summary and chosen picks.

## Output

A strategy ranking with mean points, rank metrics, and upside probabilities.

## Common Mistakes

- Ranking by expected points only.
- Using too few simulations.
- Forgetting to set a seed for reproducibility.

