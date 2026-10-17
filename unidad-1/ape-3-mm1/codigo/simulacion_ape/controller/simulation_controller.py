"""Controlador: simula los escenarios, muestra la comparación, guarda gráficas y abre la pantalla en vivo."""

import argparse
from functools import lru_cache
from pathlib import Path

from ..model.config import SCENARIOS, AnimationConfig, Scenario, SimulationConfig
from ..model.live import LiveRun, run_live
from ..model.simulation import run_scenario
from ..model.theory import is_stable
from ..view.chart_view import save_charts
from ..view.console_view import show_comparison, show_message, show_no_display, show_unstable
from ..view.live.window import LiveWindow

DEFAULT_OUTPUT = Path(__file__).resolve().parents[2] / "resultados"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m simulacion_ape",
        description="Simulación M/M/1 de una caja rápida de supermercado con SimPy.",
    )
    parser.add_argument("--escenario", type=int, choices=[s.number for s in SCENARIOS], default=1,
                        help="escenario con el que se abre la ventana en vivo (por defecto 1)")
    parser.add_argument("--llegada", type=float, help="λ personalizado (clientes/min); requiere --servicio")
    parser.add_argument("--servicio", type=float, help="μ personalizado (clientes/min); requiere --llegada")
    parser.add_argument("--tiempo", type=float, default=SimulationConfig.sim_time,
                        help="minutos simulados para las métricas (por defecto %(default).0f)")
    parser.add_argument("--semilla", type=int, default=SimulationConfig.seed, help="semilla aleatoria")
    parser.add_argument("--duracion", type=float, default=AnimationConfig.duration,
                        help="minutos del sistema que reproduce la ventana en vivo, sin pasar de --tiempo "
                             "(por defecto %(default).0f)")
    parser.add_argument("--velocidad", type=float, default=AnimationConfig.minutes_per_second,
                        help="minutos simulados por segundo al abrir la ventana (por defecto %(default)s)")
    parser.add_argument("--sin-animacion", action="store_true", help="solo tabla y gráficas, sin abrir la ventana en vivo")
    parser.add_argument("--resultados", type=Path, default=DEFAULT_OUTPUT, help="carpeta de salida de las gráficas")
    args = parser.parse_args(argv)
    if (args.llegada is None) != (args.servicio is None):
        parser.error("--llegada y --servicio se usan juntos")
    if args.duracion > args.tiempo:
        parser.error("--duracion no puede ser mayor que --tiempo")
    return args


def open_live_window(config: SimulationConfig, animation: AnimationConfig, start_rates: tuple[float, float]) -> None:
    """Abre la ventana en vivo; si Matplotlib no tiene backend con ventana, explica cómo habilitarlo."""

    # La ventana pide una corrida cada vez que cambian λ o μ; la memoria evita repetir la que ya se hizo.
    @lru_cache(maxsize=32)
    def make_run(arrival_rate: float, service_rate: float) -> LiveRun:
        return run_live(arrival_rate, service_rate, config, animation.duration)

    window = LiveWindow(make_run, SCENARIOS, start_rates, animation.duration, animation.minutes_per_second)
    if window.is_interactive():
        window.show()
    else:
        show_no_display()


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    scenarios = SCENARIOS
    start = next(scenario for scenario in SCENARIOS if scenario.number == args.escenario)
    start_rates = (start.arrival_rate, start.service_rate)
    if args.llegada is not None:
        scenarios = (Scenario(0, args.llegada, args.servicio, "Personalizado"),)
        start_rates = (args.llegada, args.servicio)
    config = SimulationConfig(sim_time=args.tiempo, seed=args.semilla, scenarios=scenarios)

    results = []
    for scenario in config.scenarios:
        if not is_stable(scenario.arrival_rate, scenario.service_rate):
            show_unstable(scenario.label, scenario.arrival_rate, scenario.service_rate)
            continue
        results.append(run_scenario(scenario, config))
    if results:
        show_comparison(results)
        for path in save_charts(results, args.resultados):
            show_message(f"Gráfica guardada: {path}")

    if not args.sin_animacion:
        open_live_window(config, AnimationConfig(duration=args.duracion, minutes_per_second=args.velocidad), start_rates)
