# Previous Public Engine Implementation — Corrected for Alignment with Validated Methodology

## Status

This document describes inconsistencies identified in the previous public repository implementation. Results reported in the manuscripts correspond to the corrected public governance engine (version 1.1; hash-locked implementation). Alternative implementations may produce different results.

## Description of Previous Implementation

The prior public repository (`ethical-alpha-public-v32-main`) contained:

- An ingestion pipeline (`src/ethical_alpha/ingest/`) for loading and normalising governance datasets
- Pre-computed engine results in `overlay_engine_results.json`
- No executable governance evaluation logic

Gate outcomes and compensatory scores were pre-computed by a process that had diverged from the canonical engine used in the associated analyses.

## Identified Inconsistencies

A forensic audit identified three categories of inconsistency between the previous public implementation and the canonical engine. These inconsistencies were corrected for alignment with the validated methodology.

### 1. Compensatory Formula Inconsistency

| Parameter | Canonical (validated) | Previous public version |
|-----------|----------------------|------------------------|
| Feature count | 5 (gate features only) | 15 (all features including negatives) |
| Formula | `0.3×S + 0.2×E + 0.2×(1−B) + 0.15×C + 0.15×T` | `mean(all 15 value_primary)` |
| Bias treatment | Inverted: `(1 − bias_harm_index)` | Not inverted |
| Max score | 1.00 | ~0.463 |
| Threshold | 0.50 (from profile) | 0.50 |
| Cases exceeding threshold | 3 (google_dr, google_flu, uber_av) | 0 (mathematically impossible) |

Under the previous version, compensatory scoring rejected all cases because no score could exceed 0.50. This made the non-compensatory versus compensatory comparison — a core analytical finding — structurally unreproducible.

### 2. Threshold Profile Inconsistency

Non-moderate profiles differed by ±0.05 on multiple gates:
- Permissive: calibration 0.30→0.25, traceability 0.30→0.25
- Strict: all 5 gates shifted by 0.05
- Very strict: all 5 gates shifted by 0.05
- **Moderate: consistent** (no differences)

### 3. Gate Evaluation Anomalies

Three cases in `overlay_engine_results.json` had gate outcomes inconsistent with the expected single-feature threshold comparison:
- `google_dr`: `gate_safety=PASS` despite `intrinsic_safety=0.40 < 0.50`
- `ehr_process_bias_agniel2018`: `gate_bias=FAIL` despite `bias=0.40 ≤ 0.50`
- `fda_maude_ml_safety_events_2023`: `gate_evidence=FAIL` despite `evidence=0.55 ≥ 0.50`

## Corrected Implementation

The corrected public governance engine (version 1.1; hash-locked implementation) was used for all reported analyses. It was validated at 48/48 configuration parity against the canonical engine's stored per-case results across both evaluation modes.

The corrected implementation supports:

- `replay_mode` — used for all primary retrospective validation results described in the associated manuscript
- `canonical_full_mode` — used for simulation validation contexts described in the associated manuscripts

**Engine file:** `corrected_public_engine_v1_1.py`
**SHA-256:** `875f73150fae43695ecc6659581e8e25b365ad6171c9e13629fb01e923ab311c`
**Dependencies:** Python 3.10+ (stdlib only)

## Provenance

- Forensic audit conducted: 2026-03-23
- Canonical baseline lock: CBS_v1
- Corrected implementation validated: 2026-03-24
