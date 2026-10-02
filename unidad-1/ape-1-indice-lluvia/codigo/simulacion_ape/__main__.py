"""Entry point: runs both models, prints the tables and saves the figures."""

from .analysis import compare, rainy_hours
from .config import FIGURES_DIR
from .model import tf_continuous, tf_table
from .reporting import plot_comparison, plot_contributions, plot_inputs, table
from .simulation import run


def main():
    base, adjusted = run(tf_table), run(tf_continuous)
    print(table(base, "Modelo base (Tf por tabla)"), end="\n\n")
    print(table(adjusted, "Modelo ajustado (Tf continuo)"), end="\n\n")

    summary = compare(base, adjusted)
    print("Horas con lluvia probable o lluvia:", ", ".join(rainy_hours(adjusted)))
    print("Diferencia máxima del índice entre modelos:", summary["max_abs_diff"])
    print("Horas que cambian de estado:", ", ".join(summary["changed_states"]) or "ninguna")

    FIGURES_DIR.mkdir(exist_ok=True)
    plot_inputs(base, FIGURES_DIR / "entradas.png")
    plot_contributions(base, FIGURES_DIR / "contribuciones.png")
    plot_comparison(base, adjusted, FIGURES_DIR / "comparacion.png")
    print(f"Figuras guardadas en {FIGURES_DIR}/")


if __name__ == "__main__":
    main()
