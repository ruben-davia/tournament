# Source Research Playbook

This framework works only if the inputs are honest about what they represent.

The goal is to build a source stack, label each signal, and avoid mixing truth probability with popularity.

## Source Families

| Source | Best use | Main risk |
| --- | --- | --- |
| Bookmaker odds, for example Winamax | Exact scores, 1X2, totals, player markets, derivative markets | Overround, market availability, ambiguous labels |
| Prediction markets, for example Polymarket | Tournament outrights, long-range questions, sentiment, source disagreement | Liquidity, spread, proxy definitions |
| Expert previews | Injuries, lineups, tactical notes, motivation, game state | Narrative bias, stale articles, unreviewed scraping |
| Observed contest data | Field ownership, public picks, leaderboard state, multiplier usage | Private data risk, sample bias, stale scrape |
| Your own model | Prior beliefs, scenario stress, custom features | Overfitting, false precision |

## Market Data Workflow

1. List every contest question and match option.
2. For each option, find the most direct market.
3. Convert decimal odds to implied probability.
4. Remove overround within the market group.
5. Keep the raw source, timestamp, market label, and mapping note.
6. Mark proxy mappings explicitly.
7. Compare sources when two sources cover the same option.
8. Use disagreement as uncertainty, not as automatic truth.

## Winamax / Polymarket Pattern

Use bookmaker odds when you need structured football markets:

- exact score
- 1X2
- totals
- both teams to score
- team totals
- player props

Use prediction markets when you need broad event probabilities:

- winner
- reaches final
- top scorer
- best player
- long-range tournament outcomes

When both exist:

- compare probabilities after normalization
- check spread, liquidity, and update time
- label direct comparisons separately from proxies
- increase uncertainty when sources disagree strongly

## Expert Signal Workflow

Expert sources should not blindly overwrite market probabilities.

Use them to answer questions markets do not fully capture:

- Is a key player unavailable?
- Are lineups expected to rotate?
- Is the tactical matchup likely to reduce scoring?
- Are experts consistently leaning toward one side?
- Is the market stale relative to new information?

Recommended normalized signal fields:

| Field | Example values |
| --- | --- |
| `event_id` | stable match/question id |
| `source_name` | source or analyst name |
| `source_url` | URL or internal reference |
| `published_at` | timestamp |
| `signal_target` | `home`, `away`, `draw`, `favorite`, `outsider`, `low_score`, `high_score` |
| `signal_direction` | `up`, `down` |
| `confidence` | `low`, `medium`, `high` |
| `note` | short reviewed explanation |
| `review_status` | `candidate`, `reviewed`, `rejected` |

## Quality Gates

Do not use a source until these questions are answered:

- Is the market definition identical to the contest question?
- Is it a direct market or a proxy?
- Is the timestamp current enough?
- Is there enough liquidity or bookmaker confidence?
- Does the source conflict with another source?
- Is the signal truth-related or popularity-related?
- Can someone reproduce the mapping later?

## Output

The output of source research should be a clean probability input table, not raw scraped data:

- one row per event option
- normalized truth probability
- source family
- source quality
- uncertainty flag
- notes for proxies and disagreements

Raw snapshots and scraped pages should stay local unless they are intentionally anonymized and legally safe to publish.
