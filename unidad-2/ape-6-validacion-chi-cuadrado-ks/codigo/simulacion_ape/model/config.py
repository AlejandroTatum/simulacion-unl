"""Parámetros del generador y de las pruebas, separados de la lógica que los usa."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LcgConfig:
    """Una configuración del LCG: X(n+1) = (a · X(n) + c) mod m, con semilla X0."""

    name: str
    a: int
    c: int
    m: int
    seed: int


# LCG de glibc: el mismo de la diapositiva 17 (ejemplo computacional, N = 10 000).
GLIBC = LcgConfig("glibc", 1_103_515_245, 12_345, 2**32, 1)
# Parámetros de la APE 5 (Numerical Recipes).
APE5 = LcgConfig("APE 5", 1_664_525, 1_013_904_223, 2**32, 12_345)
# RANDU (IBM, años 60): uniforme en una dimensión, pero sus tríos caen en 15 planos.
RANDU = LcgConfig("RANDU", 65_539, 0, 2**31, 1)
# Módulo pequeño: período 16, solo 16 valores posibles en [0, 1).
SMALL_MODULUS = LcgConfig("Módulo pequeño", 5, 3, 16, 7)

CONFIGS = (GLIBC, APE5, RANDU, SMALL_MODULUS)

# Cantidad de números de la actividad 1 y tamaños de la tabla de resultados esperados.
N = 10_000
SIZES = (1_000, 10_000, 100_000, 1_000_000)

# Diez subintervalos de igual amplitud (gl = 9) y nivel de significancia de la guía.
BINS = 10
ALPHA = 0.05

# Repeticiones de cada medición de tiempo; se informa la menor en ambos lenguajes.
TIMING_REPEATS = 3
