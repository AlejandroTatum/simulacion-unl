"""Vista de consola: tablas y resumen en texto."""

from ..model.config import CLOUDINESS, HOURS, HUMIDITY, TEMPERATURE


def table(result, title):
    lines = [title, f"{'Hora':<6} {'Hum':>4} {'Nub':>4} {'Temp':>5} {'H':>5} {'N':>5} {'Tf':>5} {'I':>6}  Estado"]
    for k, hour in enumerate(HOURS):
        lines.append(
            f"{hour:<6} {HUMIDITY[k]:>4} {CLOUDINESS[k]:>4} {TEMPERATURE[k]:>5} "
            f"{result['H'][k]:>5.2f} {result['N'][k]:>5.2f} {result['Tf'][k]:>5.2f} "
            f"{result['index'][k]:>6.4f}  {result['state'][k]}"
        )
    return "\n".join(lines)


def show_tables(base, adjusted):
    print(table(base, "Modelo base (Tf por tabla)"), end="\n\n")
    print(table(adjusted, "Modelo ajustado (pesos 0.4, 0.4, 0.2 y Tf continuo)"), end="\n\n")


def show_summary(rainy, summary):
    print("Horas con lluvia probable o lluvia:", ", ".join(rainy))
    print("Diferencia máxima del índice entre modelos:", summary["max_abs_diff"])
    print("Horas que cambian de estado:", ", ".join(summary["changed_states"]) or "ninguna")


def show_figures_saved(figures_dir):
    print(f"Figuras guardadas en {figures_dir}/")
