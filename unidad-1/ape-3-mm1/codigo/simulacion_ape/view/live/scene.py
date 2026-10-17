"""Vista en vivo: animación del local (fila serpentina, caja y salida).

Solo dibuja lo que le entrega `LiveRun`; no decide quién espera ni cuándo termina cada cobro.
"""

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
CAPACITY = PER_ROW * len(ROWS_Y)  # clientes que caben dibujados en la fila; el resto se cuenta en el letrero
SERVICE = (1520, 850)  # donde se para el cliente que atiende la caja
EXIT_POINT = (1860, 850)
EXIT_WINDOW = 0.8  # minutos que se ve a un cliente caminar hacia la salida
ARRIVAL_WINDOW = 1.0  # minutos tras llegar en los que un cliente nuevo entra caminando por la izquierda
ENTRY_X = -90.0  # fuera del plano, a la izquierda: de ahí entra quien acaba de llegar
FADE_FRACTION = 0.35  # al salir, el último 35 % del camino se desvanece
EASE_RATE = 7  # qué tan rápido alcanza cada persona su lugar (más alto = más rápido)
ARRIVED_DISTANCE = 3  # a menos de esta distancia la persona ya está parada, no caminando
PT = 0.3  # puntos de tipografía por unidad de dibujo

# Pictograma: cada pose son 5 trazos (tronco, 2 brazos, 2 piernas) como (x1, y1, x2, y2) con el origen en los pies.
STAND = ((0, -98, 0, -56), (-12, -95, -20, -56), (12, -95, 20, -56), (-7, -50, -8, -5), (7, -50, 8, -5))
WALK_A = ((1, -98, 1, -56), (-10, -94, -24, -62), (12, -94, 24, -60), (-4, -50, -21, -6), (5, -50, 19, -7))
WALK_B = ((1, -98, 1, -56), (-10, -94, -17, -56), (12, -94, 17, -56), (-3, -50, -9, -5), (4, -50, 6, -5))
STROKE_UNITS = (30, 10, 10, 13, 13)  # grosor de cada trazo, en unidades de dibujo
STROKE_WIDTHS = [width * PT for width in STROKE_UNITS]  # lo mismo en puntos
HEAD_AREA = (32 * PT) ** 2  # área del círculo de la cabeza, en puntos²
HEAD_RISE, LABEL_RISE = 124, 68  # altura de la cabeza y del número sobre los pies

# Barra de progreso del cobro, bajo el letrero de la caja.
BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT = 1332, 234, 546, 18

# Aviso rojo cuando la cola crece cerca de la saturación.
ALERT_QUEUE, ALERT_UTILIZATION = 12, 0.9

