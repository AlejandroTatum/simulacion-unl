import numpy as np

from simulacion_ape.model import classify, rain_index, tf_continuous, tf_table
from simulacion_ape.simulation import run


def test_guide_example_gives_index_081():
    # Ejemplo de la guía: humedad 90 %, nubosidad 80 %, 18 °C -> I = 0.81
    assert rain_index(0.9, 0.8, tf_table(18)) == 0.81


def test_tf_table_matches_guide_and_floors_missing_temperatures():
    temps = np.array([8, 10, 12, 17, 18, 28, 30])
    assert tf_table(temps).tolist() == [1.0, 1.0, 0.9, 0.7, 0.6, 0.1, 0.1]


def test_tf_continuous_interpolates_between_table_rows():
    assert tf_continuous(np.array([15, 17])).tolist() == [0.75, 0.65]


def test_classify_uses_guide_thresholds_inclusive_at_lower_bound():
    states = classify(np.array([0.39, 0.40, 0.60, 0.75]))
    assert states.tolist() == ["Sin lluvia", "Baja posibilidad", "Lluvia probable", "Lluvia"]


def test_run_returns_one_row_per_reading():
    result = run(tf_table)
    assert len(result["index"]) == len(result["state"]) == 9
