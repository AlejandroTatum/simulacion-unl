"""Vista de gráficas: figuras de matplotlib guardadas en archivos."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ..model.config import HOURS, STATES


def _threshold_lines(ax):
    for bound, state in STATES:
        ax.axhline(bound, color="gray", linestyle="--", linewidth=0.8)
        ax.text(1.01, bound, state, transform=ax.get_yaxis_transform(), va="center", fontsize=8, color="gray")


def _save(fig, ax, path):
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_inputs(result, path):
    fig, ax = plt.subplots(figsize=(8, 4))
    for key, label in (("H", "Humedad H"), ("N", "Nubosidad N"), ("Tf", "Factor de temperatura Tf (tabla)")):
        ax.plot(HOURS, result[key], marker="o", label=label)
    ax.set(xlabel="Hora", ylabel="Valor normalizado", title="Variables de entrada del modelo", ylim=(0, 1.05))
    _save(fig, ax, path)


def plot_contributions(result, weights, title, path):
    """Términos ponderados apilados: muestra cuánto aporta cada variable al índice."""
    fig, ax = plt.subplots(figsize=(8, 4))
    bottom = 0
    for weight, key in zip(weights, ("H", "N", "Tf")):
        term = weight * result[key]
        ax.bar(HOURS, term, bottom=bottom, label=f"{weight}·{key}")
        bottom = bottom + term
    _threshold_lines(ax)
    ax.set(xlabel="Hora", ylabel="Índice I", title=title, ylim=(0, 1))
    _save(fig, ax, path)


def plot_index(result, title, path):
    """Índice de un solo modelo a lo largo del día, con los umbrales de estado."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(HOURS, result["index"], marker="o", label="Índice I")
    _threshold_lines(ax)
    ax.set(xlabel="Hora", ylabel="Índice I", title=title, ylim=(0.3, 1))
    _save(fig, ax, path)


def plot_comparison(base, adjusted, path):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(HOURS, base["index"], marker="o", label="Índice original (0.5·H + 0.3·N + 0.2·Tf)")
    ax.plot(HOURS, adjusted["index"], marker="s", linestyle="--", label="Índice ajustado (0.4·H + 0.4·N + 0.2·Tf)")
    _threshold_lines(ax)
    ax.set(xlabel="Hora", ylabel="Índice I", title="Comparación del índice original y ajustado", ylim=(0.3, 1))
    _save(fig, ax, path)
