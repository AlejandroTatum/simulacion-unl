"""Distribuciones del sistema: objetivo f(x), propuesta g(x) = 1 y constante de aceptación M."""

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np


def proposal_density(x):
    """Distribución propuesta g(x) = 1 en 0 ≤ x ≤ 1 (uniforme)."""
    return np.ones_like(np.asarray(x, dtype=float))


@dataclass(frozen=True)
class TargetDistribution:
    """Distribución objetivo f(x) en [0, 1] con su constante M = max(f(x)/g(x))."""

    label: str                      # nombre que aparece en tablas y gráficas
    name: str                       # nombre corto para los archivos
    density: Callable
    m: float

    def ratio(self, x):
        """Paso 5.5: R = f(X) / (M·g(X))."""
        return self.density(x) / (self.m * proposal_density(x))

    @property
    def theoretical_efficiency(self) -> float:
        """Eficiencia teórica ET = (1/M)·100."""
        return 100 / self.m


# Distribución de la guía: f(x) = 2x con M = 2 (criterio U ≤ X, ET = 50 %).
LINEAR = TargetDistribution("f(x)=2x", "lineal", lambda x: 2 * x, 2.0)
# Actividad complementaria: f(x) = 3x² con M = 3 (criterio U ≤ X², ET = 33.33 %).
QUADRATIC = TargetDistribution("f(x)=3x²", "cuadratica", lambda x: 3 * x**2, 3.0)
TARGETS = (LINEAR, QUADRATIC)
