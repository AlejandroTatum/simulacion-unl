"""Animación del local: fila serpentina, caja y salida. Solo dibuja lo que le entrega `LiveRun`."""

import math
from functools import lru_cache

import numpy as np
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.colors import to_rgba
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Circle, Rectangle
from matplotlib.textpath import TextPath
from matplotlib.transforms import IdentityTransform

from ...model.live import LiveRun
from ...model.state import SystemState
from .theme import ALERT, EXIT, FLOOR, INK, PAPER, SIGNAL

# Plano del local en unidades de dibujo (1900 × 1000); el eje y crece hacia abajo, como en pantalla.
WIDTH, HEIGHT = 1900, 1000
ROWS_Y = (850, 670, 490, 310)
QUEUE_LEFT, QUEUE_RIGHT = 230, 1190
PER_ROW = 10
SERVICE = (1520, 850)  # donde se para el cliente que atiende la caja
EXIT_POINT = (1860, 850)
EXIT_WINDOW = 0.8  # minutos que se ve a un cliente caminar hacia la salida
PT = 0.3  # puntos de tipografía por unidad de dibujo

# Pictograma: cada pose son 5 trazos (tronco, 2 brazos, 2 piernas) como (x1, y1, x2, y2) con el origen en los pies.
STAND = ((0, -98, 0, -56), (-12, -95, -20, -56), (12, -95, 20, -56), (-7, -50, -8, -5), (7, -50, 8, -5))
WALK_A = ((1, -98, 1, -56), (-10, -94, -24, -62), (12, -94, 24, -60), (-4, -50, -21, -6), (5, -50, 19, -7))
WALK_B = ((1, -98, 1, -56), (-10, -94, -17, -56), (12, -94, 17, -56), (-3, -50, -9, -5), (4, -50, 6, -5))
STROKE_UNITS = (30, 10, 10, 13, 13)  # grosor de cada trazo, en unidades de dibujo
HEAD_AREA = (32 * PT) ** 2  # área del círculo de la cabeza, en puntos²
CAPACITY = PER_ROW * len(ROWS_Y)  # clientes que caben dibujados en la fila; el resto se cuenta en el letrero
ARRIVAL_WINDOW = 1.0  # minutos tras llegar en los que un cliente nuevo entra caminando por la izquierda
INK_RGBA, EXIT_RGBA = to_rgba(INK), to_rgba(EXIT)
LABEL_FONT = FontProperties(weight="bold")


def queue_spot(position: int) -> tuple[float, float]:
    """Lugar en la fila serpentina: las filas pares avanzan hacia la caja y las impares regresan."""
    row, column = divmod(min(position, CAPACITY - 1), PER_ROW)
    step = (QUEUE_RIGHT - QUEUE_LEFT) / (PER_ROW - 1)
    x = QUEUE_RIGHT - column * step if row % 2 == 0 else QUEUE_LEFT + column * step
    return x, ROWS_Y[row]


@lru_cache(maxsize=None)
def label_path(customer_id: int):
    """Número del cliente como trazo vectorial (en puntos), centrado en x y con la línea base en y = 0.

    Dibujar 40 números como `Text` costaba ~1 ms cada uno por cuadro; como trazos van en una sola colección.
    """
    path = TextPath((0, 0), str(customer_id), size=19 * PT, prop=LABEL_FONT)
    box = path.get_extents()
    return TextPath((-(box.x0 + box.x1) / 2, 0), str(customer_id), size=19 * PT, prop=LABEL_FONT)


def _text(ax, x, y, content, size, color, weight="normal", ha="left", **kwargs):
    return ax.text(x, y, content, fontsize=size * PT, color=color, fontweight=weight, ha=ha, va="baseline", **kwargs)


def _line(ax, x, y, width, color, **kwargs):
    ax.plot(x, y, color=color, lw=width * PT, solid_capstyle="round", **kwargs)


def _sign(ax, x, y, width, height, color, label):
    ax.add_patch(Rectangle((x, y), width, height, color=color))
    _text(ax, x + 22, y + height * 0.68, label, height * 0.5, "white", "bold")
    arrow_x, arrow_y = x + width - 58, y + height / 2
    _line(ax, [arrow_x, arrow_x + 36], [arrow_y, arrow_y], 8, "white")
    _line(ax, [arrow_x + 22, arrow_x + 37, arrow_x + 22], [arrow_y - 15, arrow_y, arrow_y + 15], 8, "white")


def _draw_cart(ax) -> None:
    """Carrito de compras del letrero, ampliado ×2 desde su esquina (1365, 95)."""
    path = [(4, 7), (9, 7), (13.5, 26), (30.5, 26), (35, 13), (11.3, 13)]
    _line(ax, [1365 + 2 * x for x, _ in path], [95 + 2 * y for _, y in path], 6.8, INK)
    for wheel_x in (15, 29):
        ax.add_patch(Circle((1365 + 2 * wheel_x, 95 + 66), 5.2, color=INK))


