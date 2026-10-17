"""Modelo: datos de la pantalla en vivo, una corrida (λ, μ) lista para consultarla minuto a minuto.

La pantalla no calcula nada: le pide a `LiveRun` el estado y las métricas en el minuto que muestra.
"""

from dataclasses import dataclass

from .analysis import OccupancyTrace, interarrival_times, occupancy_trace, records_until, service_times, simulated_metrics
from .config import Scenario, SimulationConfig
from .queue_system import CustomerRecord, simulate_mm1
from .simulation import run_scenario
from .state import SystemState, state_at
from .theory import QueueMetrics, is_stable


@dataclass(frozen=True)
class LiveRun:
    """Una corrida completa con todas sus consultas; la ventana la recibe ya armada por el controlador."""
    arrival_rate: float
    service_rate: float
    duration: float  # minutos que se reproducen
    customers: list[CustomerRecord]  # solo los que llegan dentro de la reproducción
    theory: QueueMetrics | None  # None si λ ≥ μ (no existe estado estable)
    long_run: QueueMetrics | None  # métricas de la corrida larga (None si λ ≥ μ)
    long_run_minutes: float
    trace: OccupancyTrace  # clientes en el sistema y en la cola durante la reproducción

    @property
    def stable(self) -> bool:
        """Hay teoría solo si λ < μ."""
        return self.theory is not None

    def state_at(self, time: float, exit_window: float) -> SystemState:
        """Quién espera, quién está en la caja y quién sale en el minuto `time`."""
        return state_at(self.customers, time, exit_window)

    def metrics_at(self, time: float) -> QueueMetrics | None:
        """Métricas simuladas con lo ocurrido hasta `time` (None en el minuto 0, sin datos aún)."""
        if time <= 0:
            return None
        return simulated_metrics(records_until(self.customers, time), time)

    def interarrival_times(self, time: float) -> list[float]:
        """Tiempos entre llegadas vistos hasta `time`."""
        return interarrival_times(self.customers, time)

    def service_times(self, time: float) -> list[float]:
        """Duraciones de atención terminadas hasta `time`."""
        return service_times(self.customers, time)


def run_live(arrival_rate: float, service_rate: float, config: SimulationConfig, duration: float) -> LiveRun:
    """Simula con la semilla de `config`; si el sistema es estable, también la corrida larga de `config.sim_time`."""
    if is_stable(arrival_rate, service_rate):
        result = run_scenario(Scenario(0, arrival_rate, service_rate, "En vivo"), config)
        customers, theory, long_run, minutes = result.customers, result.theory, result.simulated, result.sim_time
    else:
        # Con λ ≥ μ no hay teoría ni corrida larga: solo se simula lo que se va a mostrar.
        customers = simulate_mm1(arrival_rate, service_rate, duration, config.seed)
        theory = long_run = None
        minutes = 0.0
    # La corrida larga y la reproducción comparten semilla: los primeros minutos son los mismos clientes.
    shown = [record for record in customers if record.arrival <= duration]
    return LiveRun(arrival_rate, service_rate, duration, shown, theory, long_run, minutes,
                   occupancy_trace(shown, duration))

