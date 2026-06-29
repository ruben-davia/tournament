# Simulation Method

The framework simulates a contest, not only football matches.

A contest simulation needs four layers:

1. what happens in the real tournament
2. what you pick
3. what other players pick
4. how the leaderboard and payout resolve

## 1. Simulate Real Outcomes

For each event, sample the true outcome from the truth model.

For football contests this can include:

- exact scores
- match result
- total goals
- special questions
- tournament winner
- player awards
- stage reached

Use scenarios when the truth model is uncertain:

- base market scenario
- draw-heavy or draw-light scenario
- favorite-heavy or outsider-heavy scenario
- low-score or high-score scenario
- tail-heavy scenario for unusual scores

The point is not to pretend that one probability table is perfect. The point is to test whether a strategy still works when the world is slightly different from the base model.

## 2. Simulate Opponent Picks

The field model estimates how other players behave.

Common field profiles:

- safe favorites
- common exact scores
- market-EV aware players
- contrarian players
- team/visibility biased players
- players who copy popular choices
- players who chase multipliers

Observed public picks are better than a prior when they are available. If they are not available, build a prior from market probability, contest EV, common score bias, visibility, and simple behavior assumptions.

## 3. Simulate Your Strategy

A strategy is a portfolio, not a single pick.

It can contain:

- one pick per match
- multiplier choices
- special-question answers
- intentional correlations
- anti-crowd exposure
- risk caps

Examples:

- safe baseline
- maximum expected points
- contrarian upside
- risk-capped survival
- top-1 attack
- balanced paid-place strategy

## 4. Score The Leaderboard

For every simulation:

1. score your portfolio
2. score every opponent
3. rank the leaderboard
4. apply tie-breaks if known
5. compute payout or paid-place result

Then aggregate:

- probability of top 1
- probability of top X, where X is the number of paid places
- probability of top 10 percent
- expected payout
- expected rank
- bad-tail probability
- regret versus baseline

## Static Versus Adaptive Simulation

Use static simulation when:

- the contest has not started
- all picks are locked at once
- the objective is to choose a full-tournament portfolio

Use adaptive simulation when:

- matches are already played
- the current leaderboard matters
- players can still submit future picks
- multipliers remain available
- the optimal risk level changes over time

Adaptive simulation should lock known history, then simulate only the remaining contest from the current state.

## Output

A useful simulation output is not just "pick this".

It should include:

- recommended portfolio
- alternative portfolios
- robust frontier
- scenario comparison
- pick-level diagnostics
- field exposure
- expert conflicts
- risk flags
- explanation of why the recommendation beats the baseline
