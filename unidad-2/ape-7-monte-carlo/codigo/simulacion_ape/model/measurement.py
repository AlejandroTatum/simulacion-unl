"""Resultado de una ejecución de un experimento, en cualquiera de los dos lenguajes."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Measurement:
    hits: int
    estimate: float
    error: float      # error absoluto |valor real − estimación|
    seconds: float
