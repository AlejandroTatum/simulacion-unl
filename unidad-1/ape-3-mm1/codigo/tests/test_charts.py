"""Pruebas de las gráficas estáticas: se generan los PNG del informe."""

from simulacion_ape.model.config import SCENARIOS, SimulationConfig
from simulacion_ape.model.simulation import run_scenario
from simulacion_ape.view.chart_view import save_charts


def test_save_charts_creates_the_wait_scatter_plot(tmp_path):
    results = [run_scenario(scenario, SimulationConfig(sim_time=300.0)) for scenario in SCENARIOS]
    paths = save_charts(results, tmp_path)
    scatter = tmp_path / "dispersion_espera.png"
    assert scatter in paths
    assert scatter.stat().st_size > 0
