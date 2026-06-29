from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from PIL import Image


PALETTE = ["#1b7f5d", "#2f5f9f", "#b6632c", "#7a4fa3", "#c94f5d", "#555f6d"]
ROUND_LABELS = [
    "After group round 1",
    "After group round 2",
    "After group round 3",
    "After knockout entry",
    "After round of 16",
    "After quarter-finals",
    "After semi-finals",
    "After final",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate README charts from a public deterministic tournament simulation.")
    parser.add_argument("--output-dir", default="docs/assets")
    parser.add_argument("--seed", type=int, default=20260612)
    parser.add_argument("--n-sims", type=int, default=200_000)
    parser.add_argument("--n-opponents", type=int, default=125)
    parser.add_argument("--gif-duration-ms", type=int, default=900)
    parser.add_argument("--no-gif", action="store_true")
    parser.add_argument("--smoothing-sigma", type=float, default=2.5)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    configure_plot_style()

    rng = np.random.default_rng(args.seed)
    data = simulate_public_rank_samples(args.n_sims, args.n_opponents, rng)

    plot_rank_distribution(
        {"recommended": data["recommended"]},
        {"recommended": "Recommended"},
        "Probability mass of final rank - recommended portfolio",
        output_dir / "readme-final-rank-distribution-recommended.png",
        x_max=args.n_opponents + 1,
        smoothing_sigma=args.smoothing_sigma,
        show_legend=False,
    )

    frame_paths = plot_round_frames(
        data["rounds"],
        output_dir=output_dir,
        x_max=args.n_opponents + 1,
        smoothing_sigma=args.smoothing_sigma,
    )
    if not args.no_gif:
        build_gif(
            frame_paths,
            output_dir / "readme-rank-distribution-tournament-rounds.gif",
            duration_ms=args.gif_duration_ms,
        )

    strategy_labels = {
        "market_central": "Market central",
        "max_ev": "Max EV",
        "expert_controlled": "Expert controlled",
        "risk_capped": "Risk capped",
        "selective_leverage": "Selective leverage",
    }
    plot_rank_distribution(
        data["strategies"],
        strategy_labels,
        "Probability mass of final rank by strategy",
        output_dir / "readme-final-rank-distribution-by-strategy.png",
        x_max=args.n_opponents + 1,
        smoothing_sigma=args.smoothing_sigma,
    )

    scenario_labels = {
        "base": "Base",
        "crowd_chalk": "Crowd chalk",
        "noisy_inputs": "Noisy inputs",
        "field_learns": "Field learns",
        "sharp_field": "Sharp field",
    }
    plot_rank_distribution(
        data["scenarios"],
        scenario_labels,
        "Probability mass of final rank by scenario",
        output_dir / "readme-final-rank-distribution-by-scenario.png",
        x_max=args.n_opponents + 1,
        smoothing_sigma=args.smoothing_sigma,
    )


def configure_plot_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif"],
            "mathtext.fontset": "dejavuserif",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "figure.dpi": 160,
            "savefig.dpi": 160,
        }
    )
    sns.set_theme(
        context="paper",
        style="whitegrid",
        rc={"font.family": "serif", "grid.color": "#d9dee3", "grid.linewidth": 0.7},
    )


def simulate_public_rank_samples(
    n_sims: int,
    n_opponents: int,
    rng: np.random.Generator,
) -> dict[str, dict[str, np.ndarray] | np.ndarray]:
    """Create anonymous Monte Carlo rank samples for README figures.

    The simulation is intentionally public and generic. It models ranks as the
    result of our latent portfolio score against a field of opponent portfolio
    scores. Higher score means a better leaderboard finish.
    """

    strategies = {
        "market_central": sample_ranks(n_sims, n_opponents, our_mean=0.35, our_sd=0.95, field_mean=0.0, field_sd=1.0, rng=rng),
        "max_ev": sample_ranks(n_sims, n_opponents, our_mean=0.72, our_sd=1.05, field_mean=0.0, field_sd=1.0, rng=rng),
        "expert_controlled": sample_ranks(n_sims, n_opponents, our_mean=0.86, our_sd=0.92, field_mean=0.0, field_sd=1.0, rng=rng),
        "risk_capped": sample_ranks(n_sims, n_opponents, our_mean=1.02, our_sd=0.78, field_mean=0.0, field_sd=1.0, rng=rng),
        "selective_leverage": sample_ranks(n_sims, n_opponents, our_mean=1.05, our_sd=1.18, field_mean=0.0, field_sd=1.0, rng=rng),
    }
    scenarios = {
        "base": strategies["risk_capped"],
        "crowd_chalk": sample_ranks(n_sims, n_opponents, our_mean=1.12, our_sd=0.80, field_mean=-0.08, field_sd=0.98, rng=rng),
        "noisy_inputs": sample_ranks(n_sims, n_opponents, our_mean=0.72, our_sd=1.15, field_mean=0.0, field_sd=1.05, rng=rng),
        "field_learns": sample_ranks(n_sims, n_opponents, our_mean=0.92, our_sd=0.84, field_mean=0.10, field_sd=0.95, rng=rng),
        "sharp_field": sample_ranks(n_sims, n_opponents, our_mean=0.76, our_sd=0.84, field_mean=0.18, field_sd=0.92, rng=rng),
    }
    round_means = np.array([0.10, 0.24, 0.42, 0.62, 0.78, 0.92, 1.04, 1.12])
    round_sds = np.array([1.12, 1.06, 0.98, 0.92, 0.88, 0.84, 0.81, 0.78])
    rounds = {
        label: sample_ranks(
            n_sims,
            n_opponents,
            our_mean=float(mean),
            our_sd=float(sd),
            field_mean=0.0,
            field_sd=1.0,
            rng=rng,
        )
        for label, mean, sd in zip(ROUND_LABELS, round_means, round_sds, strict=True)
    }
    return {"recommended": strategies["risk_capped"], "strategies": strategies, "scenarios": scenarios, "rounds": rounds}


