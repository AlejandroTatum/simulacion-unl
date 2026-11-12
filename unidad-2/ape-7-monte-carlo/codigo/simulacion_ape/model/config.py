"""Parámetros de la práctica: generador, tamaños de muestra y los dos experimentos."""

import math
from collections.abc import Callable
from dataclasses import dataclass

from .lcg import LcgConfig
from .monte_carlo import count_dice_hits, count_pi_hits

# Mismo generador de la APE 5 (constantes de Numerical Recipes), con período completo 2^32.
DEFAULT_LCG = LcgConfig("LCG APE 5", a=1664525, c=1013904223, m=2**32, seed=12345)

# Tamaños de muestra que pide la guía.
SIZES = (1_000, 10_000, 100_000, 1_000_000)

# Cada medición de tiempo se repite y se toma el mínimo, para reducir el ruido del sistema.
TIMING_REPEATS = 3

# Puntos que se dibujan en la figura del círculo.
SCATTER_POINTS = 5_000


@dataclass(frozen=True)
class Experiment:
    """Un modelo Monte Carlo: estimador = scale · aciertos / N."""

    key: str                 # nombre que también entiende el programa Java
    label: str
    symbol: str
    exact: float             # valor real contra el que se mide el error
    scale: float
    hit_probability: float   # probabilidad p de un acierto
    count_hits: Callable

    def estimate(self, hits: int, n: int) -> float:
        return self.scale * hits / n

    def standard_error(self, n: int) -> float:
        """Error estándar teórico del estimador: scale · √(p(1−p)/N)."""
        p = self.hit_probability
        return self.scale * math.sqrt(p * (1.0 - p) / n)


PI = Experiment("pi", "Estimación de π (círculo inscrito)", "π", exact=math.pi, scale=4.0,
                hit_probability=math.pi / 4, count_hits=count_pi_hits)

DICE = Experiment("dados", "P(suma de dos dados = 7)", "P", exact=6 / 36, scale=1.0,
                  hit_probability=6 / 36, count_hits=count_dice_hits)

EXPERIMENTS = (PI, DICE)
