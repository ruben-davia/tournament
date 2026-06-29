# Risk And Portfolio Strategy

Prediction contests are portfolio problems.

The safest-looking pick can be bad if everyone else has it. The highest-upside pick can be bad if it relies on too many low-probability exact scores. The framework is useful because it compares those tradeoffs explicitly.

## Main Objectives

Choose the objective from the payout structure:

| Objective | Use when | Optimize |
| --- | --- | --- |
| Paid-place strategy | Several places are paid | `P(rank <= paid_places)` |
| Top-1 strategy | Winner-take-most contest | `P(rank == 1)` |
| Balanced strategy | You need paid-place safety and win upside | Top-X first, top-1 as tie-break |
| Catch-up strategy | You are behind | Higher variance and anti-crowd leverage |
| Protect-lead strategy | You are ahead | Lower ruin risk and controlled differentiation |

## Risk Metrics

Use these diagnostics before trusting a recommendation:

- **Low-probability exact score count**: too many fragile scores can destroy the portfolio.
- **Very low-probability picks**: these should be rare and intentional.
- **Draw exposure**: many football contests underplay draws; zero-draw portfolios can be fragile.
- **Crowd concentration**: if many opponents share your pick, it gives less leaderboard leverage.
- **Expert conflicts**: a pick that fights strong expert signals needs a clear EV reason.
- **Single-match concentration**: avoid portfolios where one match decides everything.
- **Regret versus baseline**: test whether a strategy loses too much when assumptions change.
- **Scenario robustness**: a strategy should survive plausible truth and field scenarios.

## Risk-Capped Portfolio Logic

A risk-capped portfolio does not mean "play safe everywhere".

It means:

1. remove picks below a minimum probability unless they have exceptional strategic value
2. avoid severe expert conflicts unless the model edge is large
3. avoid unsupported draws
4. keep enough draw/favorite/outsider balance
5. limit crowd concentration
6. compare against baseline EV and top-X objective
7. keep top-1 upside as a tie-break

This is especially useful late in a tournament when current rank, remaining matches, and paid places matter more than abstract expected points.

## Frontier Selection

A robust frontier compares strategies across metrics:

- paid-place probability
- top-1 probability
- top-10 probability
- expected payout
- worst scenario
- regret versus baseline
- concentration
- selection quality

The recommended portfolio should come from a near-optimal band across many simulations.

Typical rule:

1. find the best paid-place probability
2. keep strategies within a tolerance band
3. within that band, prefer better expert alignment, better draw coverage, fewer low-probability picks, lower concentration, and higher top-1 upside

## Explain The Pick

Every final recommendation should answer:

- What objective is optimized?
- What is the baseline?
- Why is this better than the baseline?
- What risks remain?
- Which picks are crowd leverage?
- Which picks are risk controls?
- Which picks are expert-driven?
- What would make us change the recommendation?