def _draw_store(ax) -> None:
    """Parte fija del local: piso, cintas separadoras, letreros y mostrador."""
    ax.add_patch(Rectangle((0, 900), WIDTH, 100, color=FLOOR))
    # Cintas separadoras: poste, cinta y poste; el paso libre alterna de lado en cada fila.
    left, right = QUEUE_LEFT - 70, QUEUE_RIGHT + 70
    for y, x1, x2 in ((890, left, right), (690, left + 120, right), (510, left, right - 120), (330, left + 120, right)):
        _line(ax, [x1, x2], [y, y], 5, INK, alpha=0.75)
        for x in (x1, (x1 + x2) / 2, x2):
            _line(ax, [x, x], [y - 12, y + 12], 9, INK)
    _text(ax, QUEUE_RIGHT + 40, 962, "ESPERE SU TURNO", 28, INK, "bold", "right")
    ax.add_patch(Rectangle((QUEUE_RIGHT + 70, 902), 12, 80, color=SIGNAL))
    ax.add_patch(Rectangle((SERVICE[0] - 70, 902), 140, 16, color=SIGNAL))
    _text(ax, SERVICE[0], 962, "PASE", 28, INK, "bold", "center")

    # Letrero colgante de la caja.
    for x in (1395, 1815):
        _line(ax, [x, x], [0, 60], 4, INK)
    ax.add_patch(Rectangle((1330, 60), 550, 150, color=INK))
    ax.add_patch(Rectangle((1352, 82), 106, 106, color=SIGNAL))
    _draw_cart(ax)
    _text(ax, 1482, 140, "Caja rápida", 52, "white", "bold")
    _text(ax, 1484, 184, "Hasta 10 artículos", 30, "#c5cad0")

    # Mostrador con la cajera detrás; el cliente atendido se para delante.
    for (a, b, c, d), width in zip(STAND, STROKE_UNITS):  # cajera
        _line(ax, [1560 + a, 1560 + c], [770 + b, 770 + d], width, INK)
    ax.add_patch(Circle((1560, 646), 16, color=INK))
    ax.add_patch(Rectangle((1400, 690), 280, 110, fc="#cdd3d9", ec=INK, lw=6 * PT, zorder=3))
    ax.add_patch(Rectangle((1403, 693), 274, 14, color=SIGNAL, zorder=3))
    ax.add_patch(Rectangle((1610, 628), 58, 44, color=INK, zorder=3))
    _line(ax, [1420, 1420], [520, 690], 8, INK)  # poste de la lámpara de carril

    _sign(ax, 22, 30, 250, 74, INK, "Entrada")
    _sign(ax, 1660, 420, 220, 70, EXIT, "Salida")


