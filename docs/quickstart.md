# Quickstart

Run the example:

```bash
python examples/basic_football_pool/run_example.py
```

Use your own CSV:

```bash
python scripts/build_probabilities.py --input-dir data/raw --output-dir data/work
python scripts/build_field_model.py --input-dir data/work --output-dir data/work
python scripts/run_strategy.py --input-dir data/work --output-dir data/out --n-sims 5000
```

Your raw folder should contain `options.csv`.

Minimum columns:

- `event_id`
- `option_id`
- `label`
- `decimal_odds`
- `points_if_hit`

Optional but useful:

- `popularity_hint`
