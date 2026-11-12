"""Vista gráfica: guarda las figuras del informe con Matplotlib."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from ..model.experiment import Row  # noqa: E402

BLUE, ORANGE, GRAY = "#1f5fa8", "#e07b00", "#555555"


def plot_circle(points: list[tuple[float, float, bool]], path: Path) -> None:
    """Puntos dentro y fuera del círculo inscrito en el cuadrado."""
    inside = [(x, y) for x, y, hit in points if hit]
    outside = [(x, y) for x, y, hit in points if not hit]
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    ax.scatter(*zip(*inside), s=3, color=BLUE, label=f"Dentro ({len(inside)})")
    ax.scatter(*zip(*outside), s=3, color=ORANGE, label=f"Fuera ({len(outside)})")
    ax.add_patch(plt.Circle((0, 0), 1, fill=False, color="black", linewidth=1.2))
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect("equal")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"N = {len(points):,} puntos, π ≈ {4 * len(inside) / len(points):.4f}".replace(",", " "))
    ax.legend(loc="upper right", markerscale=4, framealpha=0.95)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_errors(groups: list[list[Row]], path: Path) -> None:
    """Error absoluto observado frente al error estándar teórico, en escala logarítmica."""
    fig, axes = plt.subplots(1, len(groups), figsize=(5.2 * len(groups), 4.2))
    for ax, rows in zip(axes, groups):
        experiment = rows[0].experiment
        sizes = [row.n for row in rows]
        ax.loglog(sizes, [row.python.error for row in rows], "o-", color=BLUE, label="Error absoluto observado")
        ax.loglog(sizes, [experiment.standard_error(n) for n in sizes], "--", color=GRAY,
                  label="Error estándar teórico (∝ 1/√N)")
        ax.set_xlabel("Tamaño de muestra N")
        ax.set_ylabel("Error")
        ax.set_title(experiment.label)
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_times(groups: list[list[Row]], path: Path) -> None:
    """Tiempo de ejecución de Python y de Java según el tamaño de muestra."""
    fig, axes = plt.subplots(1, len(groups), figsize=(5.2 * len(groups), 4.2))
    for ax, rows in zip(axes, groups):
        sizes = [row.n for row in rows]
        ax.loglog(sizes, [row.python.seconds for row in rows], "o-", color=BLUE, label="Python")
        ax.loglog(sizes, [row.java.seconds for row in rows], "s-", color=ORANGE, label="Java")
        ax.set_xlabel("Tamaño de muestra N")
        ax.set_ylabel("Tiempo (s)")
        ax.set_title(rows[0].experiment.label)
        ax.grid(True, which="both", alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_dice_sums(counts: dict[int, int], probability, path: Path) -> None:
    """Frecuencia observada de cada suma frente a su probabilidad exacta."""
    n = sum(counts.values())
    totals = list(counts)
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    colors = [ORANGE if total == 7 else BLUE for total in totals]
    ax.bar(totals, [counts[total] / n for total in totals], color=colors, label="Frecuencia simulada")
    ax.plot(totals, [probability(total) for total in totals], "k_", markersize=22, markeredgewidth=2,
            label="Probabilidad exacta (6 − |s − 7|)/36")
    ax.set_xticks(totals)
    ax.set_xlabel("Suma de los dos dados")
    ax.set_ylabel("Probabilidad")
    ax.set_ylim(0, 0.215)  # deja espacio para la leyenda sobre la barra más alta
    ax.set_title(f"N = {n:,} lanzamientos".replace(",", " "))
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
