"""Experimentos de la práctica: configuraciones del generador y tamaños de muestra, en Python y Java."""

import time
from dataclasses import dataclass
from pathlib import Path

from .config import TIMING_REPEATS, LcgConfig
from .java_runner import JavaRun, run_java_states, run_java_tests
from .lcg import generate, lcg_states
from .uniformity import ChiSquareResult, KsResult, chi_square_test, ks_test


@dataclass(frozen=True)
class PythonRun:
    chi: ChiSquareResult
    ks: KsResult
    seconds: float


@dataclass(frozen=True)
class Row:
    """Una fila de las tablas: misma configuración y mismo N en ambos lenguajes."""

    config: LcgConfig
    n: int
    python: PythonRun
    java: JavaRun


def run_python(config: LcgConfig, n: int, repeats: int = TIMING_REPEATS) -> PythonRun:
    """Mide generación + ambas pruebas, como en Java, y conserva la menor de las repeticiones."""
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        values = generate(config, n)
        chi = chi_square_test(values)
        ks = ks_test(values)
        best = min(best, time.perf_counter() - start)
    return PythonRun(chi, ks, best)


def run_row(config: LcgConfig, n: int, build_dir: Path) -> Row:
    return Row(config, n, run_python(config, n), run_java_tests(config, n, build_dir))


def sequence_mismatches(config: LcgConfig, n: int, build_dir: Path) -> int:
    """Cantidad de posiciones donde X(n) de Python y de Java difieren."""
    python_states = lcg_states(config, n)
    java_states = run_java_states(config, n, build_dir)
    if len(python_states) != len(java_states):
        return max(len(python_states), len(java_states))
    return sum(p != j for p, j in zip(python_states, java_states))


def max_statistic_difference(row: Row) -> float:
    """Mayor diferencia absoluta entre los estadísticos y valores p de ambos programas."""
    py, java = row.python, row.java
    return max(abs(py.chi.statistic - java.chi2), abs(py.chi.p_value - java.p_chi2),
               abs(py.ks.statistic - java.d), abs(py.ks.p_value - java.p_ks))
