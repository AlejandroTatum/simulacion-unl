"""Modelo: motor de corridas; simula un escenario y reúne sus resultados teóricos y simulados."""

from dataclasses import dataclass

from .analysis import simulated_metrics
from .config import Scenario, SimulationConfig
from .queue_system import CustomerRecord, simulate_mm1
from .theory import QueueMetrics, theoretical_metrics


@dataclass(frozen=True)
class ScenarioResult:
    """Todo lo que las vistas necesitan de un escenario ya simulado."""
    scenario: Scenario
    customers: list[CustomerRecord]
    theory: QueueMetrics
    simulated: QueueMetrics
    sim_time: float


def run_scenario(scenario: Scenario, config: SimulationConfig) -> ScenarioResult:
    """Calcula la teoría y simula; lanza UnstableSystemError si λ ≥ μ, antes de simular (como indica el pseudocódigo)."""
    theory = theoretical_metrics(scenario.arrival_rate, scenario.service_rate)
    customers = simulate_mm1(scenario.arrival_rate, scenario.service_rate, config.sim_time, config.seed)
    return ScenarioResult(scenario, customers, theory, simulated_metrics(customers, config.sim_time), config.sim_time)
