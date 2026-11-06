"""Gráficas de la práctica (se guardan en figuras/)."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from ..model.experiment import Row  # noqa: E402


def plot_frequencies(rows: list[Row], path: Path) -> None:
    """Frecuencias observadas por subintervalo frente a la esperada, una por configuración."""
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), sharey=True)
    for ax, row in zip(axes.flat, rows):
        chi = row.python.chi
        k = len(chi.observed)
        centers = [(i + 0.5) / k for i in range(k)]
        ax.bar(centers, chi.observed, width=0.9 / k, color="#4C72B0", label="Observada")
        ax.axhline(chi.expected, color="#C44E52", linestyle="--", label=f"Esperada = {chi.expected:g}")
        ax.set_title(f"{row.config.name}: χ² = {chi.statistic:.2f}, p = {chi.p_value:.3f}", fontsize=10)
        ax.set_xlabel("Subintervalo de [0, 1)")
        ax.set_xticks([i / k for i in range(k + 1)])
        ax.tick_params(axis="x", labelsize=7)
    for ax in axes[:, 0]:
        ax.set_ylabel("Frecuencia")
    axes[0, 0].legend(fontsize=8)
    fig.suptitle("Prueba Chi-cuadrado: frecuencias observadas y esperadas (N = 10 000)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_ecdf(samples: list[tuple[str, list[float]]], path: Path) -> None:
    """FDE empírica frente a F(x) = x, marcando dónde ocurre la distancia máxima D."""
    fig, axes = plt.subplots(1, len(samples), figsize=(5 * len(samples), 4.5))
    for ax, (name, values) in zip(axes, samples):
        ordered = sorted(values)
        n = len(ordered)
        xs = [0.0] + ordered + [1.0]
        ys = [0.0] + [i / n for i in range(1, n + 1)] + [1.0]
        ax.step(xs, ys, where="post", color="#4C72B0", label="FDE empírica $F_N(x)$")
        ax.plot([0, 1], [0, 1], color="#C44E52", linestyle="--", label="F(x) = x")
        gaps = [(i / n - u, u, (i - 1) / n, i / n) for i, u in enumerate(ordered, start=1)]
        gaps += [(u - (i - 1) / n, u, (i - 1) / n, i / n) for i, u in enumerate(ordered, start=1)]
        d, x_at, low, high = max(gaps)
        y_from, y_to = (high, x_at) if high - x_at >= x_at - low else (low, x_at)
        ax.vlines(x_at, min(y_from, y_to), max(y_from, y_to), color="#55A868", linewidth=2.5,
                  label=f"D = {d:.4f}")
        ax.set_title(f"{name} (N = {n})", fontsize=10)
        ax.set_xlabel("x")
        ax.set_ylabel("Probabilidad acumulada")
        ax.legend(fontsize=8, loc="upper left")
    fig.suptitle("Prueba Kolmogorov-Smirnov: distribución acumulada empírica y teórica")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_p_values(rows: list[Row], alpha: float, path: Path) -> None:
    """Valores p de ambas pruebas según N, con la línea de α."""
    ns = [row.n for row in rows]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(ns, [row.python.chi.p_value for row in rows], marker="o", label="p Chi-cuadrado")
    ax.plot(ns, [row.python.ks.p_value for row in rows], marker="s", label="p Kolmogorov-Smirnov")
    ax.axhline(alpha, color="#C44E52", linestyle="--", label=f"α = {alpha}")
    ax.set_xscale("log")
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("N (escala logarítmica)")
    ax.set_ylabel("Valor p")
    ax.set_title(f"Valores p según el tamaño de muestra ({rows[0].config.name})")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
