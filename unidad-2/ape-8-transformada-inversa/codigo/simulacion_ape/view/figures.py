"""Vista gráfica: histogramas con su densidad teórica (algoritmos 1, 3 y 5)."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from ..model.inverse_transform import exponential_density  # noqa: E402

BLUE, ORANGE, GREEN = "#1f5fa8", "#e07b00", "#2e8b57"
BINS = 50


def plot_uniform(u: np.ndarray, path: Path) -> None:
    """Histograma de U normalizado frente a la densidad f(u) = 1."""
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.hist(u, bins=BINS, range=(0, 1), density=True, color=BLUE, alpha=0.7, edgecolor="white",
            label="Histograma de U")
    ax.plot([0, 1], [1, 1], "k-", linewidth=2, label="Densidad teórica f(u) = 1")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.3)
    ax.set_xlabel("u")
    ax.set_ylabel("Densidad")
    ax.set_title(f"Distribución uniforme U(0,1), N = {len(u):_}".replace("_", " "))
    ax.legend(loc="lower center")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_exponential(x: np.ndarray, rate: float, path: Path) -> None:
    """Histograma de X con la curva teórica f(x) = λ·e^(-λx) (algoritmo 3)."""
    upper = float(np.quantile(x, 0.999))
    grid = np.linspace(0, upper, 400)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.hist(x, bins=BINS, range=(0, upper), density=True, color=BLUE, alpha=0.7, edgecolor="white",
            label="Histograma de X (transformada inversa)")
    ax.plot(grid, exponential_density(grid, rate), "-", color=ORANGE, linewidth=2,
            label=f"Densidad teórica f(x) = {rate}·e^(−{rate}x)")
    ax.set_xlim(0, upper)
    ax.set_xlabel("x")
    ax.set_ylabel("Densidad")
    ax.set_title(f"Distribución exponencial, λ = {rate}, N = {len(x):_}".replace("_", " "))
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_rates(samples: dict[float, np.ndarray], path: Path) -> None:
    """Histogramas superpuestos para cada λ con su curva teórica (algoritmo 5)."""
    upper = float(np.quantile(samples[min(samples)], 0.995))
    grid = np.linspace(0, upper, 400)
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    for (rate, x), color in zip(sorted(samples.items()), (BLUE, ORANGE, GREEN)):
        ax.hist(x, bins=BINS * 2, range=(0, upper), density=True, histtype="step", color=color, linewidth=1.4,
                label=f"Histograma λ = {rate}")
        ax.plot(grid, exponential_density(grid, rate), "--", color=color, linewidth=1.2,
                label=f"Teórica λ = {rate}")
    ax.set_xlim(0, upper)
    ax.set_xlabel("x")
    ax.set_ylabel("Densidad")
    ax.set_title("Distribución exponencial para distintos valores de λ")
    ax.legend(ncols=2)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
