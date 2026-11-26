"""Medidas estadísticas experimentales frente a las teóricas (algoritmos 1 y 4)."""

from dataclasses import dataclass

import numpy as np

from .inverse_transform import validate_rate

UNIFORM_MEAN = 0.5
UNIFORM_VARIANCE = 1 / 12


@dataclass(frozen=True)
class Comparison:
    """Media y varianza experimentales y teóricas con su error porcentual."""

    label: str
    theoretical_mean: float
    experimental_mean: float
    theoretical_variance: float
    experimental_variance: float

    @property
    def mean_error_pct(self) -> float:
        return percent_error(self.experimental_mean, self.theoretical_mean)

    @property
    def variance_error_pct(self) -> float:
        return percent_error(self.experimental_variance, self.theoretical_variance)


def percent_error(experimental: float, theoretical: float) -> float:
    """Error porcentual |experimental - teórico| / teórico · 100."""
    return abs(experimental - theoretical) / theoretical * 100


def sample_variance(values: np.ndarray) -> float:
    """Varianza muestral (divide entre N - 1)."""
    return float(np.var(values, ddof=1))


def compare_uniform(u: np.ndarray) -> Comparison:
    """Media y varianza de U frente a 1/2 y 1/12."""
    return Comparison("U(0,1)", UNIFORM_MEAN, float(np.mean(u)), UNIFORM_VARIANCE, sample_variance(u))


def compare_exponential(x: np.ndarray, rate: float) -> Comparison:
    """Media y varianza de X frente a 1/λ y 1/λ²."""
    validate_rate(rate)
    return Comparison(f"λ = {rate}", 1 / rate, float(np.mean(x)), 1 / rate**2, sample_variance(x))
