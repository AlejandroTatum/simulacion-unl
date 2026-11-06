"""Comparación Python vs Java y estadísticas de la secuencia normalizada."""

from dataclasses import dataclass
from statistics import fmean, pvariance


@dataclass(frozen=True)
class ComparisonRow:
    index: int
    x_python: int
    x_java: int
    u_python: float
    u_java: float

    @property
    def equal(self) -> bool:
        return self.x_python == self.x_java


@dataclass(frozen=True)
class SequenceStats:
    seed: int
    mean: float
    variance: float
    lag1_correlation: float
    first_values: tuple[float, ...]


def compare(python_states: list[int], java_states: list[int], m: int, count: int) -> list[ComparisonRow]:
    return [
        ComparisonRow(i, xp, xj, xp / m, xj / m)
        for i, (xp, xj) in enumerate(zip(python_states[:count], java_states[:count]), start=1)
    ]


def mismatches(python_states: list[int], java_states: list[int]) -> int:
    """Cantidad de posiciones distintas en toda la secuencia (también cuenta largos distintos)."""
    differing = sum(1 for xp, xj in zip(python_states, java_states) if xp != xj)
    return differing + abs(len(python_states) - len(java_states))


def lag1_correlation(values: list[float]) -> float:
    """Correlación entre U(n) y U(n+1); cerca de 0 si no hay dependencia lineal."""
    x, y = values[:-1], values[1:]
    mx, my = fmean(x), fmean(y)
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sx = sum((a - mx) ** 2 for a in x) ** 0.5
    sy = sum((b - my) ** 2 for b in y) ** 0.5
    return cov / (sx * sy)


def sequence_stats(seed: int, values: list[float], shown: int = 5) -> SequenceStats:
    return SequenceStats(seed, fmean(values), pvariance(values), lag1_correlation(values),
                         tuple(values[:shown]))
