"""Vista de gráficas: figuras de matplotlib guardadas en archivos."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from ..model.config import CLOUDINESS, HOURS, HUMIDITY, STATES, TEMPERATURE, WEIGHTS


def _threshold_lines(ax):
    for bound, state in STATES:
        ax.axhline(bound, color="gray", linestyle="--", linewidth=0.8)
        ax.text(1.01, bound, state, transform=ax.get_yaxis_transform(), va="center", fontsize=8, color="gray")


def plot_inputs(result, path):
    fig, ax = plt.subplots(figsize=(8, 4))
    for key, label in (("H", "Humedad H"), ("N", "Nubosidad N"), ("Tf", "Factor de temperatura Tf")):
        ax.plot(HOURS, result[key], marker="o", label=label)
    ax.set(xlabel="Hora", ylabel="Valor normalizado", title="Variables de entrada del modelo", ylim=(0, 1.05))
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_contributions(result, path):
    """Términos ponderados apilados: muestra cuánto aporta cada variable al índice."""
    fig, ax = plt.subplots(figsize=(8, 4))
    bottom = 0
    for weight, key, label in zip(WEIGHTS, ("H", "N", "Tf"), ("0.5·H", "0.3·N", "0.2·Tf")):
        term = weight * result[key]
        ax.bar(HOURS, term, bottom=bottom, label=label)
        bottom = bottom + term
    _threshold_lines(ax)
    ax.set(xlabel="Hora", ylabel="Índice I", title="Aporte de cada variable al índice (modelo base)", ylim=(0, 1))
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_comparison(base, adjusted, path):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(HOURS, base["index"], marker="o", label="Modelo base (tabla)")
    ax.plot(HOURS, adjusted["index"], marker="s", linestyle="--", label="Modelo ajustado (0.4·H + 0.4·N + 0.2·Tf)")
    _threshold_lines(ax)
    ax.set(xlabel="Hora", ylabel="Índice I", title="Índice de lluvia durante el día", ylim=(0.3, 1))
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
