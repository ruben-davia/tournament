# Market And Probability Inputs

The framework does not call a betting API by default.

It expects you to provide one of these:

- `decimal_odds`: market-like decimal odds already collected elsewhere
- `truth_probability`: direct probabilities from your own model or manual work

## Decimal Odds

If your table has decimal odds, the framework converts them to probabilities:

```text
raw_probability = 1 / decimal_odds
truth_probability = raw_probability / sum(raw_probability within event)
```

Example:

```bash
python scripts/build_probabilities.py --input-dir data/raw --output-dir data/work
```

The input file should be:

```text
data/raw/options.csv
```

Minimum columns:

- `event_id`
- `option_id`
- `decimal_odds`

## Direct Probabilities

If you already have probabilities, pass the source column:

```bash
python scripts/build_probabilities.py \
  --input-dir data/raw \
  --output-dir data/work \
  --probability-col model_probability
```

## API Integrations

API integrations are intentionally out of scope for the public core.

If you fetch data from an API, do it before using the framework, then export the result into the standard options table described in `docs/data-contracts.md`.