INK_RGBA, EXIT_RGBA = to_rgba(INK), to_rgba(EXIT)
LABEL_FONT = FontProperties(weight="bold")
LABEL_SIZE = 19 * PT


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
    La memoria (`lru_cache`) hace que cada número se convierta en trazo una sola vez.
    """
    box = TextPath((0, 0), str(customer_id), size=LABEL_SIZE, prop=LABEL_FONT).get_extents()  # para centrarlo
    return TextPath((-(box.x0 + box.x1) / 2, 0), str(customer_id), size=LABEL_SIZE, prop=LABEL_FONT)


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


def _draw_queue_area(ax) -> None:
    """Piso y cintas separadoras de la fila serpentina, con sus carteles."""
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


def _draw_register(ax) -> None:
    """Letrero colgante de la caja, mostrador y cajera."""
    for x in (1395, 1815):
        _line(ax, [x, x], [0, 60], 4, INK)
    ax.add_patch(Rectangle((1330, 60), 550, 150, color=INK))
    ax.add_patch(Rectangle((1352, 82), 106, 106, color=SIGNAL))
    _draw_cart(ax)
    _text(ax, 1482, 140, "Caja rápida", 52, "white", "bold")
    _text(ax, 1484, 184, "Hasta 10 artículos", 30, "#c5cad0")

    # La cajera va detrás del mostrador; el cliente atendido se para delante.
    for (a, b, c, d), width in zip(STAND, STROKE_UNITS):
        _line(ax, [1560 + a, 1560 + c], [770 + b, 770 + d], width, INK)
    ax.add_patch(Circle((1560, 646), 16, color=INK))
    ax.add_patch(Rectangle((1400, 690), 280, 110, fc="#cdd3d9", ec=INK, lw=6 * PT, zorder=3))
    ax.add_patch(Rectangle((1403, 693), 274, 14, color=SIGNAL, zorder=3))
    ax.add_patch(Rectangle((1610, 628), 58, 44, color=INK, zorder=3))
    _line(ax, [1420, 1420], [520, 690], 8, INK)  # poste de la lámpara de carril


class Scene:
    """El local dibujado: lo fijo se crea una vez y los elementos móviles se actualizan en cada cuadro."""

    def __init__(self, ax) -> None:
        ax.set_xlim(0, WIDTH)
        ax.set_ylim(HEIGHT, 0)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.add_patch(Rectangle((0, 0), WIDTH, HEIGHT, color=PAPER, zorder=-2))
        _draw_queue_area(ax)
        _draw_register(ax)
        _sign(ax, 22, 30, 250, 74, INK, "Entrada")
        _sign(ax, 1660, 420, 220, 70, EXIT, "Salida")

        # Elementos que cambian. Se crean una sola vez y se reutilizan: nada se crea ni se quita por cuadro.
        self.params = _text(ax, 300, 76, "", 28, INK, "bold")  # cambia solo al cargar otra corrida
        self.lamp = ax.add_patch(Circle((1420, 500), 30, fc=EXIT, ec=INK, lw=7 * PT))
        ax.add_patch(Rectangle((BAR_X - 2, BAR_Y - 2), BAR_WIDTH + 4, BAR_HEIGHT + 4, fc="white", ec=INK, lw=4 * PT))
        self.progress = ax.add_patch(Rectangle((BAR_X, BAR_Y), 0, BAR_HEIGHT, color=SIGNAL))
        self.progress_label = _text(ax, 1330, 296, "", 30, INK, "bold")
        self.overflow = _text(ax, 40, 962, "", 30, SIGNAL, "bold", bbox=dict(fc=INK, ec="none", pad=12), visible=False)
        self.alert = _text(ax, 300, 148, "", 30, "white", "bold", bbox=dict(fc=ALERT, ec="none", pad=8), visible=False)
        # Todas las personas son 3 colecciones (cuerpos, cabezas, números): una por tipo, no un artista por persona.
        self.bodies = ax.add_collection(LineCollection([], capstyle="round", zorder=5))
        self.heads = ax.scatter([], [], s=HEAD_AREA, linewidths=0, zorder=6)
        self.labels = ax.add_collection(PathCollection([], sizes=[1.0], facecolors="white", edgecolors="none",
                                                       offset_transform=ax.transData, zorder=7))
        self.labels.set_transform(IdentityTransform())  # los trazos están en puntos; solo el desplazamiento usa `transData`
        # Capas del blitting (ver window.py): `fast` se pinta en cada cuadro, `slow` cada cierto tiempo.
        self.fast = [self.lamp, self.progress, self.progress_label, self.bodies, self.heads, self.labels]
        self.slow = [self.overflow, self.alert]
        self.positions: dict[int, list[float]] = {}  # id de cliente -> [x, y] actual (se acerca a su destino)
        self.frame = 0  # contador de cuadros: alterna las dos poses de caminar

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

    def _targets(self, run: LiveRun, state: SystemState) -> dict[int, tuple[float, float]]:
        """Hacia dónde camina cada persona visible: su lugar en la fila, la caja o la salida."""
        # Solo caben CAPACITY personas en la serpentina: las demás se cuentan en el letrero de `update_notices`.
        targets = {cid: queue_spot(place) for place, cid in enumerate(state.waiting[:CAPACITY])}
        if state.in_service is not None:
            targets[state.in_service] = SERVICE
        for cid in state.leaving:
            progress = min((state.time - run.customers[cid - 1].departure) / EXIT_WINDOW, 1)  # el id k es el registro k - 1
            targets[cid] = (SERVICE[0] + (EXIT_POINT[0] - SERVICE[0]) * progress, SERVICE[1])
        return targets

    def _step(self, run: LiveRun, state: SystemState, cid: int, target: tuple[float, float], ease: float) -> list[float]:
        """Acerca la posición de la persona a su destino (`ease` = fracción del camino por cuadro)."""
        pos = self.positions.get(cid)
        if pos is None:
            # Quien acaba de llegar entra por la izquierda; quien estaba fuera de la fila aparece en su lugar.
            fresh = state.time - run.customers[cid - 1].arrival < ARRIVAL_WINDOW
            pos = self.positions[cid] = [ENTRY_X, target[1]] if fresh else list(target)
        if cid in state.leaving:  # el destino ya avanza con el tiempo del modelo: se sigue sin suavizar
            pos[:] = target
        else:
            pos[0] += (target[0] - pos[0]) * ease
            pos[1] += (target[1] - pos[1]) * ease
        return pos

    def _update_people(self, run: LiveRun, state: SystemState, speed: float, dt: float) -> None:
        targets = self._targets(run, state)
        for cid in [cid for cid in self.positions if cid not in targets]:  # ya salieron (o volvieron al exterior)
            del self.positions[cid]

        # Suavizado exponencial: independiente de los cuadros por segundo y más rápido con más velocidad.
        ease = 1 - math.exp(-dt * EASE_RATE * max(1, speed))
        walking = (WALK_A, WALK_B)[self.frame // 2 % 2]
        segments, colors, head_xy, head_colors, label_ids, label_xy = [], [], [], [], [], []
        for cid, target in targets.items():
            leaving = cid in state.leaving
            x, y = self._step(run, state, cid, target, ease)
            moving = leaving or math.hypot(target[0] - x, target[1] - y) > ARRIVED_DISTANCE
            pose = walking if moving else STAND
            if leaving:  # verde y se desvanece al llegar a la salida
                fade = (EXIT_POINT[0] - x) / (EXIT_POINT[0] - SERVICE[0]) / FADE_FRACTION
                color = EXIT_RGBA[:3] + (max(0.0, min(1.0, fade)),)
            else:
                color = INK_RGBA
            segments += [((x + a, y + b), (x + c, y + d)) for a, b, c, d in pose]
            colors += [color] * len(pose)
            head_xy.append((x, y - HEAD_RISE))
            head_colors.append(color)
            if not leaving:
                label_ids.append(cid)
                label_xy.append((x + 1, y - LABEL_RISE))

        self.bodies.set_segments(segments)
        self.bodies.set_color(colors)
        self.bodies.set_linewidth(STROKE_WIDTHS * len(targets))
        self.heads.set_offsets(np.array(head_xy).reshape(-1, 2))
        self.heads.set_facecolor(head_colors)
        self.labels.set_paths([label_path(cid) for cid in label_ids])
        self.labels.set_offsets(np.array(label_xy).reshape(-1, 2))

    def _update_register(self, run: LiveRun, state: SystemState) -> None:
        busy = state.in_service is not None
        self.lamp.set_facecolor(SIGNAL if busy else EXIT)
        if busy:
            record = run.customers[state.in_service - 1]
            end = run.duration if record.departure is None else record.departure  # cobro que sigue al cerrar la reproducción
            fraction = min((state.time - record.service_start) / (end - record.service_start), 1) if end > record.service_start else 1
            self.progress_label.set_text(f"Cobrando al cliente {state.in_service}")
        else:
            fraction = 0
            self.progress_label.set_text("Esperando cliente")
        self.progress.set_width(BAR_WIDTH * fraction)

    def update_notices(self, run: LiveRun, state: SystemState) -> None:
        """Letreros que cambian poco: clientes fuera de la fila y aviso rojo de saturación."""
        hidden = len(state.waiting) - CAPACITY  # clientes que ya no caben dibujados en la fila
        self.overflow.set_visible(hidden > 0)
        self.overflow.set_text(f"+{max(hidden, 0)} esperando fuera de la fila")
        # Aviso rojo: sistema inestable, o cola larga con ρ alto.
        if not run.stable:
            message = "Sistema inestable: λ ≥ μ, la teoría no aplica"
        elif len(state.waiting) >= ALERT_QUEUE and run.theory.utilization >= ALERT_UTILIZATION:
            message = f"ρ = {run.theory.utilization:.3f}: la cola crece"
        else:
            message = ""
        self.alert.set_visible(bool(message))
        self.alert.set_text(message)
