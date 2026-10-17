"""Modelo: parámetros de la simulación (escenarios, tiempo, semilla), separados de la lógica que los usa.

Unidad de tiempo: minutos. Las tasas λ y μ están en clientes por minuto.
"""

from dataclasses import dataclass

# Sistema real que representa el modelo M/M/1: una sola caja atiende una fila FIFO.
SYSTEM_NAME = "Caja rápida de supermercado"


@dataclass(frozen=True)
class Scenario:
    """Un par (λ, μ) con nombre; `number` 0 marca un escenario personalizado."""
    number: int
    arrival_rate: float  # λ: clientes que llegan por minuto
    service_rate: float  # μ: clientes que la caja atiende por minuto
    condition: str

    @property
    def utilization(self) -> float:
        """ρ = λ/μ: fracción del tiempo que la caja está ocupada."""
        return self.arrival_rate / self.service_rate

    @property
    def label(self) -> str:
        """Título del escenario para tablas y gráficas."""
        return f"Escenario {self.number}: {self.condition}"


# Escenarios de la guía de la práctica.
SCENARIOS = (
    Scenario(1, 2.0, 3.0, "Sistema estable"),
    Scenario(2, 2.5, 3.0, "Mayor utilización"),
    Scenario(3, 2.9, 3.0, "Cerca de saturación"),
)


@dataclass(frozen=True)
class SimulationConfig:
    """Datos de una corrida; la misma semilla da siempre los mismos números aleatorios."""
    sim_time: float = 20_000.0  # minutos simulados para estimar las métricas
    seed: int = 42


@dataclass(frozen=True)
class AnimationConfig:
    """Datos de la ventana en vivo."""
    duration: float = 60.0  # minutos del sistema que se reproducen en la pantalla en vivo
    minutes_per_second: float = 1.0  # velocidad inicial: minutos simulados por segundo real
