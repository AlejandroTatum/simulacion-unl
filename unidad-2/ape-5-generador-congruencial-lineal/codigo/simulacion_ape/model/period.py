"""Análisis del período: teorema de Hull-Dobell y detección empírica de ciclos."""

from math import gcd


def prime_factors(n: int) -> set[int]:
    factors = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1
    if n > 1:
        factors.add(n)
    return factors


def hull_dobell(a: int, c: int, m: int) -> dict[str, bool]:
    """Condiciones de Hull-Dobell para período completo (τ = m) con c ≠ 0."""
    return {
        "c y m son primos relativos": gcd(c, m) == 1,
        "a - 1 es divisible por todos los factores primos de m": all(
            (a - 1) % p == 0 for p in prime_factors(m)
        ),
        "si 4 divide a m, 4 divide a a - 1": m % 4 != 0 or (a - 1) % 4 == 0,
    }


def find_period(a: int, c: int, m: int, seed: int) -> int:
    """Longitud del ciclo en que cae la secuencia (recorrido exhaustivo, solo para m pequeño)."""
    seen = {}
    x = seed
    step = 0
    while x not in seen:
        seen[x] = step
        x = (a * x + c) % m
        step += 1
    return step - seen[x]


def first_repetition(states: list[int]) -> int | None:
    """Índice (base 1) del primer valor repetido dentro de la muestra, o None si no hay."""
    seen = set()
    for index, x in enumerate(states, start=1):
        if x in seen:
            return index
        seen.add(x)
    return None
