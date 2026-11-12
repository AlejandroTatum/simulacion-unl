"""Ejecuta un experimento en Python y en Java con los mismos parámetros y junta ambos resultados."""

import time
from dataclasses import dataclass
from pathlib import Path

from .config import TIMING_REPEATS, Experiment
from .java_runner import run_java
from .lcg import Lcg, LcgConfig
from .measurement import Measurement


@dataclass(frozen=True)
class Row:
    experiment: Experiment
    n: int
    python: Measurement
    java: Measurement

    @property
    def same_result(self) -> bool:
        """Verdadero si los dos lenguajes contaron los mismos aciertos."""
        return self.python.hits == self.java.hits


def run_python(experiment: Experiment, config: LcgConfig, n: int,
               repeats: int = TIMING_REPEATS) -> Measurement:
    """Cada repetición arranca de la misma semilla, así que solo cambia el tiempo."""
    best = float("inf")
    hits = 0
    for _ in range(repeats):
        start = time.perf_counter()
        hits = experiment.count_hits(Lcg(config), n)
        best = min(best, time.perf_counter() - start)
    estimate = experiment.estimate(hits, n)
    return Measurement(hits, estimate, abs(experiment.exact - estimate), best)


def run_row(experiment: Experiment, config: LcgConfig, n: int, build_dir: Path) -> Row:
    return Row(experiment, n, run_python(experiment, config, n), run_java(experiment, config, n, build_dir))
