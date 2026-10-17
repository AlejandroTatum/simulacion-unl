"""Modelo: métricas teóricas del M/M/1 (estado estable, válidas solo si λ < μ).

λ: clientes que llegan por minuto, μ: clientes que la caja atiende por minuto.
"""

from dataclasses import dataclass


class UnstableSystemError(ValueError):
    """λ ≥ μ: la cola crece sin límite y no existen valores de estado estable."""


@dataclass(frozen=True)
class QueueMetrics:
    """Las cinco métricas del sistema; sirve igual para los valores teóricos y los simulados."""
    utilization: float  # ρ
    mean_in_system: float  # L
    mean_in_queue: float  # Lq
    mean_time_in_system: float  # W
    mean_wait: float  # Wq


def is_stable(arrival_rate: float, service_rate: float) -> bool:
    """El sistema tiene estado estable solo si la caja atiende más rápido de lo que llegan (ρ < 1)."""
    return arrival_rate < service_rate


def theoretical_metrics(arrival_rate: float, service_rate: float) -> QueueMetrics:
    """Fórmulas cerradas del M/M/1; lanza `UnstableSystemError` si λ ≥ μ."""
    lam, mu = arrival_rate, service_rate
    if not is_stable(lam, mu):
        raise UnstableSystemError(f"El sistema no es estable: λ = {lam} ≥ μ = {mu}")
    return QueueMetrics(
        utilization=lam / mu,  # ρ = λ/μ: fracción del tiempo que la caja está ocupada
        mean_in_system=lam / (mu - lam),  # L = λ/(μ−λ) = ρ/(1−ρ)
        mean_in_queue=lam**2 / (mu * (mu - lam)),  # Lq = λ²/(μ(μ−λ)) = L − ρ
        mean_time_in_system=1 / (mu - lam),  # W = 1/(μ−λ), de la ley de Little: L = λW
        mean_wait=lam / (mu * (mu - lam)),  # Wq = λ/(μ(μ−λ)) = W − 1/μ, también Lq = λWq
    )
