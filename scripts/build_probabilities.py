#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from prediction_framework import build_probability_table  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize odds or probability weights by event.")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n-sims", type=int, default=1000)
    parser.add_argument("--input-file", default="options.csv")
    parser.add_argument("--odds-col", default="decimal_odds")
    parser.add_argument("--probability-col", default=None)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = pd.read_csv(args.input_dir / args.input_file)
    probabilities = build_probability_table(
        rows,
        odds_col=args.odds_col,
        probability_col=args.probability_col,
    )
    probabilities.to_csv(args.output_dir / "probabilities.csv", index=False)
    print(f"Wrote {args.output_dir / 'probabilities.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

