"""Distribuciones del sistema: uniforme U(0,1) y exponencial generada por Transformada Inversa."""

import numpy as np


def generate_uniforms(n: int, seed: int) -> np.ndarray:
    """Algoritmo 1: vector de N números aleatorios uniformes en [0, 1)."""
    rng = np.random.default_rng(seed)
    return rng.random(n)


def validate_rate(rate: float) -> None:
    """La tasa λ de la exponencial debe ser mayor que cero."""
    if not rate > 0:
        raise ValueError(f"lambda debe ser mayor que 0 (se recibió {rate})")


def inverse_exponential(u, rate: float):
    """Algoritmo 2: X = -ln(1 - U) / λ, inversa de F(x) = 1 - e^(-λx)."""
    validate_rate(rate)
    return -np.log(1.0 - np.asarray(u, dtype=float)) / rate


def exponential_density(x, rate: float):
    """Densidad teórica f(x) = λ·e^(-λx) para x ≥ 0 (algoritmo 3)."""
    validate_rate(rate)
    x = np.asarray(x, dtype=float)
    return np.where(x >= 0, rate * np.exp(-rate * x), 0.0)
