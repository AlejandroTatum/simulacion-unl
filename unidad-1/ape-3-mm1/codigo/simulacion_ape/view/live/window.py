"""Vista en vivo: ventana de Matplotlib con el diseño, los controles y el ciclo de animación.

La ventana no simula: cada vez que cambian λ o μ le pide una corrida a `make_run` (un callback que arma
el controlador con funciones del modelo) y la reproduce minuto a minuto.

Para que la animación sea fluida se usa blitting (ver `LiveWindow._blit`): redibujar toda la figura cuesta
cerca de 200 ms por los ~150 textos, así que el dibujo completo solo ocurre cuando cambia algo fijo.
"""

import time
from collections.abc import Callable

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, Slider

from ...model.config import Scenario
from ...model.live import LiveRun
from .board import Board
from .charts import Histogram, OccupancyChart
from .scene import EXIT_WINDOW, Scene
from .theme import BOARD_RULE, INK, SIGNAL, WALL, hide_frame

SPEEDS = (0.5, 1, 2, 4)  # minutos simulados por segundo real
FRAME_MS = 10  # pausa entre cuadros; el período real es esta pausa más lo que cuesta pintar (~30 cuadros por segundo)
SLOW_SECONDS = 0.25  # cada cuánto tiempo real se actualizan los histogramas, la columna viva y los avisos
MAX_STEP = 0.25  # un cuadro lento no hace saltar el reloj más de este tiempo real (segundos)
RATE_MIN, RATE_MAX, RATE_STEP = 0.1, 5.0, 0.1  # rango y paso de los deslizadores de λ y μ
BUTTON_IDLE, BUTTON_HOVER = "#2b2d33", "#3d3f45"
# Posición de cada panel como [izquierda, abajo, ancho, alto] en fracciones de la ventana.
SCENE_RECT = [0.01, 0.35, 0.60, 0.51]
BOARD_RECT = [0.62, 0.35, 0.37, 0.51]
CHART_X = (0.045, 0.37, 0.695)  # izquierda de cada una de las tres gráficas (misma fila, mismo tamaño)


