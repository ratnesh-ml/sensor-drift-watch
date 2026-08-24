from __future__ import annotations

import numpy as np
import pandas as pd


def generate_stream(n: int = 720, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    baseline = 20 + 1.5 * np.sin(t / 24) + rng.normal(0, .35, n)
    drift = np.where(t >= int(n * .65), 1.2 + .005 * (t - int(n * .65)), 0)
    spikes = np.zeros(n)
    start = 40 if n > 80 else max(1, n // 5)
    end = n - 40 if n > 80 else min(n - 1, n - n // 5)
    candidates = np.arange(start, max(start, end))
    count = min(max(4, n // 120), len(candidates))
    spike_indices = rng.choice(candidates, size=count, replace=False) if count else np.array([], dtype=int)
    spikes[spike_indices] = rng.choice([-4.0, 4.0], size=len(spike_indices))
    return pd.DataFrame({"step": t, "reading": baseline + drift + spikes, "drift_active": t >= int(n * .65), "spike": spikes != 0})


def detect_anomalies(values: np.ndarray, window: int = 48, z: float = 3.5) -> np.ndarray:
    series = pd.Series(values)
    median = series.rolling(window, center=True, min_periods=max(8, window // 3)).median()
    deviation = (series - median).abs()
    scale = deviation.rolling(window, center=True, min_periods=max(8, window // 3)).median().replace(0, np.nan)
    score = deviation / (1.4826 * scale.replace(0, np.nan))
    flags = score.gt(z)
    # If the local scale is effectively zero, an obvious departure is still an anomaly.
    flags |= scale.fillna(0).lt(1e-6) & deviation.gt(1.0)
    return flags.fillna(False).to_numpy()


def population_stability_index(reference: np.ndarray, current: np.ndarray, bins: int = 10) -> float:
    edges = np.quantile(reference, np.linspace(0, 1, bins + 1))
    edges = np.unique(edges)
    if len(edges) < 3:
        return 0.0
    ref_counts, _ = np.histogram(reference, bins=edges)
    cur_counts, _ = np.histogram(current, bins=edges)
    ref_pct = np.maximum(ref_counts / max(1, len(reference)), 1e-6)
    cur_pct = np.maximum(cur_counts / max(1, len(current)), 1e-6)
    return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))


def summarize(seed: int = 42) -> dict[str, float]:
    frame = generate_stream(seed=seed)
    flags = detect_anomalies(frame["reading"].to_numpy())
    split = int(len(frame) * .65)
    return {
        "rows": float(len(frame)),
        "point_anomalies": float(flags.sum()),
        "known_spikes": float(frame["spike"].sum()),
        "psi_after_shift": population_stability_index(frame["reading"][:split], frame["reading"][split:]),
    }
