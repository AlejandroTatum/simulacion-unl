"""Vista en vivo: tablero oscuro con reloj, estado de la caja, contadores y la tabla teórico vs. simulado.

Solo muestra los valores que recibe del modelo (`LiveRun`, `SystemState`); no calcula métricas.
"""

import math

from matplotlib.patches import Rectangle

from ...model.live import LiveRun
from ...model.state import SystemState
from ...model.theory import QueueMetrics
from .theme import BOARD_CELL, BOARD_CELL_LIVE, BOARD_LABEL, BOARD_RULE, EXIT, INK, SIGNAL, hide_frame

# (campo de QueueMetrics, símbolo, nombre)
METRICS = (
    ("utilization", "ρ", "Utilización de la caja"),
    ("mean_in_system", "L", "Clientes en el sistema"),
    ("mean_in_queue", "Lq", "Clientes en la cola"),
    ("mean_time_in_system", "W", "Minutos en el sistema"),
    ("mean_wait", "Wq", "Minutos de espera en cola"),
)
COUNTERS = ("En cola", "En el sistema", "Atendidos", "Llegaron")
# Coordenadas del tablero: el eje va de 0 a 1 en x y en y, con y creciendo hacia abajo.
LEFT, RIGHT = 0.04, 0.96  # márgenes de las líneas separadoras
COUNTER_STEP = 0.235  # separación horizontal entre contadores
COLUMNS = (0.62, 0.80, 0.98)  # borde derecho de las columnas: teórico, simulado ahora, corrida larga
ROW_Y = [0.62 + 0.085 * i for i in range(len(METRICS))]
LIVE_COLUMN = 1  # índice de la columna "Simulado ahora", la única que cambia durante la reproducción


def fmt(value: float | None, digits: int = 3) -> str:
    """Valor con `digits` decimales; "—" si la métrica no existe o aún no tiene datos."""
    return "—" if value is None or math.isnan(value) else f"{value:.{digits}f}"


class Board:
    """Tablero dibujado con textos de Matplotlib; guarda cada texto para cambiarlo sin recrearlo."""

    def __init__(self, ax) -> None:
        self.ax = ax
        ax.set_xlim(0, 1)
        ax.set_ylim(1, 0)  # y crece hacia abajo
        ax.set_facecolor(INK)
        hide_frame(ax)

        # Franja superior: reloj, minutos totales y lámpara de la caja.
        self.clock = self._text(LEFT, 0.12, "0.0", 34, "white", "bold")
        self.clock_total = self._text(0.31, 0.12, "", 13, BOARD_LABEL, "bold")
        self.lamp = ax.plot([0.625], [0.085], "o", ms=10, color=EXIT)[0]
        self.lamp_text = self._text(0.66, 0.105, "CAJA LIBRE", 11, "white", "bold")

        ax.plot([LEFT, RIGHT], [0.2, 0.2], color=BOARD_RULE, lw=1.5)
        self.counters = []
        for i, label in enumerate(COUNTERS):
            x = LEFT + COUNTER_STEP * i
            self._text(x, 0.26, label, 9.5, BOARD_LABEL)
            self.counters.append(self._text(x, 0.375, "0", 28, SIGNAL if i == 0 else "white", "bold"))
        ax.plot([LEFT, RIGHT], [0.43, 0.43], color=BOARD_RULE, lw=1.5)

        # Tabla: una fila por métrica y tres columnas (teórico, simulado ahora, corrida larga).
        self._text(LEFT, 0.515, "Métrica", 9, BOARD_LABEL, "bold")
        headers = [self._text(x, 0.515, name, 8.5, color, "bold", "right", linespacing=1.1)
                   for x, name, color in zip(COLUMNS, ("Teórico", "Simulado\nahora", ""), (BOARD_LABEL, SIGNAL, BOARD_LABEL))]
        self.long_run_header = headers[2]  # su texto ("20 000 min") depende de la corrida
        self.cells: dict[str, list] = {}  # campo -> textos de las tres columnas
        for y, (field, symbol, name) in zip(ROW_Y, METRICS):
            self._text(LEFT, y, symbol, 17, SIGNAL, "bold", style="italic")
            self._text(0.13, y, name, 8.5, "#d8dce0")
            row = []
            for i, x in enumerate(COLUMNS):
                live = i == LIVE_COLUMN
                ax.add_patch(Rectangle((x - 0.13, y - 0.062), 0.135, 0.078, color=BOARD_CELL_LIVE if live else BOARD_CELL))
                row.append(self._text(x - 0.01, y, "—", 14, SIGNAL if live else "white", "bold", "right"))
            self.cells[field] = row
        # Capas del blitting (ver window.py): `fast` se pinta en cada cuadro, `slow` cada cierto tiempo.
        self.fast = [self.clock, self.lamp, self.lamp_text, *self.counters]
        self.slow = [cells[LIVE_COLUMN] for cells in self.cells.values()]

    def _text(self, x, y, content, size, color, weight="normal", ha="left", **kwargs):
        return self.ax.text(x, y, content, fontsize=size, color=color, fontweight=weight, ha=ha, va="baseline", **kwargs)

    def set_run(self, run: LiveRun) -> None:
        """Valores que no cambian durante la reproducción: columnas teórica y de la corrida larga."""
        self.clock_total.set_text(f"de {run.duration:g} min")
        minutes = f"{run.long_run_minutes:,.0f}".replace(",", "\u00a0")  # espacio fijo: "20 000" no se parte
        self.long_run_header.set_text(f"{minutes} min" if run.stable else "")
        for field, (theory, _, long_run) in self.cells.items():
            theory.set_text(fmt(getattr(run.theory, field) if run.stable else None))
            long_run.set_text(fmt(getattr(run.long_run, field) if run.stable else None))

    def update(self, state: SystemState) -> None:
        """Reloj, estado de la caja y contadores: cambian con cada cuadro."""
        self.clock.set_text(f"{state.time:.1f}")
        busy = state.in_service is not None
        self.lamp.set_color(SIGNAL if busy else EXIT)
        self.lamp_text.set_text("ATENDIENDO" if busy else "CAJA LIBRE")
        in_system = len(state.waiting) + busy  # quien está en la caja también está en el sistema
        for text, value in zip(self.counters, (len(state.waiting), in_system, state.served, state.arrived)):
            text.set_text(str(value))

    def update_live(self, live: QueueMetrics | None) -> None:
        """Columna "Simulado ahora": métricas calculadas solo con lo ocurrido hasta el minuto actual."""
        for field, cells in self.cells.items():
            cells[LIVE_COLUMN].set_text(fmt(getattr(live, field) if live else None))