def _dark_axes(fig, rect):
    ax = fig.add_axes(rect, facecolor=INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    hide_frame(ax)
    return ax


class LiveWindow:
    """Reproduce una `LiveRun` en una figura de Matplotlib y atiende los controles del usuario."""

    def __init__(self, make_run: Callable[[float, float], LiveRun], presets: tuple[Scenario, ...],
                 start_rates: tuple[float, float], duration: float, speed: float = 1.0) -> None:
        self.make_run = make_run  # la única vía por la que la vista obtiene datos
        self.presets = presets
        self.duration = duration
        self.speeds = sorted({*SPEEDS, speed})
        self.speed = speed
        self.playing = False
        self.time = 0.0  # minuto simulado que se está mostrando
        self.last_tick = time.perf_counter()
        self.timer = None  # temporizador de la ventana; se crea en show()
        # Imágenes guardadas para el blitting (ver `_blit`).
        self._static_bg = None  # fondo: todo lo fijo de la ventana
        self._frame_bg = None  # fondo + capa lenta: es lo que se restaura en cada cuadro
        self._bg_size = None
        self._slow_dirty = False  # la capa lenta tiene valores nuevos que aún no están en `_frame_bg`
        self._since_slow = 0.0

        self.fig = plt.figure(figsize=(15, 8.5), dpi=90, facecolor=WALL)  # ventana de 1350 × 765 píxeles
        if self.fig.canvas.manager:
            self.fig.canvas.manager.set_window_title("Caja rápida — Simulación M/M/1 con SimPy")
        self._build_header()
        self._build_sliders(start_rates)
        self.scene = Scene(self.fig.add_axes(SCENE_RECT))
        self.board = Board(self.fig.add_axes(BOARD_RECT))
        ax_occupancy, ax_arrivals, ax_service = (self.fig.add_axes([x, 0.075, 0.285, 0.20]) for x in CHART_X)
        self.occupancy = OccupancyChart(ax_occupancy)
        self.arrivals = Histogram(ax_arrivals, "Tiempo entre llegadas")
        self.service = Histogram(ax_service, "Tiempo de servicio")
        self._split_layers()
        self.fig.canvas.mpl_connect("draw_event", self._on_draw)
        # Los deslizadores solo vuelven a simular al soltar el mouse, no mientras se arrastran.
        self.fig.canvas.mpl_connect("button_release_event", lambda _: self.apply_sliders())
        self.fig.canvas.mpl_connect("key_press_event", self._on_key)
        self.load(*start_rates)

    def _split_layers(self) -> None:
        """Reparte los elementos que cambian en dos capas y los marca `animated`.

        Un artista `animated` no entra en el dibujo completo de la figura: lo pintamos nosotros encima del fondo.
        La capa rápida (personas, reloj, contadores, L(t)) se pinta en cada cuadro; la lenta (histogramas, columna
        "Simulado ahora", avisos) solo cada `SLOW_SECONDS`, porque cambia poco y es lo más caro de dibujar.
        """
        parts = (self.scene, self.board, self.occupancy, self.arrivals, self.service)
        self.fast = sorted((a for part in parts for a in part.fast), key=lambda a: a.get_zorder())
        self.slow = sorted((a for part in parts for a in part.slow), key=lambda a: a.get_zorder())
        for artist in self.fast + self.slow:
            artist.set_animated(True)

    def _build_header(self) -> None:
        """Franja superior: título, botones de escenario, pausa, reinicio y velocidad."""
        header = _dark_axes(self.fig, [0, 0.915, 1, 0.085])
        header.text(0.012, 0.52, "Caja rápida", color="white", fontsize=20, fontweight="bold")
        header.text(0.012, 0.16, "Sistema de colas M/M/1 simulado con SimPy", color="#c5cad0", fontsize=9)

        # Un botón por escenario de la guía: al pulsarlo, los deslizadores toman sus valores.
        self.preset_buttons = []
        for i, scenario in enumerate(self.presets):
            label = (f"{scenario.number}  {scenario.condition}\n"
                     f"λ {scenario.arrival_rate:.1f}   μ {scenario.service_rate:.1f}   ρ {scenario.utilization:.3f}")
            button = Button(self.fig.add_axes([0.255 + 0.155 * i, 0.925, 0.145, 0.065]), label,
                            color=BUTTON_IDLE, hovercolor=BUTTON_HOVER)
            button.label.set_fontsize(9)
            button.on_clicked(lambda _, s=scenario: self.select_preset(s))
            self.preset_buttons.append(button)

        self.play_button = Button(self.fig.add_axes([0.725, 0.925, 0.075, 0.065]), "Pausar", color="white", hovercolor=SIGNAL)
        self.play_button.on_clicked(lambda _: self.toggle_play())
        self.restart_button = Button(self.fig.add_axes([0.805, 0.925, 0.075, 0.065]), "Reiniciar", color="white", hovercolor=SIGNAL)
        self.restart_button.on_clicked(lambda _: self.load(self.run.arrival_rate, self.run.service_rate))

        header.text(0.945, 0.72, "min por seg", color="#c5cad0", fontsize=8, ha="center")
        count = len(self.speeds)
        self.speed_radio = RadioButtons(
            self.fig.add_axes([0.893, 0.925, 0.105, 0.04], facecolor=INK), [f"{s:g}" for s in self.speeds],
            active=self.speeds.index(self.speed), activecolor=SIGNAL, layout=(1, count),
            label_props={"color": ["white"] * count, "fontsize": [9] * count}, radio_props={"s": [60] * count})
        self.speed_radio.on_clicked(lambda label: setattr(self, "speed", float(label)))

    def _build_sliders(self, start_rates: tuple[float, float]) -> None:
        """Deslizadores de λ (llegadas) y μ (atenciones)."""
        sliders = []
        for rect, label, value in (([0.14, 0.872, 0.28, 0.022], "λ  llegadas/min", start_rates[0]),
                                   ([0.58, 0.872, 0.28, 0.022], "μ  atenciones/min", start_rates[1])):
            slider = Slider(self.fig.add_axes(rect), label, RATE_MIN, RATE_MAX, valinit=value, valstep=RATE_STEP,
                            valfmt="%.1f", color=SIGNAL, track_color=BOARD_RULE)
            slider.label.set_fontsize(10)
            slider.valtext.set_fontsize(10)
            sliders.append(slider)
        self.lambda_slider, self.mu_slider = sliders

    def load(self, arrival_rate: float, service_rate: float) -> None:
        """Pide una corrida nueva con estas tasas (misma semilla) y la reproduce desde el minuto 0."""
        self.run = self.make_run(arrival_rate, service_rate)
        self.time = 0.0
        self.scene.reset()
        self.scene.set_run(self.run)
        self.board.set_run(self.run)
        self.occupancy.set_run(self.run)
        self.arrivals.set_rate(self.run.arrival_rate)
        self.service.set_rate(self.run.service_rate)
        self._sync_controls(arrival_rate, service_rate)
        self._set_playing(True)
        self._static_bg = None  # cambió lo fijo (curvas teóricas, ejes, textos): el próximo dibujo completo lo guarda
        self.render()
        self.fig.canvas.draw_idle()

    def select_preset(self, scenario: Scenario) -> None:
        """Escenario de la guía: pone sus λ y μ en los deslizadores y simula."""
        self.load(scenario.arrival_rate, scenario.service_rate)

    def apply_sliders(self) -> None:
        """Se llama al soltar el mouse: si los deslizadores cambiaron λ o μ, vuelve a simular."""
        rates = (round(self.lambda_slider.val, 2), round(self.mu_slider.val, 2))  # quita el ruido de coma flotante
        if rates != (self.run.arrival_rate, self.run.service_rate):
            self.load(*rates)

    def _sync_controls(self, arrival_rate: float, service_rate: float) -> None:
        """Deslizadores y botón de escenario reflejan las tasas en uso (sin disparar otra simulación)."""
        for slider, value in ((self.lambda_slider, arrival_rate), (self.mu_slider, service_rate)):
            slider.eventson = False  # mover el deslizador por código no debe llamar a sus callbacks
            slider.set_val(value)
            slider.eventson = True
        for button, scenario in zip(self.preset_buttons, self.presets):
            active = (scenario.arrival_rate, scenario.service_rate) == (arrival_rate, service_rate)
            button.color, button.hovercolor = (SIGNAL, SIGNAL) if active else (BUTTON_IDLE, BUTTON_HOVER)
            button.ax.set_facecolor(button.color)
            button.label.set_color(INK if active else "white")

    def toggle_play(self) -> None:
        """Pausa o reanuda; si la reproducción terminó, la repite desde el minuto 0."""
        if not self.playing and self.time >= self.duration:
            self.load(self.run.arrival_rate, self.run.service_rate)
        else:
            self._set_playing(not self.playing)

    def _set_playing(self, playing: bool) -> None:
        """Cambia entre reproducir y pausa: texto del botón y temporizador."""
        self.playing = playing
        self.last_tick = time.perf_counter()
        self.play_button.label.set_text("Pausar" if playing else "Repetir" if self.time >= self.duration else "Reanudar")
        if self.timer:  # en pausa no hace falta animar
            if playing:
                self.timer.start()
            else:
                self.timer.stop()
        self.fig.canvas.draw_idle()  # cambió el texto del botón: dibujo completo (y fondo nuevo)

    def advance(self, seconds: float, slow: bool = True) -> None:
        """Avanza el reloj `seconds` de tiempo real (a `speed` minutos por segundo) y actualiza los datos."""
        if self.playing:
            self.time = min(self.time + seconds * self.speed, self.duration)
            if self.time >= self.duration:
                self._set_playing(False)
        self.render(seconds, slow or not self.playing)

    def render(self, seconds: float = 0.0, slow: bool = True) -> None:
        """Actualiza animación, tablero y gráficas con lo que ocurrió hasta el minuto actual.

        Con `slow=False` se omite la capa lenta (histogramas, columna viva y avisos).
        """
        state = self.run.state_at(self.time, EXIT_WINDOW)
        self.scene.update(self.run, state, self.speed, seconds)
        self.board.update(state)
        self.occupancy.update(self.run, self.time)
        if slow:
            self.scene.update_notices(self.run, state)
            self.board.update_live(self.run.metrics_at(self.time))
            # Recalcular los histogramas recorre a todos los clientes: por eso va en la capa lenta.
            self.arrivals.update(self.run.interarrival_times(self.time))
            self.service.update(self.run.service_times(self.time))
            self._slow_dirty = True

    def frame(self, seconds: float) -> list:
        """Un cuadro de la animación: avanza el reloj, actualiza los datos y pinta solo los artistas animados."""
        self._since_slow += seconds
        slow = self._since_slow >= SLOW_SECONDS
        if slow:
            self._since_slow = 0.0
        self.advance(seconds, slow)
        return self._blit()

    def _on_frame(self) -> None:
        now = time.perf_counter()
        seconds, self.last_tick = min(now - self.last_tick, MAX_STEP), now
        self.frame(seconds)

    def _on_draw(self, _event) -> None:
        """Tras un dibujo completo de la figura (sin los artistas animados): guarda el fondo y pinta encima las dos capas."""
        canvas = self.fig.canvas
        if canvas.is_saving():  # al guardar una imagen sí se dibuja todo; ese resultado no sirve de fondo
            return
        self._static_bg = canvas.copy_from_bbox(self.fig.bbox)
        self._bg_size = tuple(self.fig.bbox.size)
        self._paint_slow()
        for artist in self.fast:
            self.fig.draw_artist(artist)

    def _paint_slow(self) -> None:
        """Pinta la capa lenta sobre el fondo y guarda el resultado: así no se vuelve a dibujar en cada cuadro."""
        for artist in self.slow:
            self.fig.draw_artist(artist)
        self._frame_bg = self.fig.canvas.copy_from_bbox(self.fig.bbox)
        self._slow_dirty = False

    def _blit(self) -> list:
        """Blitting: en vez de redibujar la figura, restaura la imagen guardada, pinta encima solo lo que se mueve y
        copia el resultado a la pantalla. Cuesta unos pocos milisegundos en lugar de ~200 ms."""
        canvas = self.fig.canvas
        if self._static_bg is None or self._bg_size != tuple(self.fig.bbox.size):
            canvas.draw_idle()  # no hay fondo válido (recién cargado o cambió el tamaño): el dibujo completo lo crea
            return []
        if self._slow_dirty:
            canvas.restore_region(self._static_bg)
            self._paint_slow()
        canvas.restore_region(self._frame_bg)
        for artist in self.fast:
            self.fig.draw_artist(artist)
        canvas.blit(self.fig.bbox)
        return self.fast

    def _on_key(self, event) -> None:
        """Atajos: espacio pausa, R reinicia, ← → cambian la velocidad, 1 2 3 cargan un escenario."""
        if event.key == " ":
            self.toggle_play()
        elif event.key == "r":
            self.load(self.run.arrival_rate, self.run.service_rate)
        elif event.key in ("left", "right"):
            index = self.speeds.index(self.speed) + (1 if event.key == "right" else -1)
            self.speed_radio.set_active(min(max(index, 0), len(self.speeds) - 1))
        elif event.key in ("1", "2", "3") and int(event.key) <= len(self.presets):
            self.select_preset(self.presets[int(event.key) - 1])

    def is_interactive(self) -> bool:
        """False si Matplotlib quedó con un backend sin ventana (por ejemplo Agg, sin Tk instalado)."""
        return self.fig.canvas.required_interactive_framework is not None

    def show(self) -> None:
        """Abre la ventana y bloquea hasta que se cierre."""
        self.timer = self.fig.canvas.new_timer(interval=FRAME_MS)
        self.timer.add_callback(self._on_frame)
        self.fig.canvas.mpl_connect("close_event", lambda _: self.timer.stop())
        self.last_tick = time.perf_counter()
        if self.playing:
            self.timer.start()
        plt.show()
