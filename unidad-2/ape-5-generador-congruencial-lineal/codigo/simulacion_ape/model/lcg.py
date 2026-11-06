"""Generador Congruencial Lineal: X(n+1) = (a · X(n) + c) mod m."""

from .config import LcgConfig


def lcg_states(config: LcgConfig) -> list[int]:
    """Devuelve X1..Xn a partir de la semilla X0 (la semilla no se incluye)."""
    states = []
    x = config.seed
    for _ in range(config.n):
        x = (config.a * x + config.c) % config.m
        states.append(x)
    return states


def normalize(states: list[int], m: int) -> list[float]:
    """U(n) = X(n) / m, valores en [0, 1)."""
    return [x / m for x in states]
