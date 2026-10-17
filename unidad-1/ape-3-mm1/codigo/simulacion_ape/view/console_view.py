"""Vista de consola: tabla comparativa teórico vs. simulado por escenario."""

from ..model.simulation import ScenarioResult

METRIC_ROWS = (
    ("ρ   utilización del servidor", "utilization"),
    ("L   clientes en el sistema", "mean_in_system"),
    ("Lq  clientes en la cola", "mean_in_queue"),
    ("W   tiempo en el sistema (min)", "mean_time_in_system"),
    ("Wq  tiempo de espera en cola (min)", "mean_wait"),
)


def format_comparison(result: ScenarioResult) -> str:
    scenario = result.scenario
    lines = [
        f"{scenario.label}  (λ = {scenario.arrival_rate}, μ = {scenario.service_rate} clientes/min)",
        f"  Clientes simulados: {len(result.customers)} en {result.sim_time:,.0f} minutos",
        f"  {'Métrica':<36}{'Teórico':>10}{'Simulado':>11}{'Error %':>10}",
    ]
    for label, field in METRIC_ROWS:
        theory, simulated = getattr(result.theory, field), getattr(result.simulated, field)
        error = abs(simulated - theory) / theory * 100
        lines.append(f"  {label:<36}{theory:>10.3f}{simulated:>11.3f}{error:>9.1f}%")
    return "\n".join(lines)


def show_comparison(results: list[ScenarioResult]) -> None:
    for result in results:
        print(format_comparison(result))
        print()


def show_unstable(label: str, arrival_rate: float, service_rate: float) -> None:
    print(f"{label}: el sistema no es estable (λ = {arrival_rate} ≥ μ = {service_rate}); la cola crece sin límite.")


def show_message(message: str) -> None:
    print(message)


def show_no_display() -> None:
    print(
        "No hay ventana gráfica disponible: Matplotlib usa un backend sin pantalla (Agg).\n"
        "Instale Tk y vuelva a ejecutar: en Linux `sudo apt install python3-tk` (Debian/Ubuntu) o\n"
        "`sudo pacman -S tk` (Arch); en Windows y macOS Tk ya viene con Python.\n"
        "Mientras tanto, `--sin-animacion` muestra la tabla y guarda las gráficas."
    )
