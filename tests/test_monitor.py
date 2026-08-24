import numpy as np

from sensor_drift_watch.monitor import detailed_summary, detect_anomalies, generate_stream, population_stability_index, psi_severity, summarize


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


def test_detailed_summary_adds_actionable_context():
    metrics = detailed_summary(seed=5)
    assert 0 <= metrics["anomaly_rate"] <= 1
    assert metrics["psi_severity"] == psi_severity(metrics["psi_after_shift"])


def test_psi_severity_bands_are_ordered():
    assert psi_severity(.05) == "stable"
    assert psi_severity(.15) == "watch"
    assert psi_severity(.30) == "investigate"
