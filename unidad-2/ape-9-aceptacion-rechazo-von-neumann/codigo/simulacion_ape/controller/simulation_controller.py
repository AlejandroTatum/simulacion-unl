"""Controlador: ejecuta las simulaciones, muestra la tabla y guarda CSV y figuras."""

import argparse
from pathlib import Path

import pandas as pd

from ..model.config import SimulationConfig
from ..model.simulation import EfficiencyRow, run
from ..view import console_view

CODE_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = CODE_DIR / "resultados"
FIGURES_DIR = CODE_DIR / "figuras"


def efficiency_frame(rows: list[EfficiencyRow]) -> pd.DataFrame:
    """Tabla de la guía (N, aceptados, rechazados, eficiencia) con la eficiencia teórica y el error."""
    return pd.DataFrame({
        "distribución": [row.target.label for row in rows],
        "N": [row.n for row in rows],
        "aceptados": [row.n_accepted for row in rows],
        "rechazados": [row.n_rejected for row in rows],
        "eficiencia_experimental": [row.efficiency for row in rows],
        "eficiencia_teorica": [row.target.theoretical_efficiency for row in rows],
        "error_absoluto": [row.absolute_error for row in rows],
    })


def main(argv: list[str] | None = None) -> None:
    defaults = SimulationConfig()
    parser = argparse.ArgumentParser(description="APE 9: método de aceptación-rechazo de Von Neumann")
    parser.add_argument("--seed", type=int, default=defaults.seed, help="semilla del generador (42)")
    parser.add_argument("--no-figures", action="store_true", help="no genera las gráficas")
    args = parser.parse_args(argv)

    config = SimulationConfig(seed=args.seed)
    result = run(config)

    console_view.show_header(config.seed)
    console_view.show_table(result.rows)

    RESULTS_DIR.mkdir(exist_ok=True)
    efficiency_frame(result.rows).to_csv(RESULTS_DIR / "eficiencia-python.csv", index=False)

    figures_dir = None
    if not args.no_figures:
        from ..view import figures

        figures_dir = FIGURES_DIR
        figures_dir.mkdir(exist_ok=True)
        for name, sample in result.samples.items():
            figures.plot_histogram(sample, figures_dir / f"histograma-{name}.png")
            figures.plot_candidates(sample, figures_dir / f"aceptados-rechazados-{name}.png")
        figures.plot_efficiency(result.rows, figures_dir / "comparativa-eficiencia.png")
    console_view.show_outputs(RESULTS_DIR, figures_dir)
