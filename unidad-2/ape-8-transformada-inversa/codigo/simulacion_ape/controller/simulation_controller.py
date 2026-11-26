"""Controlador: ejecuta la práctica, muestra los resultados y guarda CSV y figuras."""

import argparse
from pathlib import Path

import pandas as pd

from ..model.analysis import Comparison
from ..model.config import SimulationConfig
from ..model.simulation import run
from ..view import console_view

CODE_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = CODE_DIR / "resultados"
FIGURES_DIR = CODE_DIR / "figuras"


def comparison_frame(rows: list[Comparison], key: str, keys: list) -> pd.DataFrame:
    """Tabla comparativa con las columnas de la guía más los errores porcentuales."""
    return pd.DataFrame({
        key: keys,
        "media_teorica": [row.theoretical_mean for row in rows],
        "media_experimental": [row.experimental_mean for row in rows],
        "varianza_teorica": [row.theoretical_variance for row in rows],
        "varianza_experimental": [row.experimental_variance for row in rows],
        "error_media_pct": [row.mean_error_pct for row in rows],
        "error_varianza_pct": [row.variance_error_pct for row in rows],
    })


def main(argv: list[str] | None = None) -> None:
    defaults = SimulationConfig()
    parser = argparse.ArgumentParser(description="APE 8: método de la Transformada Inversa")
    parser.add_argument("--seed", type=int, default=defaults.seed, help="semilla del generador (42)")
    parser.add_argument("--n", type=int, default=defaults.n, help="tamaño de la muestra (10000)")
    parser.add_argument("--no-figures", action="store_true", help="no genera las gráficas")
    args = parser.parse_args(argv)

    config = SimulationConfig(n=args.n, seed=args.seed)
    result = run(config)

    console_view.show_header(config)
    console_view.show_uniform(result.uniform_stats)
    console_view.show_sample(result.samples[config.rate], config.rate)
    table = [result.stats[rate] for rate in config.rates]
    console_view.show_table(table)

    RESULTS_DIR.mkdir(exist_ok=True)
    comparison_frame(table, "lambda", list(config.rates)).to_csv(
        RESULTS_DIR / "tabla-lambda-python.csv", index=False)
    comparison_frame([result.uniform_stats], "distribucion", ["U(0,1)"]).to_csv(
        RESULTS_DIR / "uniforme-python.csv", index=False)

    figures_dir = None
    if not args.no_figures:
        from ..view import figures

        figures_dir = FIGURES_DIR
        figures_dir.mkdir(exist_ok=True)
        figures.plot_uniform(result.uniforms, figures_dir / "histograma-uniforme.png")
        figures.plot_exponential(result.samples[config.rate], config.rate, figures_dir / "histograma-exponencial.png")
        figures.plot_rates({rate: result.samples[rate] for rate in config.rates}, figures_dir / "comparativa-lambda.png")
    console_view.show_outputs(RESULTS_DIR, figures_dir)
