"""Controlador: estima los parámetros, ejecuta los escenarios y pide a las vistas mostrarlos."""

import numpy as np

from ..model.analysis import euler_error, fit_table
from ..model.config import (
    DATA,
    DECREASING_DATA,
    DT,
    DT_VALUES,
    FIGURES_DIR,
    R_VALUES,
    RUNS,
    SEED,
    SIGMA_VALUES,
)
from ..model.estimation import estimate_parameters
from ..model.growth_models import continuous_euler, deterministic
from ..model.simulation import monte_carlo, run_all
from ..view import chart_view, console_view


def main():
    FIGURES_DIR.mkdir(exist_ok=True)
    params = estimate_parameters(DATA)
    p0, r, periods = params["P0"], params["r"], params["periods"]

    # Escenario principal: los cuatro modelos con los parámetros de los datos.
    results = run_all(params, DT, SEED)
    console_view.show_parameters("Parámetros estimados del arreglo de la guía", params)
    console_view.show_fit_table(fit_table(results, DATA), DATA)
    chart_view.plot_models(results, DATA, "Comparación de los cuatro modelos (datos de la guía)",
                           FIGURES_DIR / "comparacion_modelos.png")

    # Arreglo nuevo: la serie invertida produce r < 0 y un decrecimiento.
    decreasing = estimate_parameters(DECREASING_DATA)
    decreasing_results = run_all(decreasing, DT, SEED)
    console_view.show_parameters("Parámetros estimados del arreglo decreciente", decreasing)
    console_view.show_fit_table(fit_table(decreasing_results, DECREASING_DATA), DECREASING_DATA)
    chart_view.plot_models(decreasing_results, DECREASING_DATA, "Decrecimiento: los cuatro modelos con el arreglo invertido",
                           FIGURES_DIR / "decrecimiento.png", "Datos invertidos")

    # Influencia de r.
    t = np.linspace(0, periods, 301)
    curves = {rate: (t, deterministic(p0, rate, t)) for rate in R_VALUES}
    console_view.show_rate_finals({rate: population[-1] for rate, (_, population) in curves.items()})
    chart_view.plot_rate_influence(curves, FIGURES_DIR / "influencia_r.png")

    # Influencia de sigma, con muchas corridas de Monte Carlo.
    bands = {sigma: monte_carlo(p0, r, sigma, periods, RUNS, SEED) for sigma in SIGMA_VALUES}
    console_view.show_noise_spread({sigma: band["p95"][-1] - band["p5"][-1] for sigma, band in bands.items()})
    chart_view.plot_noise_influence(bands, FIGURES_DIR / "influencia_sigma.png")

    # Influencia de dt.
    approximations = {dt: continuous_euler(p0, r, periods, dt) for dt in DT_VALUES}
    console_view.show_euler_errors({dt: euler_error(p0, r, periods, dt) for dt in DT_VALUES})
    chart_view.plot_step_influence((t, deterministic(p0, r, t)), approximations, FIGURES_DIR / "influencia_dt.png")

    console_view.show_figures_saved(FIGURES_DIR)
