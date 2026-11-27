"""Motor de la práctica: tres simulaciones (N = 1000, 5000 y 10000) por cada distribución objetivo."""

from dataclasses import dataclass

from .acceptance_rejection import SamplingResult, acceptance_rejection
from .config import SimulationConfig
from .distributions import TARGETS, TargetDistribution


@dataclass(frozen=True)
class EfficiencyRow:
    """Una fila de la tabla de resultados."""

    target: TargetDistribution
    n: int
    n_accepted: int
    n_rejected: int
    efficiency: float

    @property
    def absolute_error(self) -> float:
        """|E experimental − ET| en puntos porcentuales."""
        return abs(self.efficiency - self.target.theoretical_efficiency)


@dataclass(frozen=True)
class SimulationResult:
    rows: list[EfficiencyRow]
    samples: dict[str, SamplingResult]   # simulación con el mayor N de cada distribución (para las gráficas)


def run(config: SimulationConfig) -> SimulationResult:
    """Cada simulación usa la misma semilla, así cada fila se puede reproducir por separado."""
    rows, samples = [], {}
    largest = max(config.sizes)
    for target in TARGETS:
        for n in config.sizes:
            result = acceptance_rejection(target, n, config.seed)
            rows.append(EfficiencyRow(target, n, result.n_accepted, result.n_rejected, result.efficiency))
            if n == largest:
                samples[target.name] = result
    return SimulationResult(rows, samples)
