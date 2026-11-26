"""Vista de consola: imprime las muestras y las tablas comparativas."""

import numpy as np

from ..model.analysis import Comparison
from ..model.config import SimulationConfig


def show_header(config: SimulationConfig) -> None:
    print("APE 8: método de la Transformada Inversa")
    print(f"N = {config.n}   semilla = {config.seed}")


def show_uniform(stats: Comparison) -> None:
    print("\nAlgoritmo 1: uniformes U(0,1)")
    print(f"  media    experimental = {stats.experimental_mean:.6f}   teórica = {stats.theoretical_mean:.6f}"
          f"   error = {stats.mean_error_pct:.4f} %")
    print(f"  varianza experimental = {stats.experimental_variance:.6f}   teórica = {stats.theoretical_variance:.6f}"
          f"   error = {stats.variance_error_pct:.4f} %")


def show_sample(x: np.ndarray, rate: float) -> None:
    print(f"\nAlgoritmo 2: transformada inversa con λ = {rate}")
    print("  primeros 10 valores de X:")
    for i, value in enumerate(x[:10], start=1):
        print(f"    X[{i:>2}] = {value:.6f}")
    print(f"  cantidad de datos generados: {len(x)}")


def show_table(stats: list[Comparison]) -> None:
    print("\nAlgoritmos 4 y 5: medidas experimentales y teóricas")
    print(f"{'λ':>5}  {'media teór.':>11}  {'media exp.':>10}  {'var. teór.':>10}  {'var. exp.':>9}"
          f"  {'error media %':>13}  {'error var. %':>12}")
    for row in stats:
        print(f"{row.label.removeprefix('λ = '):>5}  {row.theoretical_mean:>11.4f}  {row.experimental_mean:>10.4f}"
              f"  {row.theoretical_variance:>10.4f}  {row.experimental_variance:>9.4f}"
              f"  {row.mean_error_pct:>13.4f}  {row.variance_error_pct:>12.4f}")


def show_outputs(results_dir, figures_dir) -> None:
    if figures_dir is not None:
        print(f"\nFiguras en {figures_dir}")
    print(f"CSV en {results_dir}")
