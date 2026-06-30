from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from PIL import Image


PALETTE = ["#1b7f5d", "#2f5f9f", "#b6632c", "#7a4fa3", "#c94f5d", "#555f6d"]
FRONTIER_LABEL_OFFSETS = {
    "risk_capped_expert": (8, -18),
    "paid_place_balanced": (8, 0),
    "selective_leverage": (8, -2),
    "max_ev": (8, -2),
    "top1_attack": (8, -2),
    "field_leverage": (8, -2),
    "expert_controlled": (8, -2),
    "draw_balanced": (8, -2),
    "anti_crowd": (8, -2),
    "market_central": (8, -2),
    "chalk_survival": (8, -2),
    "contrarian_tail": (8, -2),
}
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

    candidates = strategy_frontier_data()
    plot_strategy_frontier(
        candidates,
        output_dir / "readme-strategy-frontier-expected-payout.png",
        y_col="expected_payout",
        y_label="Expected payout",
        title="Strategy frontier - expected payout vs stress loss",
    )
    plot_strategy_frontier(
        candidates,
        output_dir / "readme-strategy-frontier-topx.png",
        y_col="p_paid",
        y_label="P(top 5%)",
        title="Strategy frontier - top-5% probability vs stress loss",
        percent_y=True,
    )
    plot_top10_strategy_ranking(
        candidates,
        output_dir / "readme-top10-strategy-ranking-expected-payout.png",
        value_col="expected_payout",
        value_label="Expected payout",
        title="Top strategy candidates by expected payout",
    )
    plot_top10_strategy_ranking(
        candidates,
        output_dir / "readme-top10-strategy-ranking-topx.png",
        value_col="p_paid",
        value_label="P(top 5%)",
        title="Top strategy candidates by top-5% probability",
        percent_x=True,
    )
    cloud = strategy_candidate_cloud(140, rng)
    plot_strategy_candidate_cloud(
        cloud,
        output_dir / "readme-strategy-candidate-cloud.png",
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


def strategy_frontier_data() -> list[dict[str, float | str | bool]]:
    """Public synthetic frontier inspired by the strategy-selection workflow."""

    return [
        {"strategy": "risk_capped_expert", "family": "risk-capped", "expected_payout": 41.8, "p_paid": 0.334, "p_top1": 0.057, "stress_loss": 2.4, "expert_alignment": 0.88, "selected": True},
        {"strategy": "paid_place_balanced", "family": "paid-place", "expected_payout": 42.1, "p_paid": 0.338, "p_top1": 0.050, "stress_loss": 4.7, "expert_alignment": 0.72, "selected": False},
        {"strategy": "selective_leverage", "family": "leverage", "expected_payout": 43.0, "p_paid": 0.329, "p_top1": 0.071, "stress_loss": 7.9, "expert_alignment": 0.58, "selected": False},
        {"strategy": "expert_controlled", "family": "expert", "expected_payout": 40.6, "p_paid": 0.326, "p_top1": 0.054, "stress_loss": 3.1, "expert_alignment": 0.91, "selected": False},
        {"strategy": "max_ev", "family": "ev", "expected_payout": 42.6, "p_paid": 0.315, "p_top1": 0.066, "stress_loss": 8.8, "expert_alignment": 0.46, "selected": False},
        {"strategy": "top1_attack", "family": "top-1", "expected_payout": 41.2, "p_paid": 0.286, "p_top1": 0.089, "stress_loss": 12.6, "expert_alignment": 0.41, "selected": False},
        {"strategy": "anti_crowd", "family": "anti-crowd", "expected_payout": 39.5, "p_paid": 0.301, "p_top1": 0.073, "stress_loss": 10.8, "expert_alignment": 0.50, "selected": False},
        {"strategy": "market_central", "family": "baseline", "expected_payout": 36.8, "p_paid": 0.292, "p_top1": 0.041, "stress_loss": 3.9, "expert_alignment": 0.66, "selected": False},
        {"strategy": "field_leverage", "family": "leverage", "expected_payout": 40.9, "p_paid": 0.310, "p_top1": 0.076, "stress_loss": 9.4, "expert_alignment": 0.52, "selected": False},
        {"strategy": "chalk_survival", "family": "survival", "expected_payout": 37.7, "p_paid": 0.318, "p_top1": 0.030, "stress_loss": 2.8, "expert_alignment": 0.70, "selected": False},
        {"strategy": "contrarian_tail", "family": "tail", "expected_payout": 38.4, "p_paid": 0.252, "p_top1": 0.096, "stress_loss": 15.2, "expert_alignment": 0.33, "selected": False},
        {"strategy": "draw_balanced", "family": "risk-capped", "expected_payout": 39.9, "p_paid": 0.322, "p_top1": 0.048, "stress_loss": 5.4, "expert_alignment": 0.79, "selected": False},
    ]


def strategy_candidate_cloud(n_candidates: int, rng: np.random.Generator) -> list[dict[str, float | str | bool]]:
    families = [
        ("baseline", 0.292, 0.041, 36.0),
        ("ev", 0.315, 0.066, 41.5),
        ("anti-crowd", 0.302, 0.073, 39.5),
        ("top-1", 0.286, 0.089, 40.5),
        ("paid-place", 0.334, 0.050, 41.8),
        ("expert", 0.326, 0.054, 40.8),
        ("risk-capped", 0.329, 0.052, 41.3),
    ]
    rows: list[dict[str, float | str | bool]] = []
    for idx in range(n_candidates):
        family, base_paid, base_top1, base_payout = families[idx % len(families)]
        p_paid = float(np.clip(rng.normal(base_paid, 0.012), 0.22, 0.37))
        p_top1 = float(np.clip(rng.normal(base_top1, 0.010), 0.015, 0.12))
        expected_payout = float(
            np.clip(
                rng.normal(base_payout + 42.0 * (p_paid - base_paid) + 58.0 * (p_top1 - base_top1), 1.1),
                33.0,
                45.5,
            )
        )
        rows.append(
            {
                "strategy": f"{family}_{idx:03d}",
                "family": family,
                "p_paid": p_paid,
                "p_top1": p_top1,
                "expected_payout": expected_payout,
                "selected": False,
            }
        )
    return rows


def plot_strategy_frontier(
    rows: list[dict[str, float | str | bool]],
    output_path: Path,
    *,
    y_col: str,
    y_label: str,
    title: str,
    percent_y: bool = False,
) -> None:
    fig, ax = plt.subplots(figsize=(8.8, 4.95))
    fig.subplots_adjust(left=0.11, right=0.97, top=0.88, bottom=0.17)

    x = np.array([float(row["stress_loss"]) for row in rows])
    y = np.array([float(row[y_col]) for row in rows])
    top1 = np.array([float(row["p_top1"]) for row in rows])
    expert = np.array([float(row["expert_alignment"]) for row in rows])
    sizes = 220 + 3200 * top1

    scatter = ax.scatter(
        x,
        y,
        s=sizes,
        c=expert,
        cmap="viridis",
        alpha=0.86,
        edgecolor="#263238",
        linewidth=0.55,
    )
    selected = next(row for row in rows if bool(row["selected"]))
    selected_x = float(selected["stress_loss"])
    selected_y = float(selected[y_col])
    ax.scatter(
        [selected_x],
        [selected_y],
        s=560,
        facecolors="none",
        edgecolors="#c0392b",
        linewidths=2.0,
        zorder=4,
    )

    for row in rows:
        strategy = str(row["strategy"])
        offset = FRONTIER_LABEL_OFFSETS.get(strategy, (8, -2))
        is_selected = bool(row["selected"])
        ax.annotate(
            f"SELECTED - {strategy.replace('_', ' ')}" if is_selected else strategy.replace("_", " "),
            xy=(float(row["stress_loss"]), float(row[y_col])),
            xytext=offset,
            textcoords="offset points",
            fontsize=9 if is_selected else 8,
            fontweight="bold" if is_selected else "normal",
            color="#c0392b" if is_selected else "#263238",
            va="center",
            bbox={"boxstyle": "round,pad=0.12", "fc": "white", "ec": "none", "alpha": 0.72},
        )

    ax.set_title(title, loc="left", fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("Stress loss")
    ax.set_ylabel(y_label)
    ax.set_xlim(float(x.min()) - 0.65, float(x.max()) + 2.2)
    if percent_y:
        ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter(1.0, decimals=0))
    cbar = fig.colorbar(scatter, ax=ax, fraction=0.034, pad=0.02)
    cbar.set_label("Expert alignment", rotation=90)
    ax.grid(True, axis="both", alpha=0.75)
    fig.savefig(output_path, format="png", facecolor="white")
    plt.close(fig)


def plot_top10_strategy_ranking(
    rows: list[dict[str, float | str | bool]],
    output_path: Path,
    *,
    value_col: str,
    value_label: str,
    title: str,
    percent_x: bool = False,
) -> None:
    top_rows = sorted(rows, key=lambda row: float(row[value_col]), reverse=True)[:10]
    labels = [str(row["strategy"]).replace("_", " ") for row in top_rows][::-1]
    values = np.array([float(row[value_col]) for row in top_rows][::-1])
    selected = [bool(row["selected"]) for row in top_rows][::-1]
    colors = ["#1b7f5d" if flag else "#8fa3b5" for flag in selected]

    fig, ax = plt.subplots(figsize=(8.8, 4.95))
    fig.subplots_adjust(left=0.29, right=0.97, top=0.88, bottom=0.17)
    ax.barh(labels, values, color=colors, alpha=0.92)
    ax.set_xlim(0, float(values.max()) * 1.12)
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel(value_label)
    ax.set_ylabel("")
    if percent_x:
        ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter(1.0, decimals=0))
    for idx, (value, flag) in enumerate(zip(values, selected, strict=True)):
        label = " (selected)" if flag else ""
        shown = f"{100 * value:.1f}%{label}" if percent_x else f"{value:.1f}{label}"
        ax.text(value, idx, f"  {shown}", va="center", fontsize=8, color="#263238")
    ax.grid(True, axis="x", alpha=0.75)
    ax.grid(False, axis="y")
    fig.savefig(output_path, format="png", facecolor="white")
    plt.close(fig)


