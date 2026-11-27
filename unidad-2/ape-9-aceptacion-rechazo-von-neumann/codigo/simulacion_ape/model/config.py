"""Parámetros de la práctica, separados de la lógica que los usa."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationConfig:
    seed: int = 42                                   # semilla del generador uniforme
    sizes: tuple[int, ...] = (1_000, 5_000, 10_000)  # número de candidatos N de cada simulación
