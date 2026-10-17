"""Vista en vivo: paleta compartida por la animación, el tablero y las gráficas. Cada color de señal tiene un solo significado."""

INK = "#16171a"  # letreros, pictogramas, tablero y serie L(t)
WALL = "#e4e7ea"  # fondo de la ventana
PAPER = "#f7f8f9"  # fondo del local y de las gráficas
FLOOR = "#d3d8dd"  # franja del piso
SIGNAL = "#ffc20e"  # amarillo: lo que ocurre ahora (caja ocupada, cola, minuto actual)
EXIT = "#00875a"  # verde: libre o saliendo, y serie Lq(t)
ALERT = "#c8102e"  # rojo: solo saturación
MUTED = "#5d636b"  # etiquetas de ejes
RULE = "#c2c8cf"  # barras de los histogramas
BOARD_CELL = "#24262b"  # celda del tablero
BOARD_CELL_LIVE = "#2e2b1c"  # celda de la columna "Simulado ahora"
BOARD_LABEL = "#a3a9b0"  # etiquetas del tablero
BOARD_RULE = "#3a3c42"  # líneas del tablero


def hide_frame(ax) -> None:
    """Quita marcas y bordes del eje: sirve de lienzo para dibujar texto y figuras a mano."""
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ax.spines.values():
        side.set_visible(False)
