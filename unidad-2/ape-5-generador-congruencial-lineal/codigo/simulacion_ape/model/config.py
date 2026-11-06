"""Parámetros del generador, separados de la lógica que los usa."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LcgConfig:
    """Parámetros de la guía: a = 1664525, c = 1013904223, m = 2^32, semilla = 12345."""

    a: int = 1_664_525
    c: int = 1_013_904_223
    m: int = 2**32
    seed: int = 12_345
    n: int = 10_000


# Cantidad de observaciones que se comparan entre Python y Java en la tabla.
COMPARED_VALUES = 20

# Semillas alternativas para el paso 7 (cambiar la semilla).
ALTERNATIVE_SEEDS = (54_321, 1)