def sample_ranks(
    n_sims: int,
    n_opponents: int,
    *,
    our_mean: float,
    our_sd: float,
    field_mean: float,
    field_sd: float,
    rng: np.random.Generator,
    chunk_size: int = 25_000,
) -> np.ndarray:
    ranks = np.empty(n_sims, dtype=np.int16)
    for start in range(0, n_sims, chunk_size):
        stop = min(start + chunk_size, n_sims)
        size = stop - start
        our_scores = rng.normal(our_mean, our_sd, size=size)
        opponent_scores = rng.normal(field_mean, field_sd, size=(size, n_opponents))
        ranks[start:stop] = 1 + (opponent_scores > our_scores[:, None]).sum(axis=1)
    return ranks


def rank_probability_mass(
    values: np.ndarray,
    *,
    smoothing_sigma: float,
    x_max: int,
) -> tuple[np.ndarray, np.ndarray]:
    ranks = np.clip(np.rint(values).astype(int), 1, x_max)
    counts = np.bincount(ranks, minlength=x_max + 1)[1 : x_max + 1].astype(float)
    probabilities = counts / counts.sum()
    radius = max(1, int(np.ceil(smoothing_sigma * 4)))
    offsets = np.arange(-radius, radius + 1)
    kernel = np.exp(-0.5 * (offsets / smoothing_sigma) ** 2)
    kernel = kernel / kernel.sum()
    mass = np.convolve(probabilities, kernel, mode="same")
    mass = mass / mass.sum()
    return np.arange(1, x_max + 1), mass


def plot_round_frames(
    frames: dict[str, np.ndarray],
    *,
    output_dir: Path,
    x_max: int,
    smoothing_sigma: float,
) -> list[Path]:
    ymax = max(
        rank_probability_mass(values, smoothing_sigma=smoothing_sigma, x_max=x_max)[1].max()
        for values in frames.values()
    )
    fixed_ylim = max(0.05, ymax * 1.18)
    frame_paths: list[Path] = []
    for idx, (title, values) in enumerate(frames.items(), start=1):
        output_path = output_dir / f"readme-rank-distribution-round-{idx:02d}.png"
        plot_rank_distribution(
            {title: values},
            {title: title},
            f"Probability mass of rank - {title.lower()}",
            output_path,
            x_max=x_max,
            fixed_ylim=fixed_ylim,
            show_legend=False,
            smoothing_sigma=smoothing_sigma,
            x_label="Rank",
        )
        frame_paths.append(output_path)
    return frame_paths


def plot_rank_distribution(
    series: dict[str, np.ndarray],
    labels: dict[str, str],
    title: str,
    output_path: Path,
    *,
    x_max: int,
    fixed_ylim: float | None = None,
    show_legend: bool = True,
    smoothing_sigma: float = 2.5,
    x_label: str = "Final rank",
) -> None:
    fig, ax = plt.subplots(figsize=(8.8, 4.95))
    fig.subplots_adjust(left=0.10, right=0.97, top=0.88, bottom=0.18)

    ax.axvspan(1, 6, color="#dcefe7", alpha=0.9, lw=0)
    for idx, key in enumerate(labels):
        x, y = rank_probability_mass(series[key], smoothing_sigma=smoothing_sigma, x_max=x_max)
        ax.plot(x, y, lw=2.0, color=PALETTE[idx % len(PALETTE)], label=labels[key])

    ax.axvline(5, color="#7f8c8d", lw=0.8, ls="--", alpha=0.65)
    ax.set_xlim(1, x_max)
    ymax = max(rank_probability_mass(series[key], smoothing_sigma=smoothing_sigma, x_max=x_max)[1].max() for key in labels)
    ax.set_ylim(0, fixed_ylim if fixed_ylim is not None else max(0.05, ymax * 1.18))
    ax.set_xlabel(x_label)
    ax.set_ylabel("Probability mass")
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold", pad=10)
    ax.set_xticks([tick for tick in [1, 5, 20, 40, 60, 80, 100, 126] if tick <= x_max])
    ax.set_yticks(np.linspace(0, ax.get_ylim()[1], 5))
    ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter(1.0, decimals=0))
    ax.grid(True, axis="y", alpha=0.9)
    ax.grid(True, axis="x", alpha=0.35)
    if show_legend and len(labels) > 1:
        ax.legend(frameon=False, loc="upper right", ncol=1, handlelength=2.2)

    fig.savefig(output_path, format="png", facecolor="white")
    plt.close(fig)


def build_gif(frame_paths: list[Path], output_path: Path, *, duration_ms: int) -> None:
    if not frame_paths:
        return
    frames = [Image.open(path).convert("P", palette=Image.Palette.ADAPTIVE) for path in frame_paths]
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:] + [frames[-1]],
        duration=[duration_ms] * len(frames) + [duration_ms * 2],
        loop=0,
        optimize=False,
        disposal=2,
    )


if __name__ == "__main__":
    main()