class Scene:
    def __init__(self, ax) -> None:
        self.ax = ax
        ax.set_xlim(0, WIDTH)
        ax.set_ylim(HEIGHT, 0)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.add_patch(Rectangle((0, 0), WIDTH, HEIGHT, color=PAPER, zorder=-2))
        _draw_store(ax)

        # Elementos que cambian. Se crean una sola vez y se reutilizan: nada se crea ni se quita por cuadro.
        self.params = _text(ax, 300, 76, "", 28, INK, "bold")  # cambia solo al cargar otra corrida
        self.lamp = ax.add_patch(Circle((1420, 500), 30, fc=EXIT, ec=INK, lw=7 * PT))
        ax.add_patch(Rectangle((1330, 232), 550, 22, fc="white", ec=INK, lw=4 * PT))
        self.progress = ax.add_patch(Rectangle((1332, 234), 0, 18, color=SIGNAL))
        self.progress_label = _text(ax, 1330, 296, "", 30, INK, "bold")
        self.overflow = _text(ax, 40, 962, "", 30, SIGNAL, "bold", bbox=dict(fc=INK, ec="none", pad=12), visible=False)
        self.alert = _text(ax, 300, 148, "", 30, "white", "bold", bbox=dict(fc=ALERT, ec="none", pad=8), visible=False)
        self.bodies = ax.add_collection(LineCollection([], capstyle="round", zorder=5))
        self.heads = ax.scatter([], [], s=HEAD_AREA, linewidths=0, zorder=6)
        self.labels = ax.add_collection(PathCollection([], sizes=[1.0], facecolors="white", edgecolors="none",
                                                       offset_transform=ax.transData, zorder=7))
        self.labels.set_transform(IdentityTransform())  # los trazos están en puntos; solo el desplazamiento usa `transData`
        # Se dibujan cada cuadro (fast) o cada cierto tiempo (slow); el resto queda en el fondo de la ventana.
        self.fast = [self.lamp, self.progress, self.progress_label, self.bodies, self.heads, self.labels]
        self.slow = [self.overflow, self.alert]
        self.positions: dict[int, list[float]] = {}
        self.frame = 0

    def set_run(self, run: LiveRun) -> None:
        """Texto fijo de la corrida (λ, μ y ρ)."""
        params = f"λ = {run.arrival_rate:.1f} llegadas/min    μ = {run.service_rate:.1f} atenciones/min"
        if run.stable:
            params += f"    ρ = λ/μ = {run.theory.utilization:.3f}"
        self.params.set_text(params)

    def reset(self) -> None:
        """Vacía el local (al cambiar λ o μ, o al reiniciar)."""
        self.positions.clear()

    def update(self, run: LiveRun, state: SystemState, speed: float, dt: float) -> None:
        """Lo que se mueve en cada cuadro: personas, lámpara y barra de la caja."""
        self.frame += 1
        self._update_people(run, state, speed, dt)
        self._update_register(run, state)

    def _update_people(self, run: LiveRun, state: SystemState, speed: float, dt: float) -> None:
        # Solo caben CAPACITY personas en la serpentina: las demás se cuentan en el letrero de `update_notices`.
        targets = {cid: queue_spot(place) for place, cid in enumerate(state.waiting[:CAPACITY])}
        if state.in_service is not None:
            targets[state.in_service] = SERVICE
        for cid in state.leaving:
            progress = min((state.time - run.customers[cid - 1].departure) / EXIT_WINDOW, 1)
            targets[cid] = (SERVICE[0] + (EXIT_POINT[0] - SERVICE[0]) * progress, SERVICE[1])
        for cid in [cid for cid in self.positions if cid not in targets]:  # ya salieron (o volvieron al exterior)
            del self.positions[cid]

        ease = 1 - math.exp(-dt * 7 * max(1, speed))  # cada persona recorre una fracción del camino por cuadro
        walking = (WALK_A, WALK_B)[self.frame // 2 % 2]
        segments, colors, head_xy, head_colors, label_ids, label_xy = [], [], [], [], [], []
        for cid, (tx, ty) in targets.items():
            leaving = cid in state.leaving
            pos = self.positions.get(cid)
            if pos is None:
                # Quien acaba de llegar entra por la izquierda; quien estaba fuera de la fila aparece en su lugar.
                fresh = state.time - run.customers[cid - 1].arrival < ARRIVAL_WINDOW
                pos = self.positions[cid] = [-90.0, ty] if fresh else [tx, ty]
            if leaving:
                pos[:] = [tx, ty]
            else:
                pos[0] += (tx - pos[0]) * ease
                pos[1] += (ty - pos[1]) * ease
            moving = leaving or math.hypot(tx - pos[0], ty - pos[1]) > 3
            pose = walking if moving else STAND
            if leaving:  # se desvanece al llegar a la salida
                alpha = max(0.0, min(1.0, (1 - (pos[0] - SERVICE[0]) / (EXIT_POINT[0] - SERVICE[0])) / 0.35))
                color = EXIT_RGBA[:3] + (alpha,)
            else:
                color = INK_RGBA
            x, y = pos
            segments += [((x + a, y + b), (x + c, y + d)) for a, b, c, d in pose]
            colors += [color] * len(pose)
            head_xy.append((x, y - 124))
            head_colors.append(color)
            if not leaving:
                label_ids.append(cid)
                label_xy.append((x + 1, y - 68))

        self.bodies.set_segments(segments)
        self.bodies.set_color(colors)
        self.bodies.set_linewidth([w * PT for w in STROKE_UNITS] * len(targets))
        self.heads.set_offsets(np.array(head_xy).reshape(-1, 2))
        self.heads.set_facecolor(head_colors)
        self.labels.set_paths([label_path(cid) for cid in label_ids])
        self.labels.set_offsets(np.array(label_xy).reshape(-1, 2))

    def _update_register(self, run: LiveRun, state: SystemState) -> None:
        busy = state.in_service is not None
        self.lamp.set_facecolor(SIGNAL if busy else EXIT)
        if busy:
            record = run.customers[state.in_service - 1]
            end = run.duration if record.departure is None else record.departure
            fraction = min((state.time - record.service_start) / (end - record.service_start), 1) if end > record.service_start else 1
            self.progress_label.set_text(f"Cobrando al cliente {state.in_service}")
        else:
            fraction = 0
            self.progress_label.set_text("Esperando cliente")
        self.progress.set_width(546 * fraction)

    def update_notices(self, run: LiveRun, state: SystemState) -> None:
        """Letreros que cambian poco: clientes fuera de la fila y aviso rojo de saturación."""
        hidden = len(state.waiting) - CAPACITY  # clientes que ya no caben dibujados en la fila
        self.overflow.set_visible(hidden > 0)
        self.overflow.set_text(f"+{max(hidden, 0)} esperando fuera de la fila")
        # Aviso rojo: sistema inestable, o cola larga con ρ alto.
        if not run.stable:
            message = "Sistema inestable: λ ≥ μ, la teoría no aplica"
        elif len(state.waiting) >= 12 and run.theory.utilization >= 0.9:
            message = f"ρ = {run.theory.utilization:.3f}: la cola crece"
        else:
            message = ""
        self.alert.set_visible(bool(message))
        self.alert.set_text(message)
