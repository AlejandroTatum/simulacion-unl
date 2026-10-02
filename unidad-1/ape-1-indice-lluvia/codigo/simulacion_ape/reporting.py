"""Console tables and figures."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .config import CLOUDINESS, HOURS, HUMIDITY, STATES, TEMPERATURE, WEIGHTS


def table(result, title):
    lines = [title, f"{'Hora':<6} {'Hum':>4} {'Nub':>4} {'Temp':>5} {'H':>5} {'N':>5} {'Tf':>5} {'I':>6}  Estado"]
    for k, hour in enumerate(HOURS):
        lines.append(
            f"{hour:<6} {HUMIDITY[k]:>4} {CLOUDINESS[k]:>4} {TEMPERATURE[k]:>5} "
            f"{result['H'][k]:>5.2f} {result['N'][k]:>5.2f} {result['Tf'][k]:>5.2f} "
            f"{result['index'][k]:>6.4f}  {result['state'][k]}"
        )
    return "\n".join(lines)


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
    """Stacked weighted terms: shows how much each variable pushes the index."""
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
    ax.plot(HOURS, adjusted["index"], marker="s", linestyle="--", label="Modelo ajustado (Tf continuo)")
    _threshold_lines(ax)
    ax.set(xlabel="Hora", ylabel="Índice I", title="Índice de lluvia durante el día", ylim=(0.3, 1))
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
