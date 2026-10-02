"""Parámetros del modelo y datos de entrada tomados de la guía de la práctica."""

from pathlib import Path

import numpy as np

# Pesos de la humedad (H), la nubosidad (N) y el factor de temperatura (Tf).
WEIGHTS = (0.5, 0.3, 0.2)

# Límite inferior de cada estado, evaluado de mayor a menor.
STATES = ((0.75, "Lluvia"), (0.60, "Lluvia probable"), (0.40, "Baja posibilidad"))
DEFAULT_STATE = "Sin lluvia"

HOURS = ["06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"]
HUMIDITY = np.array([65, 70, 68, 60, 75, 85, 92, 88, 80])  # %
CLOUDINESS = np.array([40, 50, 45, 30, 70, 85, 95, 90, 75])  # %
TEMPERATURE = np.array([14, 16, 18, 22, 20, 18, 16, 17, 15])  # °C

FIGURES_DIR = Path("figuras")
