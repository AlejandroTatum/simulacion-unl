"""Modelo: métricas simuladas a partir de los registros de clientes.

Hay dos tipos de promedio:
- L, Lq y ρ son promedios **en el tiempo**: cada valor se pondera por cuánto tiempo duró (área bajo la curva
  de clientes dividida por el tiempo total).
- W y Wq son promedios **por cliente**: se suma lo que esperó cada cliente y se divide entre cuántos fueron.
"""

from dataclasses import dataclass, replace

import numpy as np

from .queue_system import CustomerRecord
from .theory import QueueMetrics


@dataclass(frozen=True)
class OccupancyTrace:
    """Función escalonada: desde times[i] hasta times[i + 1] hay in_system[i] clientes y in_queue[i] en cola."""

    times: np.ndarray
    in_system: np.ndarray
    in_queue: np.ndarray


def occupancy_trace(customers: list[CustomerRecord], end_time: float) -> OccupancyTrace:
    """Cuenta clientes en el sistema y en la cola después de cada evento hasta `end_time`."""
    # Cada evento cambia los conteos: llegar suma 1 al sistema y a la cola; pasar a la caja saca 1 de la cola;
    # irse saca 1 del sistema. Acumulando los cambios en orden de tiempo se obtiene la función escalonada.
    events = []  # (tiempo, cambio en el sistema, cambio en la cola)
    for record in customers:
        if record.arrival <= end_time:
            events.append((record.arrival, 1, 1))
        if record.service_start is not None and record.service_start <= end_time:
            events.append((record.service_start, 0, -1))
        if record.departure is not None and record.departure <= end_time:
            events.append((record.departure, -1, 0))
    events.sort(key=lambda event: event[0])
    times = np.array([0.0] + [event[0] for event in events])
    in_system = np.concatenate(([0], np.cumsum([event[1] for event in events], dtype=int)))
    in_queue = np.concatenate(([0], np.cumsum([event[2] for event in events], dtype=int)))
    return OccupancyTrace(times, in_system, in_queue)


def time_average(times: np.ndarray, values: np.ndarray, end_time: float) -> float:
    """Promedio ponderado por tiempo de una función escalonada en [0, end_time]: área bajo la curva / tiempo."""
    durations = np.diff(np.append(times, end_time))
    return float(np.sum(values * durations) / end_time)


def records_until(customers: list[CustomerRecord], time: float) -> list[CustomerRecord]:
    """Copia de los registros tal como se conocían en el minuto `time` (sin eventos futuros)."""
    known = []
    for record in customers:
        if record.arrival > time:
            break
        started = record.service_start is not None and record.service_start <= time
        departed = record.departure is not None and record.departure <= time
        known.append(replace(record, service_start=record.service_start if started else None,
                             departure=record.departure if departed else None))
    return known


def interarrival_times(customers: list[CustomerRecord], time: float) -> list[float]:
    """Tiempos entre llegadas observados hasta `time` (deben seguir una exponencial de tasa λ)."""
    arrivals = [record.arrival for record in customers if record.arrival <= time]
    return list(np.diff([0.0] + arrivals))


def service_times(customers: list[CustomerRecord], time: float) -> list[float]:
    """Duraciones de atención terminadas hasta `time` (deben seguir una exponencial de tasa μ)."""
    return [record.departure - record.service_start for record in customers
            if record.departure is not None and record.departure <= time]


def wait_times(customers: list[CustomerRecord]) -> list[float]:
    """Tiempo en cola de cada cliente que ya pasó a la caja."""
    return [record.wait for record in customers if record.wait is not None]


def _mean(values: list[float]) -> float:
    """Media de la lista, o NaN si todavía no hay datos."""
    return float(np.mean(values)) if values else float("nan")


def simulated_metrics(customers: list[CustomerRecord], end_time: float) -> QueueMetrics:
    """ρ, L y Lq se promedian en el tiempo; W y Wq se promedian por cliente (NaN si aún no hay datos)."""
    trace = occupancy_trace(customers, end_time)
    # ρ simulado = tiempo con la caja atendiendo / tiempo total.
    busy_time = sum(
        min(record.departure if record.departure is not None else end_time, end_time) - record.service_start
        for record in customers
        if record.service_start is not None
    )
    # W y Wq: promedio por cliente, solo con los que ya pasaron a la caja (Wq) o ya se fueron (W).
    times_in_system = [record.time_in_system for record in customers if record.time_in_system is not None]
    return QueueMetrics(
        utilization=busy_time / end_time,
        mean_in_system=time_average(trace.times, trace.in_system, end_time),
        mean_in_queue=time_average(trace.times, trace.in_queue, end_time),
        mean_time_in_system=_mean(times_in_system),
        mean_wait=_mean(wait_times(customers)),
    )


def running_mean_wait(customers: list[CustomerRecord]) -> np.ndarray:
    """Espera promedio acumulada cliente a cliente (muestra cómo converge hacia Wq)."""
    waits = np.array(wait_times(customers))
    return np.cumsum(waits) / np.arange(1, len(waits) + 1)
