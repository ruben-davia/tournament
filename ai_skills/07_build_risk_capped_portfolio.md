# Skill 07: Build Risk-Capped Portfolio

## Use When

The user needs picks that can win or finish paid without taking uncontrolled risk.

## Method

1. Start from the objective: paid places, top 1, catch-up, or protect lead.
2. Add pick-level risk flags:
   - low probability
   - crowded
   - expert conflict
   - proxy market
3. Remove severe picks unless they have clear upside.
4. Keep enough leverage versus the field.
5. Avoid too many fragile exact scores.
6. Check draw exposure against model-implied draw frequency.
7. Compare risk-capped portfolio to baseline EV.
8. Choose from a near-optimal frontier, not one noisy run.

## Code To Use

- `add_pick_risk_flags(...)`
- `build_risk_capped_portfolio(...)`
- `rank_risk_frontier(...)`

## Output

- selected portfolio
- `selection_reason` per pick
- risk flags
- comparison against favorite/EV baseline
- remaining risks

## Hard Rule

Do not recommend a pick only because it is contrarian. It must still have enough probability, payout value, or scenario value.
