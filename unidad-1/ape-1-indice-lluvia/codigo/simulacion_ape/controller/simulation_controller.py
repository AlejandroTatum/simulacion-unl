"""Controlador: ejecuta ambos modelos y pide a las vistas mostrar y guardar los resultados."""

from ..model.analysis import compare, rainy_hours
from ..model.config import ADJUSTED_WEIGHTS, FIGURES_DIR
from ..model.rain_model import tf_continuous, tf_table
from ..model.simulation import run
from ..view import chart_view, console_view


def main():
    base, adjusted = run(tf_table), run(tf_continuous, ADJUSTED_WEIGHTS)
    console_view.show_tables(base, adjusted)
    console_view.show_summary(rainy_hours(adjusted), compare(base, adjusted))

    FIGURES_DIR.mkdir(exist_ok=True)
    chart_view.plot_inputs(base, FIGURES_DIR / "entradas.png")
    chart_view.plot_contributions(base, FIGURES_DIR / "contribuciones.png")
    chart_view.plot_comparison(base, adjusted, FIGURES_DIR / "comparacion.png")
    console_view.show_figures_saved(FIGURES_DIR)
