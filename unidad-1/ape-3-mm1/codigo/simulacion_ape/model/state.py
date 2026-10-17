"""Estado del sistema en un instante: qué clientes esperan, quién está en la caja y quién se va."""

from bisect import bisect_right
from dataclasses import dataclass

from .queue_system import CustomerRecord


@dataclass(frozen=True)
class SystemState:
    time: float
    waiting: tuple[int, ...]  # ids en la cola, del primero al último (FIFO)
    in_service: int | None  # id del cliente que atiende la caja
    leaving: tuple[int, ...]  # ids que ya pagaron y caminan a la salida
    arrived: int
    served: int
    mean_wait: float | None  # espera promedio de quienes ya pasaron a la caja


def state_at(customers: list[CustomerRecord], time: float, exit_window: float = 0.0) -> SystemState:
    """`customers` debe estar en orden de llegada; `exit_window` es cuánto tiempo se ve a un cliente salir."""
    arrived = customers[: bisect_right([record.arrival for record in customers], time)]
    waiting, leaving, waits = [], [], []
    in_service = None
    served = 0
    for record in arrived:
        if record.service_start is None or record.service_start > time:
            waiting.append(record.customer_id)
            continue
        waits.append(record.wait)
        if record.departure is None or record.departure > time:
            in_service = record.customer_id
            continue
        served += 1
        if time - record.departure <= exit_window:
            leaving.append(record.customer_id)
    return SystemState(
        time=time,
        waiting=tuple(waiting),
        in_service=in_service,
        leaving=tuple(leaving),
        arrived=len(arrived),
        served=served,
        mean_wait=sum(waits) / len(waits) if waits else None,
    )
