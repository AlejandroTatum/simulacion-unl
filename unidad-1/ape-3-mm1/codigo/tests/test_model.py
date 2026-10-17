"""Pruebas del modelo: fórmulas teóricas, simulación SimPy, métricas y estado del sistema."""

import math

import pytest

from simulacion_ape.model.analysis import (
    interarrival_times,
    occupancy_trace,
    records_until,
    service_times,
    simulated_metrics,
    time_average,
)
from simulacion_ape.model.config import SCENARIOS, SimulationConfig
from simulacion_ape.model.queue_system import CustomerRecord, simulate_mm1
from simulacion_ape.model.simulation import run_scenario
from simulacion_ape.model.state import state_at
from simulacion_ape.model.theory import UnstableSystemError, theoretical_metrics


def test_theoretical_metrics_of_scenario_1():
    metrics = theoretical_metrics(2.0, 3.0)
    assert metrics.utilization == pytest.approx(2 / 3)
    assert metrics.mean_in_system == pytest.approx(2.0)
    assert metrics.mean_in_queue == pytest.approx(4 / 3)
    assert metrics.mean_time_in_system == pytest.approx(1.0)
    assert metrics.mean_wait == pytest.approx(2 / 3)


@pytest.mark.parametrize("arrival_rate", [3.0, 3.5])
def test_unstable_system_is_rejected(arrival_rate):
    with pytest.raises(UnstableSystemError, match="no es estable"):
        theoretical_metrics(arrival_rate, 3.0)


def test_same_seed_reproduces_customers():
    assert simulate_mm1(2.0, 3.0, 200, seed=7) == simulate_mm1(2.0, 3.0, 200, seed=7)


def test_single_server_attends_in_fifo_order():
    customers = simulate_mm1(2.9, 3.0, 500, seed=3)
    served = [record for record in customers if record.departure is not None]
    previous_departure = 0.0
    for record in served:
        # Empieza cuando llega o cuando el anterior se va, lo que ocurra después.
        assert record.service_start == pytest.approx(max(record.arrival, previous_departure))
        previous_departure = record.departure


@pytest.mark.parametrize("scenario", SCENARIOS[:2], ids=lambda scenario: f"escenario-{scenario.number}")
def test_simulation_converges_to_theory(scenario):
    result = run_scenario(scenario, SimulationConfig(sim_time=50_000, seed=1))
    for field in ("utilization", "mean_in_system", "mean_in_queue", "mean_time_in_system", "mean_wait"):
        theory, simulated = getattr(result.theory, field), getattr(result.simulated, field)
        assert simulated == pytest.approx(theory, rel=0.1), field


def test_occupancy_is_time_weighted():
    customers = [CustomerRecord(1, 1.0, 1.0, 3.0), CustomerRecord(2, 2.0, 3.0, 4.0)]
    trace = occupancy_trace(customers, end_time=5.0)
    # 1 cliente en [1, 2), 2 en [2, 3), 1 en [3, 4): (1 + 2 + 1) / 5
    assert time_average(trace.times, trace.in_system, 5.0) == pytest.approx(0.8)
    assert time_average(trace.times, trace.in_queue, 5.0) == pytest.approx(0.2)
    metrics = simulated_metrics(customers, 5.0)
    assert metrics.utilization == pytest.approx(0.6)
    assert metrics.mean_wait == pytest.approx(0.5)


def test_records_until_hides_future_events():
    customers = [CustomerRecord(1, 1.0, 1.0, 3.0), CustomerRecord(2, 2.0, 3.0, 4.0), CustomerRecord(3, 6.0, 6.0, 7.0)]
    assert records_until(customers, 3.5) == [CustomerRecord(1, 1.0, 1.0, 3.0), CustomerRecord(2, 2.0, 3.0, None)]
    assert customers[1].departure == 4.0  # no modifica los registros originales
    assert interarrival_times(customers, 3.5) == pytest.approx([1.0, 1.0])
    assert service_times(customers, 3.5) == pytest.approx([2.0])


def test_live_metrics_before_anyone_is_served_are_undefined():
    metrics = simulated_metrics(records_until([CustomerRecord(1, 1.0, 2.0, 3.0)], 1.5), 1.5)
    assert metrics.mean_in_queue == pytest.approx(1 / 3)
    assert math.isnan(metrics.mean_wait) and math.isnan(metrics.mean_time_in_system)


def test_state_at_shows_queue_service_and_exit():
    customers = [
        CustomerRecord(1, 1.0, 1.0, 3.0),
        CustomerRecord(2, 2.0, 3.0, 4.0),
        CustomerRecord(3, 2.5, 4.0, None),
    ]
    state = state_at(customers, 2.6)
    assert (state.waiting, state.in_service, state.served, state.arrived) == ((2, 3), 1, 0, 3)
    state = state_at(customers, 3.2, exit_window=0.5)
    assert (state.waiting, state.in_service, state.leaving) == ((3,), 2, (1,))
    assert state_at(customers, 0.5).arrived == 0
