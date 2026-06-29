# Function Map

Use this page when an agent or new user needs to choose the right public function.

| Goal | Use | Required inputs | Output | Avoid when |
| --- | --- | --- | --- | --- |
| Normalize decimal odds or raw probabilities | `build_probability_table(...)` | `event_id`, `option_id`, `decimal_odds` or probability column | options table with `truth_probability` | multiple sources need blending |
| Blend bookmaker, prediction-market, or model sources | `build_source_probability_table(...)` | `event_id`, `option_id`, `source`, odds or source probability, source quality | one truth table with source diagnostics | each option has only one clean probability |
| Compare probability sources | `compare_source_probabilities(...)` | normalized source rows | disagreement diagnostics | no overlapping sources exist |
| Audit expert signals | `audit_expert_signals(...)` | signal table with target, direction, confidence, source | reviewed signal status | signals are already reviewed and bounded |
| Apply expert signals | `apply_expert_signals(...)` | options with `truth_probability`, reviewed signals | adjusted truth probabilities | signals are vague, stale, or unreviewed |
| Estimate opponent ownership | `estimate_field_distribution(...)` | `event_id`, `truth_probability`, optional `popularity_hint` | `field_probability` by option | observed field data needs a custom aggregation first |
| Add pick-level value diagnostics | `add_value_diagnostics(...)` | truth probability, field probability, points | EV, leverage, contrarian value | the table has no field model yet |
| Simulate candidate portfolios | `simulate_leaderboard(...)` | options with truth and field probabilities, optional candidate picks | summary, picks, rank distribution, metadata | you only need the summary table |
| Rank strategies only | `rank_strategies(...)` | same inputs as simulation | ranked strategy summary | you need rank-distribution rows |
| Full end-to-end portfolio recommendation | `run_betting_tournament_strategy(...)` | normalized truth and field probabilities | strategy summary, distributions, recommended portfolio | probabilities or field model are not prepared |
| Build risk-controlled picks | `build_risk_capped_portfolio(...)` | truth probability, field probability, points, optional expert support | one selected pick per event with risk reasons | payout objective requires full simulation comparison |
| Rank near-optimal strategy frontier | `rank_risk_frontier(...)` | simulated summary with `p_paid` and `p_top_1` | frontier-ranked strategy table | simulation metrics are missing |
| Score an exact football prediction | `score_prediction(...)` | predicted score, actual score, `MatchContext` | detailed point breakdown | contest is not exact-score based |
| Fit live continuation values | `fit_backward_value_model(...)` | rollout states, checkpoint, terminal value | continuation-value model | tournament is static and all picks are locked |

## Typical Agent Route

For a new tournament:

1. `build_probability_table(...)` or `build_source_probability_table(...)`
2. `audit_expert_signals(...)` and `apply_expert_signals(...)` when expert inputs exist
3. `estimate_field_distribution(...)`
4. `add_value_diagnostics(...)`
5. `run_betting_tournament_strategy(...)`
6. `rank_risk_frontier(...)` or `build_risk_capped_portfolio(...)` for final risk control

For a live tournament, add `fit_backward_value_model(...)` after simulations produce state rollouts.
