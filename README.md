# Sensor Drift Watch

[![CI](https://github.com/ratnesh-ml/sensor-drift-watch/actions/workflows/test.yml/badge.svg)](https://github.com/ratnesh-ml/sensor-drift-watch/actions/workflows/test.yml)

I made this monitoring lab to separate two signals that are often mixed together: one odd observation and a population that has genuinely moved. That distinction matters because the response should be different. A single spike may deserve an inspection; a distribution shift may mean the upstream data or model assumptions need to be revisited.

The repository creates a sensor-like stream with seasonality, isolated spikes, and a later mean shift. It pairs a rolling robust score for point anomalies with a small Population Stability Index (PSI) implementation for distribution drift.

## At a glance

| Signal | The question I am asking | Example response |
| --- | --- | --- |
| Point anomaly | Is this observation inconsistent with its local neighbourhood? | Inspect the event or sensor. |
| Distribution drift | Has the population of readings shifted over time? | Re-check the data pipeline and model validity. |

## Run it

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest
python -m sensor_drift_watch
pytest -q
```

## What I was trying to learn

Training a model is only one part of its lifecycle. I wanted a small, auditable project that showed I understand the difference between occasionally noisy inputs and systematically changing inputs. The `detailed_summary` helper turns raw values into an anomaly rate and an interpretable PSI band: `stable`, `watch`, or `investigate`.

## Limits and next steps

The stream is synthetic, PSI thresholds are context-dependent, and the rolling detector needs careful edge handling. This is not a production alerting service.

To move toward one, I would log alert reasons, compare against a seasonal reference, add a small dashboard, and test alerts against labelled incidents rather than only simulated shifts.

## Verification and license

Run `pytest -q` locally; GitHub Actions runs the monitoring tests on pushes and pull requests. MIT licensed; see [LICENSE](LICENSE).
