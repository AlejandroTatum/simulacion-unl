"""Vista de consola: imprime la tabla de eficiencias."""

from ..model.simulation import EfficiencyRow


def show_header(seed: int) -> None:
    print("APE 9: método de aceptación-rechazo de Von Neumann")
    print(f"distribución propuesta g(x) = 1   semilla = {seed}")


def show_table(rows: list[EfficiencyRow]) -> None:
    print(f"\n{'distribución':<12}  {'N':>6}  {'aceptados':>9}  {'rechazados':>10}  {'E exp. %':>8}"
          f"  {'ET %':>7}  {'error abs.':>10}")
    for row in rows:
        print(f"{row.target.label:<12}  {row.n:>6}  {row.n_accepted:>9}  {row.n_rejected:>10}"
              f"  {row.efficiency:>8.2f}  {row.target.theoretical_efficiency:>7.2f}  {row.absolute_error:>10.2f}")


def show_outputs(results_dir, figures_dir) -> None:
    if figures_dir is not None:
        print(f"\nFiguras en {figures_dir}")
    print(f"CSV en {results_dir}")
