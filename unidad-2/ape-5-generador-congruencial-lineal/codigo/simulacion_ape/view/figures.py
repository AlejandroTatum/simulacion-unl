"""Gráficas de la secuencia generada (se guardan en `codigo/figuras/`)."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def plot_sequence(values: list[float], path: Path, shown: int = 200) -> None:
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.plot(range(1, shown + 1), values[:shown], marker="o", markersize=3, linewidth=0.6)
    ax.set_xlabel("n")
    ax.set_ylabel("U(n)")
    ax.set_title(f"Primeros {shown} valores U(n) del LCG (semilla 12345)")
    ax.set_ylim(0, 1)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_pairs_and_histogram(values: list[float], path: Path) -> None:
    fig, (left, right) = plt.subplots(1, 2, figsize=(9, 4))
    left.scatter(values[:-1], values[1:], s=1, alpha=0.5)
    left.set_xlabel("U(n)")
    left.set_ylabel("U(n+1)")
    left.set_title("Pares consecutivos")
    right.hist(values, bins=20, range=(0, 1), edgecolor="black")
    right.axhline(len(values) / 20, color="red", linestyle="--", label="Frecuencia esperada")
    right.set_xlabel("U(n)")
    right.set_ylabel("Frecuencia")
    right.set_title("Histograma (20 clases)")
    right.legend()
    fig.suptitle(f"{len(values)} valores generados en Python")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_seeds(sequences: dict[int, list[float]], path: Path, shown: int = 30) -> None:
    fig, ax = plt.subplots(figsize=(8, 3.5))
    for seed, values in sequences.items():
        ax.plot(range(1, shown + 1), values[:shown], marker="o", markersize=3, linewidth=0.8,
                label=f"semilla {seed}")
    ax.set_xlabel("n")
    ax.set_ylabel("U(n)")
    ax.set_title(f"Primeros {shown} valores con semillas distintas")
    ax.set_ylim(0, 1)
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
