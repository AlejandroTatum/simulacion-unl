"""Datos de entrada de la guía y parámetros de los escenarios de la práctica."""

from pathlib import Path

import numpy as np

# Población observada en siete períodos consecutivos (t = 0, 1, ..., 6), dato de la guía.
DATA = np.array([1000, 1100, 1250, 1400, 1600, 1850, 2100], dtype=float)

# Arreglo nuevo para la pregunta de control: la misma serie invertida, una población que decrece.
DECREASING_DATA = DATA[::-1].copy()

SEED = 42  # semilla configurable de toda corrida aleatoria
RUNS = 500  # corridas del modelo estocástico para la banda de Monte Carlo
DT = 0.1  # paso de Euler del escenario principal

R_VALUES = (-0.15, -0.05, 0.0, 0.05, 0.12, 0.20)  # tasas para estudiar la influencia de r
SIGMA_VALUES = (0, 25, 75, 150)  # niveles de ruido para estudiar la influencia de sigma
DT_VALUES = (1.0, 0.5, 0.1, 0.01)  # pasos de Euler para estudiar la influencia de dt

FIGURES_DIR = Path("figuras")
