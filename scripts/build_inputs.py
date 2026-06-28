#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a contest options CSV for the framework.")
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--n-sims", type=int, default=1000)
    args = parser.parse_args()

    source = args.input_dir / "options.csv"
    if not source.exists():
        raise FileNotFoundError(f"Expected {source}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    options = pd.read_csv(source)
    options.to_csv(args.output_dir / "options.csv", index=False)
    print(f"Wrote {args.output_dir / 'options.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

