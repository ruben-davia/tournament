# Adapting A New Tournament

Use this checklist when applying the framework to a new football prediction contest.

## 1. Define The Contest

Write down:

- number of participants
- events or questions
- possible options for each event
- scoring rules
- prizes or leaderboard target

## 2. Prepare Options

Create one row per event option.

Examples:

- match exact score: `France 2-0`
- match result: `France win`
- tournament question: `Brazil champion`

Each option needs a stable `event_id` and `option_id`.

## 3. Prepare Truth Probabilities

Choose one source:

- decimal odds
- model probabilities
- manual probabilities

Normalize probabilities within each event.

## 4. Estimate The Field

Decide what makes an option popular:

- favorite team
- common exact score
- famous player
- home-country bias
- market favorite
- social visibility

Add a `popularity_hint` column if you have one.

## 5. Simulate Strategies

Run the simulator with:

- number of opponents
- number of simulations
- candidate strategies
- random seed

Start simple, then add complexity only if it changes the decision.

## 6. Explain The Recommendation

A good recommendation should say:

- what to pick
- why it has value
- what can go wrong
- whether it is safe, balanced, or contrarian

