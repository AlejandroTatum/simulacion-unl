"""Colas de las distribuciones Chi-cuadrado y de Kolmogorov, programadas sin librerías.

Java no trae estas funciones, así que ambos lenguajes usan exactamente las mismas fórmulas
(Numerical Recipes, cap. 6 y 14) y obtienen los mismos valores p.
"""

import math

_LANCZOS_G = 7
_LANCZOS_COEF = (
    0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
    -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6,
    1.5056327351493116e-7,
)
_TINY = 1e-300
_EPS = 1e-15
_MAX_ITERATIONS = 1000


def log_gamma(z: float) -> float:
    """ln Γ(z) para z ≥ 0.5 con la aproximación de Lanczos."""
    z -= 1
    x = _LANCZOS_COEF[0]
    for i in range(1, len(_LANCZOS_COEF)):
        x += _LANCZOS_COEF[i] / (z + i)
    t = z + _LANCZOS_G + 0.5
    return 0.5 * math.log(2 * math.pi) + (z + 0.5) * math.log(t) - t + math.log(x)


def regularized_gamma_q(s: float, x: float) -> float:
    """Q(s, x) = Γ(s, x) / Γ(s): serie si x < s + 1, fracción continua (Lentz) en otro caso."""
    if x <= 0:
        return 1.0
    log_prefactor = -x + s * math.log(x) - log_gamma(s)
    if x < s + 1:
        term = 1.0 / s
        total = term
        k = s
        for _ in range(_MAX_ITERATIONS):
            k += 1
            term *= x / k
            total += term
            if abs(term) < abs(total) * _EPS:
                break
        return 1.0 - total * math.exp(log_prefactor)
    b = x + 1 - s
    c = 1 / _TINY
    d = 1 / b
    h = d
    for i in range(1, _MAX_ITERATIONS):
        an = -i * (i - s)
        b += 2
        d = an * d + b
        if abs(d) < _TINY:
            d = _TINY
        c = b + an / c
        if abs(c) < _TINY:
            c = _TINY
        d = 1 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < _EPS:
            break
    return math.exp(log_prefactor) * h


def chi_square_sf(statistic: float, df: int) -> float:
    """Valor p de la prueba: P(χ²(gl) ≥ estadístico) = Q(gl/2, χ²/2)."""
    return regularized_gamma_q(df / 2, statistic / 2)


def kolmogorov_q(lam: float) -> float:
    """Q_KS(λ) = 2 · Σ (-1)^(j-1) · exp(-2 j² λ²); vale 1 cuando la serie no converge (λ pequeño)."""
    a2 = -2 * lam * lam
    sign = 2.0
    total = 0.0
    previous = 0.0
    for j in range(1, 101):
        term = sign * math.exp(a2 * j * j)
        total += term
        if abs(term) <= 0.001 * previous or abs(term) <= 1e-8 * total:
            return min(max(total, 0.0), 1.0)
        sign = -sign
        previous = abs(term)
    return 1.0


def kolmogorov_sf(n: int, d: float) -> float:
    """Valor p de K-S con la corrección de Stephens: λ = (√N + 0.12 + 0.11/√N) · D."""
    sqrt_n = math.sqrt(n)
    return kolmogorov_q((sqrt_n + 0.12 + 0.11 / sqrt_n) * d)
