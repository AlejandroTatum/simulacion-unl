"""Controlador: ejecuta los dos experimentos en Python y Java, y entrega los resultados a las vistas."""

import argparse
import csv
from pathlib import Path

from ..model.config import DEFAULT_LCG, DICE, EXPERIMENTS, PI, SCATTER_POINTS, SIZES
from ..model.experiment import Row, run_row
from ..model.java_runner import compile_java
from ..model.lcg import Lcg
from ..model.monte_carlo import dice_sum_counts, dice_sum_probability, sample_points
from ..view import console_view

CODE_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = CODE_DIR / "resultados"
FIGURES_DIR = CODE_DIR / "figuras"
BUILD_DIR = RESULTS_DIR / "java-build"

# Lanzamientos usados para comparar la distribución completa de la suma con la teórica.
DICE_SUM_SAMPLE = 100_000


def write_rows_csv(path: Path, rows: list[Row]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["experimento", "N", "aciertos_python", "aciertos_java", "estimacion", "valor_real",
                         "error_absoluto", "error_estandar_teorico", "tiempo_python_s", "tiempo_java_s",
                         "mismo_resultado"])
        for row in rows:
            experiment = row.experiment
            writer.writerow([experiment.key, row.n, row.python.hits, row.java.hits, row.python.estimate,
                             experiment.exact, row.python.error, experiment.standard_error(row.n),
                             row.python.seconds, row.java.seconds, row.same_result])


def write_dice_sums_csv(path: Path, counts: dict[int, int]) -> None:
    n = sum(counts.values())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["suma", "veces", "frecuencia", "probabilidad_exacta"])
        for total, count in counts.items():
            writer.writerow([total, count, count / n, dice_sum_probability(total)])


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="APE 7: estimación por el método de Monte Carlo")
    parser.add_argument("--no-figures", action="store_true", help="no genera las gráficas")
    args = parser.parse_args(argv)

    RESULTS_DIR.mkdir(exist_ok=True)
    compile_java(BUILD_DIR)
    console_view.show_header(DEFAULT_LCG)

    groups = [[run_row(experiment, DEFAULT_LCG, n, BUILD_DIR) for n in SIZES] for experiment in EXPERIMENTS]
    for rows in groups:
        console_view.show_rows(rows)

    sums = dice_sum_counts(Lcg(DEFAULT_LCG), DICE_SUM_SAMPLE)
    console_view.show_dice_sums(sums, dice_sum_probability)

    write_rows_csv(RESULTS_DIR / "resultados.csv", [row for rows in groups for row in rows])
    write_dice_sums_csv(RESULTS_DIR / "sumas-dados.csv", sums)

    figures_dir = None
    if not args.no_figures:
        from ..view import figures

        figures_dir = FIGURES_DIR
        figures_dir.mkdir(exist_ok=True)
        figures.plot_circle(sample_points(Lcg(DEFAULT_LCG), SCATTER_POINTS), figures_dir / "circulo.png")
        figures.plot_errors(groups, figures_dir / "error-vs-n.png")
        figures.plot_times(groups, figures_dir / "tiempos.png")
        figures.plot_dice_sums(sums, dice_sum_probability, figures_dir / "sumas-dados.png")
    console_view.show_outputs(RESULTS_DIR, figures_dir)
