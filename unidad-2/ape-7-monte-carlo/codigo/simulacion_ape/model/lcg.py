"""Generador congruencial lineal: X(n+1) = (a * X(n) + c) mod m, U = X / m."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LcgConfig:
    name: str
    a: int
    c: int
    m: int
    seed: int


class Lcg:
    """Entrega un número a la vez, sin guardar la secuencia (un millón de puntos no ocupa memoria)."""

    def __init__(self, config: LcgConfig) -> None:
        self._a = config.a
        self._c = config.c
        self._m = config.m
        self._state = config.seed

    def next_state(self) -> int:
        """Siguiente estado entero X(n+1). La semilla X0 no se entrega."""
        self._state = (self._a * self._state + self._c) % self._m
        return self._state

    def next_uniform(self) -> float:
        """Siguiente uniforme U = X / m, siempre en [0, 1)."""
        return self.next_state() / self._m
