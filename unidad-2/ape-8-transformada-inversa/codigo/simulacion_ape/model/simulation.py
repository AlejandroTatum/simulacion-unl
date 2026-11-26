"""Motor de la práctica: genera U una sola vez y la transforma con cada λ."""

from dataclasses import dataclass

import numpy as np

from .analysis import Comparison, compare_exponential, compare_uniform
from .config import SimulationConfig
from .inverse_transform import generate_uniforms, inverse_exponential


@dataclass(frozen=True)
class SimulationResult:
    uniforms: np.ndarray
    uniform_stats: Comparison
    samples: dict[float, np.ndarray]     # muestra exponencial X por cada λ
    stats: dict[float, Comparison]       # tabla comparativa por cada λ


def run(config: SimulationConfig) -> SimulationResult:
    """Algoritmos 1, 2, 4 y 5: los mismos U se transforman con cada tasa, como indica la guía."""
    u = generate_uniforms(config.n, config.seed)
    rates = dict.fromkeys((config.rate, *config.rates))
    samples = {rate: inverse_exponential(u, rate) for rate in rates}
    stats = {rate: compare_exponential(x, rate) for rate, x in samples.items()}
    return SimulationResult(u, compare_uniform(u), samples, stats)
