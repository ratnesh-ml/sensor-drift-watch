import numpy as np

from monitor import detect_anomalies, generate_stream, population_stability_index, summarize


def test_stream_is_reproducible():
    assert generate_stream(50, seed=4).equals(generate_stream(50, seed=4))


def test_monitor_sees_a_large_single_point_spike():
    values = np.ones(120)
    values[60] = 20
    flags = detect_anomalies(values, window=24, z=2.5)
    assert flags[60]


def test_shift_has_positive_psi():
    assert population_stability_index(np.zeros(100), np.ones(100)) >= 0


def test_summary_has_both_monitoring_signals():
    metrics = summarize(seed=5)
    assert metrics["point_anomalies"] >= 1
    assert metrics["psi_after_shift"] > 0
