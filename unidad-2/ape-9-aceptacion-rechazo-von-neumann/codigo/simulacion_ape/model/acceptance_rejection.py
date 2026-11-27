"""Algoritmo ACEPTACION_RECHAZO de la guía."""

from dataclasses import dataclass

import numpy as np

from .distributions import TargetDistribution


def accepts(u, r):
    """Paso 5.6: el candidato se acepta si U ≤ R (la igualdad también se acepta)."""
    return u <= r


@dataclass(frozen=True)
class SamplingResult:
    """Candidatos X, uniformes U y la marca de aceptación de cada uno."""

    target: TargetDistribution
    candidates: np.ndarray
    uniforms: np.ndarray
    accepted: np.ndarray            # máscara booleana: True si el candidato se aceptó

    @property
    def accepted_values(self) -> np.ndarray:
        return self.candidates[self.accepted]

    @property
    def n_accepted(self) -> int:
        return int(np.count_nonzero(self.accepted))

    @property
    def n_rejected(self) -> int:
        return len(self.candidates) - self.n_accepted

    @property
    def efficiency(self) -> float:
        """Paso 6: E = (aceptados / N)·100."""
        return self.n_accepted / len(self.candidates) * 100


def acceptance_rejection(target: TargetDistribution, n: int, seed: int) -> SamplingResult:
    """Pasos 1 a 6 con N candidatos; cada fila de números da primero X y luego U (pasos 5.1 y 5.2)."""
    rng = np.random.default_rng(seed)
    pairs = rng.random((n, 2))
    x, u = pairs[:, 0], pairs[:, 1]
    return SamplingResult(target, x, u, accepts(u, target.ratio(x)))