def plot_strategy_candidate_cloud(
    rows: list[dict[str, float | str | bool]],
    output_path: Path,
) -> None:
    family_colors = {
        "baseline": "#8fa3b5",
        "ev": "#2f5f9f",
        "anti-crowd": "#7a4fa3",
        "top-1": "#c94f5d",
        "paid-place": "#1b7f5d",
        "expert": "#e0b83f",
        "risk-capped": "#2f9d76",
    }
    family_labels = {
        "baseline": "baseline-led",
        "ev": "ev-led",
        "anti-crowd": "anti-crowd-led",
        "top-1": "top-1-led",
        "paid-place": "paid-place-led",
        "expert": "expert-led",
        "risk-capped": "risk-capped-led",
    }
    fig, ax = plt.subplots(figsize=(8.8, 4.95))
    fig.subplots_adjust(left=0.10, right=0.97, top=0.88, bottom=0.25)
    for family, color in family_colors.items():
        group = [row for row in rows if row["family"] == family]
        if not group:
            continue
        ax.scatter(
            [float(row["p_paid"]) for row in group],
            [float(row["expected_payout"]) for row in group],
            s=[70 + 3100 * float(row["p_top1"]) for row in group],
            color=color,
            alpha=0.52,
            edgecolor="#263238",
            linewidth=0.25,
            label=family_labels[family],
        )
    ax.axvline(0.305, color="#6f768a", linewidth=0.9, linestyle="--", alpha=0.55)
    ax.axhline(41.0, color="#6f768a", linewidth=0.9, linestyle="--", alpha=0.55)
    ax.text(
        0.325,
        44.7,
        "strong candidates",
        color="#464c55",
        fontsize=8,
        ha="center",
        va="center",
        bbox={"boxstyle": "round,pad=0.16", "fc": "white", "ec": "none", "alpha": 0.68},
    )
    ax.set_title("Monte Carlo candidate strategies", loc="left", fontsize=13, fontweight="bold", pad=10)
    ax.set_xlabel("P(top 5%)")
    ax.set_ylabel("Expected payout")
    ax.xaxis.set_major_formatter(mpl.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_xlim(0.245, 0.365)
    ax.set_ylim(32.5, 46.0)
    ax.grid(True, axis="both", alpha=0.75)
    ax.legend(
        frameon=False,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
        ncol=4,
        fontsize=8,
        title="Dominant ingredient",
        title_fontsize=8,
    )
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
