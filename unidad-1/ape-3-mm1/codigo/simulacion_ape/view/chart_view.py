"""Vista (MVC): gráficas estáticas (PNG) de la cola y de los tiempos de espera, para el informe."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ..model.analysis import occupancy_trace, running_mean_wait, wait_times
from ..model.simulation import ScenarioResult
from .console_view import METRIC_ROWS

COLORS = ("#2e9e5b", "#e8a33d", "#d64545", "#5b6cd6")
QUEUE_WINDOW = 480.0  # minutos que se grafican de la cola: una jornada de 8 horas
BAR_WIDTH = 0.4  # ancho de cada barra de la gráfica comparativa (teórico a la izquierda, simulado a la derecha)


def _color(index: int) -> str:
    return COLORS[index % len(COLORS)]


def plot_queue_over_time(results: list[ScenarioResult], path: Path) -> Path:
    """Clientes en cola durante una jornada de 8 horas, un panel por escenario, con Lq teórico."""
    fig, axes = plt.subplots(len(results), 1, figsize=(11, 2.8 * len(results)), sharex=True, squeeze=False)
    for index, (ax, result) in enumerate(zip(axes[:, 0], results)):
        window = min(QUEUE_WINDOW, result.sim_time)
        trace = occupancy_trace(result.customers, window)
        ax.step(trace.times, trace.in_queue, where="post", color=_color(index), linewidth=0.9, label="Cola simulada")
        ax.axhline(result.theory.mean_in_queue, color="black", linestyle="--", linewidth=1.2,
                   label=f"Lq teórico = {result.theory.mean_in_queue:.2f}")
        ax.set_title(f"{result.scenario.label} (ρ = {result.theory.utilization:.3f})", loc="left", fontsize=10)
        ax.set_ylabel("Clientes en cola")
        ax.legend(loc="upper left", fontsize=8)
        ax.grid(alpha=0.3)
    axes[-1, 0].set_xlabel("Tiempo (min)")
    fig.suptitle("Tamaño de la cola durante una jornada de 8 horas")
    return _save(fig, path)


def plot_running_wait(results: list[ScenarioResult], path: Path) -> Path:
    """Espera promedio acumulada cliente a cliente: por la ley de los grandes números tiende a Wq."""
    fig, ax = plt.subplots(figsize=(11, 5))
    for index, result in enumerate(results):
        running = running_mean_wait(result.customers)
        ax.plot(np.arange(1, len(running) + 1), running, color=_color(index), linewidth=1.2,
                label=f"Escenario {result.scenario.number} simulado")
        ax.axhline(result.theory.mean_wait, color=_color(index), linestyle="--", linewidth=1,
                   label=f"Wq teórico = {result.theory.mean_wait:.2f} min")
    ax.set_xscale("log")
    ax.set_xlabel("Clientes atendidos (escala logarítmica)")
    ax.set_ylabel("Espera promedio acumulada (min)")
    ax.set_title("Convergencia del tiempo promedio de espera en cola hacia Wq")
    # Una columna por escenario: Matplotlib llena la leyenda por columnas, así cada simulado queda sobre su Wq.
    ax.legend(fontsize=8, ncol=len(results))
    ax.grid(alpha=0.3, which="both")
    return _save(fig, path)


def plot_wait_histogram(results: list[ScenarioResult], path: Path) -> Path:
    """Histograma de los tiempos de espera de cada escenario con Wq teórico."""
    fig, axes = plt.subplots(1, len(results), figsize=(4.2 * len(results), 4), squeeze=False)
    for index, (ax, result) in enumerate(zip(axes[0], results)):
        ax.hist(wait_times(result.customers), bins=40, color=_color(index), alpha=0.85)
        ax.axvline(result.theory.mean_wait, color="black", linestyle="--", label=f"Wq = {result.theory.mean_wait:.2f}")
        ax.set_title(result.scenario.label, fontsize=10)
        ax.set_xlabel("Espera en cola (min)")
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)
    axes[0, 0].set_ylabel("Clientes")
    fig.suptitle("Distribución de los tiempos de espera")
    return _save(fig, path)


def plot_wait_scatter(results: list[ScenarioResult], path: Path) -> Path:
    """Diagrama de dispersión: espera de cada cliente según su orden de llegada, un panel por escenario.

    Cada punto es un cliente que ya pasó a la caja; se grafican todos (sin submuestreo) con puntos pequeños y
    transparentes. Cada panel tiene su propia escala vertical porque las esperas del escenario 3 son mucho
    mayores que las de los otros dos. La línea punteada marca el Wq teórico.
    """
    fig, axes = plt.subplots(len(results), 1, figsize=(11, 2.8 * len(results)), squeeze=False)
    for index, (ax, result) in enumerate(zip(axes[:, 0], results)):
        waits = wait_times(result.customers)
        ax.scatter(np.arange(1, len(waits) + 1), waits, s=2, alpha=0.3, color=_color(index),
                   linewidths=0, rasterized=True)
        ax.axhline(result.theory.mean_wait, color="black", linestyle="--", linewidth=1.2,
                   label=f"Wq teórico = {result.theory.mean_wait:.2f} min")
        ax.set_title(f"{result.scenario.label} (ρ = {result.theory.utilization:.3f})", loc="left", fontsize=10)
        ax.set_ylabel("Espera en cola (min)")
        ax.set_ylim(bottom=0)
        ax.legend(loc="upper right", fontsize=8)
        ax.grid(alpha=0.3)
    axes[-1, 0].set_xlabel("Cliente (orden de llegada)")
    fig.suptitle("Espera en cola de cada cliente según su orden de llegada")
    return _save(fig, path)


def plot_comparison(results: list[ScenarioResult], path: Path) -> Path:
    """Una gráfica de barras por métrica: teórico frente a simulado en cada escenario."""
    fig, axes = plt.subplots(1, len(METRIC_ROWS), figsize=(16, 4))
    positions = np.arange(len(results))
    for ax, (label, field) in zip(axes, METRIC_ROWS):
        theory = [getattr(result.theory, field) for result in results]
        simulated = [getattr(result.simulated, field) for result in results]
        ax.bar(positions - BAR_WIDTH / 2, theory, width=BAR_WIDTH, color="#9aa5b1", label="Teórico")
        ax.bar(positions + BAR_WIDTH / 2, simulated, width=BAR_WIDTH, color="#1f6feb", label="Simulado")
        ax.set_xticks(positions, [f"E{result.scenario.number}" for result in results])
        ax.set_title(label.split()[0], fontsize=12)  # solo el símbolo: ρ, L, Lq, W o Wq
        ax.grid(alpha=0.3, axis="y")
    axes[0].legend(fontsize=8)
    fig.suptitle("Comparación teórico vs. simulado por escenario")
    return _save(fig, path)


def save_charts(results: list[ScenarioResult], output_dir: Path) -> list[Path]:
    """Genera las cinco gráficas en `output_dir` y devuelve sus rutas."""
    output_dir.mkdir(parents=True, exist_ok=True)
    return [
        plot_queue_over_time(results, output_dir / "cola_en_el_tiempo.png"),
        plot_running_wait(results, output_dir / "convergencia_espera.png"),
        plot_wait_histogram(results, output_dir / "histograma_espera.png"),
        plot_wait_scatter(results, output_dir / "dispersion_espera.png"),
        plot_comparison(results, output_dir / "comparacion_teorico_simulado.png"),
    ]


def _save(fig, path: Path) -> Path:
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
