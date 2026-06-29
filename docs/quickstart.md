# Quickstart

## 1. Run The Public Example

The example uses in-memory synthetic data and demonstrates the full path from market inputs to recommended portfolio.

```bash
python examples/basic_football_pool/run_example.py
```

## 2. Create `options.csv`

For your own tournament, create `data/raw/options.csv` with one row per possible pick.

Minimum columns:

- `event_id`
- `option_id`
- `label`
- `decimal_odds`
- `points_if_hit`

Optional but useful:

- `popularity_hint`
- `expert_support`

## 3. Normalize Probabilities

Use this when your input has decimal odds or unnormalized probability weights.

```bash
python scripts/build_probabilities.py --input-dir data/raw --output-dir data/work
```

Output: `data/work/probabilities.csv` with `truth_probability`.

## 4. Estimate The Field

Use this to estimate what other players are likely to pick.

```bash
python scripts/build_field_model.py --input-dir data/work --output-dir data/work
```

Output: `data/work/field_probabilities.csv` with `field_probability` and value diagnostics.

## 5. Simulate And Rank Strategies

Use this to compare portfolio families by leaderboard outcome.

```bash
python scripts/run_strategy.py --input-dir data/work --output-dir data/out --n-sims 5000
```

Output: `data/out/strategy_summary.csv`.

## 6. Interpret Outputs

Important strategy columns:

- `p_paid`: probability to finish in the paid places
- `p_top_1`: probability to finish first
- `mean_rank`: average simulated rank
- `mean_points`: average simulated score

Use [function-map.md](function-map.md) when an agent needs to choose the right function directly from Python.
