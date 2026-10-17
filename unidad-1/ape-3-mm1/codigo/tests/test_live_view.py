"""Pruebas de la ventana en vivo sin abrir pantalla (backend Agg): lo que muestra coincide con el modelo."""

from functools import lru_cache

import matplotlib.pyplot as plt
import pytest

from simulacion_ape.model.analysis import records_until, simulated_metrics
from simulacion_ape.model.config import SCENARIOS, SimulationConfig
from simulacion_ape.model.live import run_live
from simulacion_ape.model.state import state_at
from simulacion_ape.view.live.board import fmt
from simulacion_ape.view.live.scene import CAPACITY, EXIT_WINDOW
from simulacion_ape.view.live.theme import SIGNAL
from simulacion_ape.view.live.window import LiveWindow

CONFIG = SimulationConfig(sim_time=2000, seed=42)
DURATION = 60.0


@lru_cache
def make_run(arrival_rate, service_rate):
    return run_live(arrival_rate, service_rate, CONFIG, DURATION)


@pytest.fixture
def window():
    live = LiveWindow(make_run, SCENARIOS, (2.0, 3.0), DURATION, speed=1.0)
    yield live
    plt.close(live.fig)


def theory_cells(window):
    return {field: cells[0].get_text() for field, cells in window.board.cells.items()}


def test_window_builds_for_scenario_1(window):
    assert theory_cells(window)["mean_in_system"] == "2.000"
    assert theory_cells(window)["utilization"] == "0.667"
    assert window.board.long_run_header.get_text() == "2\u00a0000 min"
    assert window.board.clock_total.get_text() == "de 60 min"
    assert [button.color == SIGNAL for button in window.preset_buttons] == [True, False, False]
    assert window.lambda_slider.val == pytest.approx(2.0) and window.mu_slider.val == pytest.approx(3.0)
    assert not window.is_interactive()  # con Agg no hay ventana que abrir


def test_sliders_rerun_with_new_rates_and_same_seed(window):
    window.lambda_slider.set_val(2.5)
    window.apply_sliders()  # lo mismo que se ejecuta al soltar el mouse
    assert (window.run.arrival_rate, window.run.service_rate) == (2.5, 3.0)
    assert window.run.customers == make_run(2.5, 3.0).customers
    assert theory_cells(window)["mean_in_system"] == "5.000"  # λ/(μ−λ) con λ = 2.5, μ = 3
    assert window.board.cells["mean_in_system"][2].get_text() == fmt(window.run.long_run.mean_in_system)
    assert "λ = 2.5" in window.scene.params.get_text()


def test_preset_button_sets_sliders(window):
    window.select_preset(SCENARIOS[2])
    assert (window.lambda_slider.val, window.mu_slider.val) == pytest.approx((2.9, 3.0))
    assert window.preset_buttons[2].color == SIGNAL
    assert theory_cells(window)["mean_in_system"] == "29.000"
    assert window.scene.params.get_text().endswith("ρ = λ/μ = 0.967")


def test_unstable_rates_show_message_and_hide_theory(window):
    window.lambda_slider.set_val(3.5)
    window.apply_sliders()
    assert not window.run.stable
    assert window.scene.alert.get_visible()
    assert window.scene.alert.get_text() == "Sistema inestable: λ ≥ μ, la teoría no aplica"
    assert set(theory_cells(window).values()) == {"—"}
    assert window.board.cells["mean_wait"][2].get_text() == "—"
    assert window.board.long_run_header.get_text() == ""
    assert not window.occupancy.theory_system.get_visible()
    window.advance(30.0)  # sigue animando: la cola crece
    assert window.board.cells["mean_in_queue"][1].get_text() != "—"
    assert len(window.run.state_at(30.0, EXIT_WINDOW).waiting) > 0


def test_one_frame_updates_clock_counters_and_metrics_like_the_model(window):
    window.advance(5.0)  # 5 s reales a 1 min/s: minuto 5
    state = state_at(window.run.customers, 5.0, EXIT_WINDOW)
    live = simulated_metrics(records_until(window.run.customers, 5.0), 5.0)
    assert window.board.clock.get_text() == "5.0"
    assert [text.get_text() for text in window.board.counters] == [
        str(len(state.waiting)), str(len(state.waiting) + (state.in_service is not None)),
        str(state.served), str(state.arrived)]
    assert window.board.cells["mean_in_queue"][1].get_text() == fmt(live.mean_in_queue)
    assert window.board.cells["mean_wait"][1].get_text() == fmt(live.mean_wait)
    visible = len(state.waiting) + len(state.leaving) + (state.in_service is not None)
    assert len(window.scene.positions) == visible


def test_animation_stops_at_the_end_and_pause_freezes_the_clock(window):
    window.toggle_play()
    window.advance(10.0)
    assert window.time == 0.0 and window.board.clock.get_text() == "0.0"
    window.toggle_play()
    window.advance(1000.0)
    assert window.time == DURATION and not window.playing
    assert window.play_button.label.get_text() == "Repetir"
    window.toggle_play()  # repetir: vuelve al minuto 0 y reproduce
    assert window.time == 0.0 and window.playing


def test_frame_repaints_only_the_animated_artists(window, monkeypatch):
    window.fig.canvas.draw()  # el dibujo completo guarda el fondo para el blitting
    clock, params = window.board.clock, window.scene.params
    painted = []
    monkeypatch.setattr(clock, "draw", lambda renderer: painted.append("clock"))
    monkeypatch.setattr(params, "draw", lambda renderer: painted.append("params"))
    artists = window.frame(0.1)
    assert artists == window.fast and all(artist.get_animated() for artist in artists)
    assert clock in artists and params not in artists
    assert painted == ["clock"]  # el texto fijo no se vuelve a pintar
    assert clock.get_text() == "0.1"


def test_a_very_full_queue_keeps_figures_on_their_slots_and_counts_the_rest(window):
    window.lambda_slider.set_val(3.5)
    window.apply_sliders()
    window.advance(40.0)  # un solo paso largo: cada figura llega a su lugar
    state = window.run.state_at(window.time, EXIT_WINDOW)
    assert len(state.waiting) > CAPACITY
    spots = [tuple(window.scene.positions[cid]) for cid in state.waiting[:CAPACITY]]
    assert len(set(spots)) == CAPACITY  # ningún par de figuras comparte lugar
    assert not any(cid in window.scene.positions for cid in state.waiting[CAPACITY:])
    assert window.scene.overflow.get_text() == f"+{len(state.waiting) - CAPACITY} esperando fuera de la fila"
