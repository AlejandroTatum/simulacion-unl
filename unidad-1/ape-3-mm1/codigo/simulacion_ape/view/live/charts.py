"""Las tres gráficas en vivo: L(t) y Lq(t), tiempos entre llegadas y tiempos de servicio."""

import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from ...model.live import LiveRun
from .board import fmt
from .theme import EXIT, INK, MUTED, PAPER, RULE, SIGNAL

BINS = 14


def _style(ax, title: str, xlabel: str):
    """Fondo claro, barra de título oscura y, a su derecha, un texto que se actualiza (valores teóricos o medias)."""
    ax.set_facecolor(PAPER)
    ax.tick_params(labelsize=8, colors=MUTED, length=3)
    ax.set_xlabel(xlabel, fontsize=8, color=MUTED, loc="right")
    ax.grid(axis="y", color="#e1e5e9", lw=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_linewidth(2)
    ax.add_patch(Rectangle((0, 1), 1, 0.2, transform=ax.transAxes, color=INK, clip_on=False))
    ax.text(0.015, 1.1, title, transform=ax.transAxes, color="white", fontsize=10, fontweight="bold", va="center")
    return ax.text(0.985, 1.1, "", transform=ax.transAxes, color="#c5cad0", fontsize=8, ha="right", va="center")


class Histogram:
    """Barras de las muestras observadas hasta el minuto actual y la densidad exponencial teórica λe^(−λt)."""

    def __init__(self, ax, title: str) -> None:
        self.ax = ax
        self.summary = _style(ax, title, "minutos")
        self.bars = ax.bar(np.arange(BINS), np.zeros(BINS), align="edge", color=RULE)
        self.curve, = ax.plot([], [], color=INK, lw=2)
        ax.legend([self.bars, self.curve], ["simulado", "exponencial teórica"], loc="upper right",
                  fontsize=8, frameon=False)
        self.rate = 1.0
        self.slow = [*self.bars, self.summary]  # se dibujan cada cierto tiempo; el resto queda en el fondo

    def set_rate(self, rate: float) -> None:
        self.rate = rate
        limit = 4 / rate  # 4 medias cubren casi toda la densidad exponencial
        width = limit / BINS
        for i, bar in enumerate(self.bars):
            bar.set_x(i * width + width * 0.06)
            bar.set_width(width * 0.88)
        x = np.linspace(0, limit, 80)
        self.curve.set_data(x, rate * np.exp(-rate * x))
        self.ax.set_xlim(0, limit)
        self.ax.set_ylim(0, rate * 1.6)

    def update(self, samples: list[float]) -> None:
        limit = 4 / self.rate
        if samples:
            # Los valores mayores al último borde caen en la última barra.
            density, _ = np.histogram(np.clip(samples, 0, limit), bins=BINS, range=(0, limit), density=True)
        else:
            density = np.zeros(BINS)
        for bar, value in zip(self.bars, density):
            bar.set_height(value)
        mean = float(np.mean(samples)) if samples else None
        self.summary.set_text(f"media {fmt(mean, 2)}   teórica {1 / self.rate:.2f} min")


class OccupancyChart:
    """L(t) y Lq(t) simulados (escalones) con sus valores teóricos en líneas punteadas."""

    def __init__(self, ax) -> None:
        self.ax = ax
        self.summary = _style(ax, "Clientes en sistema y cola", "Tiempo (min)")
        self.system, = ax.plot([], [], color=INK, lw=2, drawstyle="steps-post")
        self.queue, = ax.plot([], [], color=EXIT, lw=2, drawstyle="steps-post")
        self.theory_system = ax.axhline(0, color=INK, ls="--", lw=1.5)
        self.theory_queue = ax.axhline(0, color=EXIT, ls="--", lw=1.5)
        self.cursor = ax.axvline(0, color=SIGNAL, lw=2.5)  # minuto actual
        self.fast = [self.system, self.queue, self.cursor]  # se dibujan cada cuadro; el resto queda en el fondo
        ax.legend([self.system, self.queue, Line2D([], [], color=MUTED, ls="--")],
                  ["L(t) simulado", "Lq(t) simulado", "teórico"], loc="upper left", ncol=3, fontsize=8, frameon=False)

    def set_run(self, run: LiveRun) -> None:
        highest = max(run.trace.in_system.max(), run.theory.mean_in_system if run.stable else 0)
        self.ax.set_xlim(0, run.duration)
        self.ax.set_ylim(0, highest * 1.25 + 1)
        self.theory_system.set_visible(run.stable)  # con λ ≥ μ no hay valor teórico que dibujar
        self.theory_queue.set_visible(run.stable)
        if run.stable:
            self.theory_system.set_ydata([run.theory.mean_in_system] * 2)
            self.theory_queue.set_ydata([run.theory.mean_in_queue] * 2)
            self.summary.set_text(f"teórico L {run.theory.mean_in_system:.2f}   Lq {run.theory.mean_in_queue:.2f}")
        else:
            self.summary.set_text("")

    def update(self, run: LiveRun, time: float) -> None:
        trace = run.trace
        known = np.searchsorted(trace.times, time, side="right")  # cambios ocurridos hasta `time`
        times = np.append(trace.times[:known], time)  # el último escalón llega hasta el minuto actual
        for line, values in ((self.system, trace.in_system), (self.queue, trace.in_queue)):
            line.set_data(times, np.append(values[:known], values[known - 1]))
        self.cursor.set_xdata([time, time])


class LiveCharts:
    def __init__(self, ax_occupancy, ax_arrivals, ax_service) -> None:
        self.occupancy = OccupancyChart(ax_occupancy)
        self.arrivals = Histogram(ax_arrivals, "Tiempo entre llegadas")
        self.service = Histogram(ax_service, "Tiempo de servicio")
        self.fast = self.occupancy.fast
        self.slow = [*self.arrivals.slow, *self.service.slow]

    def set_run(self, run: LiveRun) -> None:
        self.occupancy.set_run(run)
        self.arrivals.set_rate(run.arrival_rate)
        self.service.set_rate(run.service_rate)

    def update(self, run: LiveRun, time: float) -> None:
        """L(t), Lq(t) y el cursor del minuto actual: avanzan con cada cuadro."""
        self.occupancy.update(run, time)

    def update_histograms(self, run: LiveRun, time: float) -> None:
        """Histogramas: recalcularlos recorre todos los clientes, así que se hace cada cierto tiempo."""
        self.arrivals.update(run.interarrival_times(time))
        self.service.update(run.service_times(time))
