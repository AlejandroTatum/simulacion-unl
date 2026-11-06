"""Controlador: genera las secuencias, aplica Chi-cuadrado y K-S en Python y Java y compara."""

import argparse
import csv
from pathlib import Path

from ..model.config import ALPHA, CONFIGS, GLIBC, N, SIZES, SMALL_MODULUS
from ..model.experiment import Row, max_statistic_difference, run_row, sequence_mismatches
from ..model.java_runner import compile_java
from ..model.lcg import generate
from ..model.uniformity import decision
from ..view import console_view

CODE_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = CODE_DIR / "resultados"
FIGURES_DIR = CODE_DIR / "figuras"
BUILD_DIR = RESULTS_DIR / "java-build"

# Muestra pequeña para que se vean los escalones de la FDE (como la visual 2 de las diapositivas, N = 200).
ECDF_SAMPLE = 200


def write_rows_csv(path: Path, rows: list[Row]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["generador", "N", "chi2", "gl", "p_chi2", "decision_chi2", "D_mas", "D_menos", "D",
                         "p_ks", "decision_ks", "tiempo_python_s", "tiempo_java_s", "dif_max_python_java"])
        for row in rows:
            py = row.python
            writer.writerow([row.config.name, row.n, py.chi.statistic, py.chi.df, py.chi.p_value,
                             decision(py.chi.p_value), py.ks.d_plus, py.ks.d_minus, py.ks.statistic,
                             py.ks.p_value, decision(py.ks.p_value), py.seconds, row.java.seconds,
                             max_statistic_difference(row)])


def write_frequencies_csv(path: Path, rows: list[Row]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["generador", "intervalo", "observada_python", "observada_java", "esperada"])
        for row in rows:
            chi = row.python.chi
            k = len(chi.observed)
            for i, (o_py, o_java) in enumerate(zip(chi.observed, row.java.observed)):
                writer.writerow([row.config.name, f"[{i / k:.1f}, {(i + 1) / k:.1f})", o_py, o_java, chi.expected])


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="APE 6: validación con Chi-cuadrado y Kolmogorov-Smirnov")
    parser.add_argument("--no-figures", action="store_true", help="no genera las gráficas")
    args = parser.parse_args(argv)

    RESULTS_DIR.mkdir(exist_ok=True)
    compile_java(BUILD_DIR)

    config_rows = [run_row(config, N, BUILD_DIR) for config in CONFIGS]
    mismatches = {config.name: sequence_mismatches(config, N, BUILD_DIR) for config in CONFIGS}
    console_view.show_frequencies(config_rows[0])
    console_view.show_configurations(config_rows, mismatches)

    size_rows = [run_row(GLIBC, n, BUILD_DIR) for n in SIZES]
    console_view.show_sizes(size_rows)

    write_rows_csv(RESULTS_DIR / "configuraciones.csv", config_rows)
    write_rows_csv(RESULTS_DIR / "tamanos.csv", size_rows)
    write_frequencies_csv(RESULTS_DIR / "frecuencias.csv", config_rows)

    if not args.no_figures:
        from ..view import figures

        FIGURES_DIR.mkdir(exist_ok=True)
        figures.plot_frequencies(config_rows, FIGURES_DIR / "frecuencias.png")
        figures.plot_ecdf([(GLIBC.name, generate(GLIBC, ECDF_SAMPLE)),
                           (SMALL_MODULUS.name, generate(SMALL_MODULUS, ECDF_SAMPLE))],
                          FIGURES_DIR / "fde-ks.png")
        figures.plot_p_values(size_rows, ALPHA, FIGURES_DIR / "valores-p.png")
        print(f"\nFiguras en {FIGURES_DIR}")
    print(f"CSV en {RESULTS_DIR}")
