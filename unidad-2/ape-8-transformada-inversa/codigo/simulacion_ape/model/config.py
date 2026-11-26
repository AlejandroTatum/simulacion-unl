"""Parámetros de la práctica, separados de la lógica que los usa."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationConfig:
    n: int = 10_000                        # tamaño de la muestra (algoritmo 1)
    seed: int = 42                         # semilla del generador uniforme
    rate: float = 0.5                      # λ de los algoritmos 2, 3 y 4
    rates: tuple[float, ...] = (0.5, 1.0, 2.0)  # tasas del algoritmo 5
