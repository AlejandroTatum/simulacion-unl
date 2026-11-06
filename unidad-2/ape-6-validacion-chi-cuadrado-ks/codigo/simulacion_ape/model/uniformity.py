"""Pruebas de bondad de ajuste a U(0, 1): Chi-cuadrado (algoritmo 2) y Kolmogorov-Smirnov."""

from dataclasses import dataclass

from .config import ALPHA, BINS
from .distributions import chi_square_sf, kolmogorov_sf


@dataclass(frozen=True)
class ChiSquareResult:
    observed: list[int]
    expected: float
    statistic: float
    df: int
    p_value: float


@dataclass(frozen=True)
class KsResult:
    d_plus: float
    d_minus: float
    statistic: float
    p_value: float


def chi_square_test(values: list[float], bins: int = BINS) -> ChiSquareResult:
    """Cuenta cuántos valores caen en cada subintervalo y suma (O - E)² / E."""
    observed = [0] * bins
    for u in values:
        observed[min(int(u * bins), bins - 1)] += 1
    expected = len(values) / bins
    statistic = 0.0
    for o in observed:
        diff = o - expected
        statistic += diff * diff / expected
    df = bins - 1
    return ChiSquareResult(observed, expected, statistic, df, chi_square_sf(statistic, df))


def ks_test(values: list[float]) -> KsResult:
    """D = máx(D+, D-) entre la FDE de los datos ordenados y F(x) = x."""
    ordered = sorted(values)
    n = len(ordered)
    d_plus = 0.0
    d_minus = 0.0
    for i, u in enumerate(ordered, start=1):
        d_plus = max(d_plus, i / n - u)
        d_minus = max(d_minus, u - (i - 1) / n)
    statistic = max(d_plus, d_minus)
    return KsResult(d_plus, d_minus, statistic, kolmogorov_sf(n, statistic))


def rejects_h0(p_value: float, alpha: float = ALPHA) -> bool:
    """Criterio de la guía: si p ≥ α no se rechaza H0; si p < α se rechaza."""
    return p_value < alpha


def decision(p_value: float, alpha: float = ALPHA) -> str:
    return "Se rechaza H0" if rejects_h0(p_value, alpha) else "No se rechaza H0"
