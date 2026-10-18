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


def test_running_wait_legend_groups_each_scenario_in_its_own_column(tmp_path, monkeypatch):
    """La leyenda de convergencia muestra cada escenario en una columna: simulado arriba y su Wq teórico abajo."""
    from simulacion_ape.view import chart_view

    figures = []
    monkeypatch.setattr(chart_view, "_save", lambda fig, path: figures.append(fig) or path)
    results = [run_scenario(scenario, SimulationConfig(sim_time=300.0)) for scenario in SCENARIOS]
    chart_view.plot_running_wait(results, tmp_path / "convergencia_espera.png")

    legend = figures[0].axes[0].get_legend()
    labels = [text.get_text() for text in legend.get_texts()]
    assert legend._ncols == len(results)
    for column, result in enumerate(results):
        assert labels[2 * column] == f"Escenario {result.scenario.number} simulado"
        assert labels[2 * column + 1] == f"Wq teórico = {result.theory.mean_wait:.2f} min"


def test_comparison_chart_uses_two_rows_so_it_stays_readable_in_the_report(tmp_path, monkeypatch):
    """La comparación ocupa dos filas de paneles (no una tira) para que sus ejes se lean en el informe."""
    from simulacion_ape.view import chart_view

    figures = []
    monkeypatch.setattr(chart_view, "_save", lambda fig, path: figures.append(fig) or path)
    results = [run_scenario(scenario, SimulationConfig(sim_time=300.0)) for scenario in SCENARIOS]
    chart_view.plot_comparison(results, tmp_path / "comparacion_teorico_simulado.png")

    plotted = [ax for ax in figures[0].axes if ax.axison]
    assert [ax.get_title() for ax in plotted] == ["ρ", "L", "Lq", "W", "Wq"]
    assert {ax.get_subplotspec().rowspan.start for ax in plotted} == {0, 1}
    width, height = figures[0].get_size_inches()
    assert width / height < 2
