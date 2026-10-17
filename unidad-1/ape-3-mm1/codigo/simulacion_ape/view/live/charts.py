"""Vista en vivo: las tres gráficas (L(t) y Lq(t), tiempos entre llegadas, tiempos de servicio).

Solo dibuja datos que ya trae `LiveRun`; las muestras y las curvas teóricas las calcula el modelo.
Cada gráfica declara qué artistas se pintan en cada cuadro (`fast`) y cuáles cada cierto tiempo (`slow`).
"""

import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

from ...model.live import LiveRun
from .board import fmt
from .theme import EXIT, INK, MUTED, PAPER, RULE, SIGNAL

BINS = 14  # barras de cada histograma
MEANS_SHOWN = 4  # el eje x cubre 4 medias (4/λ o 4/μ): casi toda la densidad exponencial
BAR_GAP = 0.06  # margen a cada lado de una barra, como fracción de su ancho
CURVE_POINTS = 80  # puntos con los que se dibuja la curva teórica


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
    fast = ()  # no tiene artistas por cuadro
    def __init__(self, ax, title: str) -> None:
        self.ax = ax
        self.summary = _style(ax, title, "minutos")
        self.bars = ax.bar(np.arange(BINS), np.zeros(BINS), align="edge", color=RULE)
        self.curve, = ax.plot([], [], color=INK, lw=2)
        ax.legend([self.bars, self.curve], ["simulado", "exponencial teórica"], loc="upper right",
                  fontsize=8, frameon=False)
        self.rate = self.limit = 1.0  # se fijan en set_rate al cargar cada corrida
        self.slow = [*self.bars, self.summary]

    def set_rate(self, rate: float) -> None:
        """Ajusta ejes, barras y curva teórica a la tasa de la corrida (λ o μ)."""
        self.rate = rate
        self.limit = MEANS_SHOWN / rate
        width = self.limit / BINS
        for i, bar in enumerate(self.bars):
            bar.set_x((i + BAR_GAP) * width)
            bar.set_width((1 - 2 * BAR_GAP) * width)
        x = np.linspace(0, self.limit, CURVE_POINTS)
        self.curve.set_data(x, rate * np.exp(-rate * x))  # densidad exponencial: máxima en t = 0, donde vale la tasa
        self.ax.set_xlim(0, self.limit)
        self.ax.set_ylim(0, rate * 1.6)  # 60 % de aire sobre el máximo de la curva

    def update(self, samples: list[float]) -> None:
        """Redibuja las barras con las muestras vistas hasta ahora (densidad, para comparar con la curva)."""
        if samples:
            # Los valores mayores al último borde caen en la última barra.
            density, _ = np.histogram(np.clip(samples, 0, self.limit), bins=BINS, range=(0, self.limit), density=True)
        else:
            density = np.zeros(BINS)
        for bar, value in zip(self.bars, density):
            bar.set_height(value)
        mean = float(np.mean(samples)) if samples else None
        self.summary.set_text(f"media {fmt(mean, 2)}   teórica {1 / self.rate:.2f} min")


class OccupancyChart:
    """L(t) y Lq(t) simulados (escalones) con sus valores teóricos en líneas punteadas."""
    slow = ()  # no tiene artistas lentos
    def __init__(self, ax) -> None:
        self.ax = ax
        self.summary = _style(ax, "Clientes en sistema y cola", "Tiempo (min)")
        self.system, = ax.plot([], [], color=INK, lw=2, drawstyle="steps-post")
        self.queue, = ax.plot([], [], color=EXIT, lw=2, drawstyle="steps-post")
        self.theory_system = ax.axhline(0, color=INK, ls="--", lw=1.5)
        self.theory_queue = ax.axhline(0, color=EXIT, ls="--", lw=1.5)
        self.cursor = ax.axvline(0, color=SIGNAL, lw=2.5)  # minuto actual
        self.fast = [self.system, self.queue, self.cursor]
        ax.legend([self.system, self.queue, Line2D([], [], color=MUTED, ls="--")],
                  ["L(t) simulado", "Lq(t) simulado", "teórico"], loc="upper left", ncol=3, fontsize=8, frameon=False)

    def set_run(self, run: LiveRun) -> None:
        """Ejes y líneas teóricas de la corrida; con λ ≥ μ no hay valores teóricos que dibujar."""
        highest = max(run.trace.in_system.max(), run.theory.mean_in_system if run.stable else 0)
        self.ax.set_xlim(0, run.duration)
        self.ax.set_ylim(0, highest * 1.25 + 1)
        self.theory_system.set_visible(run.stable)
        self.theory_queue.set_visible(run.stable)
        if run.stable:
            self.theory_system.set_ydata([run.theory.mean_in_system] * 2)
            self.theory_queue.set_ydata([run.theory.mean_in_queue] * 2)
            self.summary.set_text(f"teórico L {run.theory.mean_in_system:.2f}   Lq {run.theory.mean_in_queue:.2f}")
        else:
            self.summary.set_text("")

    def update(self, run: LiveRun, time: float) -> None:
        """Dibuja los escalones ocurridos hasta `time` y mueve el cursor del minuto actual."""
        trace = run.trace
        known = np.searchsorted(trace.times, time, side="right")  # cambios ocurridos hasta `time`
        times = np.append(trace.times[:known], time)  # el último escalón llega hasta el minuto actual
        for line, values in ((self.system, trace.in_system), (self.queue, trace.in_queue)):
            line.set_data(times, np.append(values[:known], values[known - 1]))  # repite el último valor hasta `time`
        self.cursor.set_xdata([time, time])
