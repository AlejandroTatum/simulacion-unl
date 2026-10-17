"""Configuración común de las pruebas."""

import matplotlib

# Las pruebas no abren ventanas: Agg dibuja en memoria, sin pantalla ni Tk.
matplotlib.use("Agg")
