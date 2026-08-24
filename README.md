# Sensor Drift Watch

[![CI](https://github.com/ratnesh-ml/sensor-drift-watch/actions/workflows/test.yml/badge.svg)](https://github.com/ratnesh-ml/sensor-drift-watch/actions/workflows/test.yml)

> **Portfolio demo:** [Open the Ratnesh ML Lab showcase](https://ratnesh-ml-lab.vercel.app)
Models can fail in two different ways: one reading can be strange, or the whole input distribution can move. This project keeps those signals separate.

The repository creates a sensor-like stream with seasonality, isolated spikes, and a later mean shift. It detects local point anomalies with a rolling robust score and estimates distribution movement with a small Population Stability Index implementation.

## Run it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest
python -m sensor_drift_watch
pytest -q
```

## Monitoring contract

| Signal | Question | Typical response |
| --- | --- | --- |
| Point anomaly | Is one observation inconsistent with its local neighbourhood? | Inspect the event or sensor |
| Distribution drift | Has the population of readings moved? | Re-check data pipeline and model validity |

## Why it belongs in an AI/ML portfolio

Training a model is only one part of the lifecycle. This project is a compact way to demonstrate that I understand the difference between model inputs that are occasionally noisy and inputs that have changed systematically.

## Limitations

The stream is synthetic, PSI thresholds are not universal, and the rolling detector needs careful edge handling. A production version would log alert reasons, compare against a seasonal reference, add dashboards, and test alerts against labelled incidents.


## Recent depth improvements

The monitoring module now provides `detailed_summary` with anomaly rate and an interpretable PSI severity band: `stable`, `watch`, or `investigate`. This keeps numeric drift signals connected to an operational next action. GitHub Actions runs the monitoring tests continuously.


## License

MIT. See [LICENSE](LICENSE).
