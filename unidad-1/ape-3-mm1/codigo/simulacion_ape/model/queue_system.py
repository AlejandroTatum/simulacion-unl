"""Modelo: el sistema M/M/1 en SimPy: llegadas de Poisson, servicio exponencial y un único servidor FIFO.

Conceptos de SimPy que usa este archivo:
- `Environment`: el reloj y la agenda de eventos de la simulación (`env.now` es el minuto actual).
- `Resource(capacity=1)`: la caja; solo un cliente a la vez, los demás esperan en su cola FIFO.
- Proceso: una función generadora que SimPy ejecuta; cada `yield` la pausa hasta que ocurra ese evento.
- `request()`: pedir la caja; `yield request` espera hasta que llegue el turno.
- `timeout(t)`: dejar pasar `t` minutos de tiempo simulado (llegada del siguiente cliente, duración del cobro).
- `env.run(until=T)`: avanza el reloj hasta el minuto T.

Un proceso de Poisson de tasa λ tiene tiempos entre llegadas exponenciales de media 1/λ; el servicio
exponencial de tasa μ dura en promedio 1/μ. Por eso se sortea `exponential(1 / tasa)`.
"""

from dataclasses import dataclass

import numpy as np
import simpy


@dataclass
class CustomerRecord:
    """Registro de un cliente: cuándo llega, cuándo pasa a la caja y cuándo se va."""

    customer_id: int
    arrival: float
    service_start: float | None = None
    departure: float | None = None

    @property
    def wait(self) -> float | None:
        """Tiempo en la cola (Wq de este cliente)."""
        return None if self.service_start is None else self.service_start - self.arrival

    @property
    def time_in_system(self) -> float | None:
        """Tiempo total en el sistema (W de este cliente)."""
        return None if self.departure is None else self.departure - self.arrival


def simulate_mm1(arrival_rate: float, service_rate: float, sim_time: float, seed: int) -> list[CustomerRecord]:
    """Ejecuta el sistema durante `sim_time` minutos y devuelve los clientes en orden de llegada."""
    # Flujos aleatorios independientes para llegadas y servicios: con la misma semilla,
    # todos los escenarios reciben la misma secuencia base (números aleatorios comunes).
    arrival_rng, service_rng = np.random.default_rng(seed).spawn(2)
    env = simpy.Environment()
    cashier = simpy.Resource(env, capacity=1)  # una sola caja
    customers: list[CustomerRecord] = []

    def customer(record: CustomerRecord):
        """Un cliente: pide la caja, espera su turno, es atendido y se va."""
        with cashier.request() as request:
            yield request  # espera hasta que la caja quede libre
            record.service_start = env.now
            yield env.timeout(service_rng.exponential(1 / service_rate))  # duración del cobro, media 1/μ
            record.departure = env.now

    def arrivals():
        """Genera clientes sin parar; cada uno nace como un proceso independiente."""
        customer_id = 0
        while True:
            yield env.timeout(arrival_rng.exponential(1 / arrival_rate))  # tiempo hasta la próxima llegada, media 1/λ
            customer_id += 1
            record = CustomerRecord(customer_id, env.now)
            customers.append(record)
            env.process(customer(record))

    env.process(arrivals())  # registra el proceso de llegadas en la agenda
    env.run(until=sim_time)  # ejecuta los eventos hasta el minuto sim_time
    return customers
