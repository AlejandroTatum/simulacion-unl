"""Vista de gráficas: figuras de matplotlib guardadas en archivos."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

STYLES = {
    "Determinístico": {"linestyle": "-"},
    "Discreto": {"linestyle": "none", "marker": "s"},
    "Estocástico": {"linestyle": ":", "marker": "^"},
    "Continuo (Euler)": {"linestyle": "--"},
}


def _finish(fig, ax, title, path, xlabel="Tiempo t", ylabel="Población P"):
    """Título, ejes, leyenda y cuadrícula, como pide la guía, y guardado del archivo."""
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(True, alpha=0.4)
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_models(results, data, title, path, data_label="Datos de la guía"):
    """Los cuatro modelos sobre los datos observados."""
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot(np.arange(len(data)), data, "ko", markersize=7, label=data_label)
    for name, (t, population) in results.items():
        ax.plot(t, population, label=name, **STYLES[name])
    _finish(fig, ax, title, path)


def plot_rate_influence(curves, path):
    """Curvas P0 · e^(r·t) para varios r: crecimiento, equilibrio y decrecimiento."""
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for r, (t, population) in curves.items():
        style = "-" if r > 0 else ("--" if r < 0 else ":")
        ax.plot(t, population, style, label=f"r = {r:+.2f}")
    _finish(fig, ax, "Influencia de la tasa r en el modelo determinístico", path)


def plot_noise_influence(bands, path):
    """Un panel por nivel de ruido: algunas corridas, la media y la banda del 5 % al 95 %."""
    fig, axes = plt.subplots(2, 2, figsize=(9, 5), sharex=True, sharey=True)
    for ax, (sigma, band) in zip(axes.flat, bands.items()):
        t = np.arange(band["mean"].size)
        for path_ in band["paths"][:15]:
            ax.plot(t, path_, color="tab:blue", alpha=0.25, linewidth=0.8)
        ax.fill_between(t, band["p5"], band["p95"], color="tab:orange", alpha=0.25, label="Banda 5 %–95 %")
        ax.plot(t, band["mean"], color="tab:red", linewidth=2, label="Media")
        ax.set_title(f"σ = {sigma}", fontsize=10)
        ax.grid(True, alpha=0.4)
    axes[0, 0].legend(loc="upper left", fontsize=8)
    for ax in axes[1]:
        ax.set_xlabel("Tiempo t")
    for ax in axes[:, 0]:
        ax.set_ylabel("Población P")
    fig.suptitle("Influencia del ruido σ en el modelo estocástico")
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_step_influence(exact, approximations, path):
    """Solución exacta frente a Euler con distintos pasos dt."""
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot(*exact, "k-", linewidth=2, label="Exacta P0 · e^(r·t)")
    for dt, (t, population) in approximations.items():
        ax.plot(t, population, "--", marker="o" if dt >= 0.5 else None, markersize=4, label=f"Euler dt = {dt}")
    _finish(fig, ax, "Influencia del paso dt en el modelo continuo", path)
