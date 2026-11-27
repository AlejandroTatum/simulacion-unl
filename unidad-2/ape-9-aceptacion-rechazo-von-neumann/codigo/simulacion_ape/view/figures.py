"""Vista gráfica: histograma con la curva f(x), aceptados frente a rechazados y eficiencias."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from ..model.acceptance_rejection import SamplingResult  # noqa: E402
from ..model.simulation import EfficiencyRow  # noqa: E402

BLUE, ORANGE, GREEN, RED = "#1f5fa8", "#e07b00", "#2e8b57", "#c0392b"
BINS = 30
GRID = np.linspace(0, 1, 400)


def thousands(n: int) -> str:
    return f"{n:_}".replace("_", " ")


def plot_histogram(result: SamplingResult, path: Path) -> None:
    """Histograma normalizado de los valores aceptados con la curva teórica f(x)."""
    target = result.target
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.hist(result.accepted_values, bins=BINS, range=(0, 1), density=True, color=BLUE, alpha=0.7,
            edgecolor="white", label=f"Valores aceptados ({thousands(result.n_accepted)})")
    ax.plot(GRID, target.density(GRID), "-", color=ORANGE, linewidth=2, label=f"Curva teórica {target.label}")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, target.m * 1.1)
    ax.set_xlabel("x")
    ax.set_ylabel("Densidad")
    ax.set_title(f"Aceptación-rechazo, {target.label}, N = {thousands(len(result.candidates))}")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_candidates(result: SamplingResult, path: Path) -> None:
    """Puntos (X, U·M·g(X)): los aceptados quedan bajo f(x) y los rechazados sobre ella."""
    target = result.target
    height = result.uniforms * target.m      # g(X) = 1
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.scatter(result.candidates[result.accepted], height[result.accepted], s=3, color=GREEN, alpha=0.5,
               label=f"Aceptados ({thousands(result.n_accepted)})")
    ax.scatter(result.candidates[~result.accepted], height[~result.accepted], s=3, color=RED, alpha=0.5,
               label=f"Rechazados ({thousands(result.n_rejected)})")
    ax.plot(GRID, target.density(GRID), "-", color="black", linewidth=2, label=f"Curva objetivo {target.label}")
    ax.axhline(target.m, color=BLUE, linestyle="--", linewidth=1.5, label=f"Cota M·g(x) = {target.m:g}")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, target.m * 1.4)
    ax.set_xlabel("Candidato X")
    ax.set_ylabel("U·M·g(X)")
    ax.set_title(f"Candidatos aceptados y rechazados, {target.label}")
    ax.legend(loc="upper left", markerscale=4, fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_efficiency(rows: list[EfficiencyRow], path: Path) -> None:
    """Eficiencia experimental frente a la teórica para cada N y cada distribución."""
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    labels = dict.fromkeys(row.target.label for row in rows)
    for label, color in zip(labels, (BLUE, ORANGE)):
        series = [row for row in rows if row.target.label == label]
        sizes = [row.n for row in series]
        ax.plot(sizes, [row.efficiency for row in series], "o-", color=color, label=f"Experimental {label}")
        ax.axhline(series[0].target.theoretical_efficiency, color=color, linestyle="--", linewidth=1.2,
                   label=f"Teórica {label} ({series[0].target.theoretical_efficiency:.2f} %)")
    ax.set_xticks(sorted({row.n for row in rows}))
    ax.set_xticklabels([thousands(n) for n in sorted({row.n for row in rows})])
    ax.set_ylim(20, 60)
    ax.set_xlabel("Número de candidatos N")
    ax.set_ylabel("Eficiencia (%)")
    ax.set_title("Eficiencia experimental y teórica del método")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
