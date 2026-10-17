"""Modelo: estado del sistema en un instante: qué clientes esperan, quién está en la caja y quién se va."""

from bisect import bisect_right
from dataclasses import dataclass

from .queue_system import CustomerRecord


@dataclass(frozen=True)
class SystemState:
    """Foto del sistema en el minuto `time`."""
    time: float
    waiting: tuple[int, ...]  # ids en la cola, del primero al último (FIFO)
    in_service: int | None  # id del cliente que atiende la caja
    leaving: tuple[int, ...]  # ids que ya pagaron y caminan a la salida
    arrived: int
    served: int


def state_at(customers: list[CustomerRecord], time: float, exit_window: float = 0.0) -> SystemState:
    """Reconstruye la foto en `time` con los registros (en orden de llegada); `exit_window` es cuánto se ve salir a un cliente."""
    # Los registros ya traen todos sus tiempos: se comparan con `time` para saber qué había ocurrido.
    arrived = customers[: bisect_right([record.arrival for record in customers], time)]
    waiting, leaving = [], []
    in_service = None
    served = 0
    for record in arrived:
        if record.service_start is None or record.service_start > time:
            waiting.append(record.customer_id)
        elif record.departure is None or record.departure > time:
            in_service = record.customer_id
        else:
            served += 1
            if time - record.departure <= exit_window:
                leaving.append(record.customer_id)
    return SystemState(time, tuple(waiting), in_service, tuple(leaving), len(arrived), served)
