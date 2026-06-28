#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from prediction_framework import rank_strategies  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank candidate strategies by simulated leaderboard outcomes.")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n-sims", type=int, default=1000)
    parser.add_argument("--n-opponents", type=int, default=100)
    parser.add_argument("--input-file", default="field_probabilities.csv")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    options = pd.read_csv(args.input_dir / args.input_file)
    summary = rank_strategies(
        options,
        n_sims=args.n_sims,
        n_opponents=args.n_opponents,
        seed=args.seed,
    )
    summary.to_csv(args.output_dir / "strategy_summary.csv", index=False)
    print(f"Wrote {args.output_dir / 'strategy_summary.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

