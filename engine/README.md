# Corrected Public Governance Engine (Version 1.1; Hash-Locked Implementation)

This repository provides the reference implementation of the governance engine used in the associated empirical analyses. The implementation corresponds to the validated configuration described in the accompanying manuscripts and reproducibility artefact.

## Overview

This module implements a non-compensatory (conjunctive) governance gate architecture and a weighted compensatory scoring model for evaluating AI system deployment readiness across five governance domains. It is provided as a stdlib-only Python module (Python 3.10+, no external dependencies) with deterministic, hash-locked behaviour suitable for scientific reproducibility.

The implementation is a deterministic port of the canonical governance engine (`governance_engine.py` from `historical-replay-governance-simulation`), preserving identical evaluation logic in a standalone format. Results reported in the manuscripts correspond to this implementation.

## Relationship to Previous Public Version

The previous public repository (`ethical-alpha-public-v32-main`) contained an ingestion pipeline but no executable governance evaluation logic. Gate outcomes and compensatory scores existed only as pre-computed values in `overlay_engine_results.json`. A forensic audit identified three inconsistencies between those pre-computed results and the canonical engine:

| Component | Previous public version | This implementation (canonical) |
|-----------|------------------------|-------------------------------|
| **Compensatory formula** | Arithmetic mean of 15 raw features | Weighted 5-feature: `0.3×S + 0.2×E + 0.2×(1−B) + 0.15×C + 0.15×T` |
| **Bias treatment** | Not inverted | **Inverted**: `(1 − bias_harm_index)` before weighting |
| **Max compensatory score** | ~0.463 (structurally capped) | 1.00 (full range) |
| **Gate evaluation** | 3 cases with anomalous outcomes | Raw single-feature threshold comparison |
| **Threshold profiles** | Non-moderate profiles differed by ±0.05 | Canonical profiles as specified in the simulation study |

Under the previous public version, compensatory scoring rejected all cases (no score could exceed 0.50), making the non-compensatory versus compensatory comparison structurally unreproducible. This corrected implementation restores alignment with the validated methodology.

## Validation Context

This engine has been validated across three distinct validation layers, each serving a different evidential purpose:

### Simulation Validation

The engine's `GovernancePolicyEngine` and `CompensatoryPolicyEngine` classes implement the identical gate and scoring logic used in the companion Monte Carlo simulation studies described in the associated manuscripts. The simulation validation establishes the theoretical properties of the non-compensatory architecture, including scope conditions under which the gate safety advantage holds or diminishes, threshold sensitivity, and noise robustness. Under the primary heterogeneous evidence model, the simulation demonstrated 99.5–99.8% unsafe system detection with non-compensatory gates versus 77.2% for compensatory scoring.

**Limitations (Simulation Validation):** All AI systems are synthetically generated. The generative distributions and SCM functional forms are assumed. Results characterise theoretical properties under modelled conditions, not observed institutional behaviour.

### Retrospective Validation (Historical Replay)

The engine was applied to structured evidence from 12 documented AI governance failures and a control cohort of 12 FDA-cleared AI devices via the `replay_mode` evaluation path. Under the moderate threshold profile, the non-compensatory framework rejected 11 of 12 documented failures (sensitivity 91.7%). The safety gate was the most frequently binding constraint (83% of cases). Two compensatory divergence cases (Google Flu Trends composite score 0.5675, Uber AV composite score 0.5125) illustrate how compensatory scoring can approve systems that non-compensatory gates reject. Governance outcomes were stable under Monte Carlo perturbation of evidence uncertainty bounds (100% stability across 200 iterations per case) and under adversarial ±0.05 feature perturbation (95.8% verdict stability; moderate profile fully invariant).

Cross-validation against the canonical engine's stored per-case results confirmed 48/48 configuration parity across both `replay_mode` and `canonical_full_mode` (12 cases × 4 threshold profiles).

**Limitations (Retrospective Validation):** The 12-case sample is a curated convenience sample of well-documented failures, not representative of all AI deployments. Evidence encoding involves judgement despite anchored rubrics. The analysis is retrospective; performance under real-time conditions with incomplete evidence is untested.

### Benchmark Validation (PhysioNet)

The engine was applied to governance feature vectors derived from two sepsis prediction models evaluated on PhysioNet 2019 clinical benchmark data (5,000 patients, 188,453 patient-hours). Both models were rejected under the moderate profile (safety gate binding), consistent with the historical replay finding that the safety gate is the most frequently binding constraint. Both models exhibited heterogeneous governance evidence profiles (feature spread > 0.47), consistent with the simulation study's assumption that real AI systems present different strengths and weaknesses across governance domains.

**Limitations (Benchmark Validation):** Limited to two model architectures evaluated on a single clinical prediction task (early sepsis onset). Governance features are derived from benchmark artefacts and do not include operational deployment evidence. The PhysioNet evaluation should not be characterised as real-world deployment validation.

## Dual-Mode Architecture

The engine supports two evaluation modes, corresponding to different analytical scopes:

### `replay_mode` (default)

This mode was used for all primary results in the retrospective validation described in the associated manuscript. It evaluates cases through the 5-gate non-compensatory architecture and weighted compensatory scoring model without applying SCM-derived dynamics.

- **Logic:** 5-gate non-compensatory evaluation + weighted compensatory scoring
- **Final verdict:** `approved = all_gates_pass`
- **Abstention/fallback:** Not applied

### `canonical_full_mode`

This mode extends `replay_mode` with the SCM-derived abstention override and fallback safety check. It is relevant to the simulation validation context described in the associated manuscripts, where system behaviour under deployment conditions is modelled, and to analysis of the permissive profile where abstention effects emerge.

- **Logic:** 5-gate + compensatory + SCM-derived abstention override + fallback safety check
- **Final verdict:** `approved = all_gates_pass AND (NOT abstention_triggered OR fallback_adequate)`
- **Abstention formula:** `abstention_rate = 1 / (1 + exp(−5.0 × (0.5 − uncertainty_calibration)))`
- **Abstention trigger:** `abstention_rate > 0.5` (strict greater-than)
- **Fallback check:** `fallback_safety_delta >= 0.3`

**Mode equivalence under moderate profile:** Both modes produce identical outcomes for all 12 retrospective validation cases under the moderate threshold profile. Differences emerge only under the permissive profile, where 3 cases (Epic Sepsis, Google Flu Trends, Babylon) pass all gates but are rejected by the abstention override in `canonical_full_mode`.

## CLI Usage

### Retrospective Validation — Moderate Profile (Primary Result)

```bash
python corrected_public_engine_v1_1.py \
  --cases-dir /path/to/canonical_cases/ \
  --profiles moderate \
  --mode replay_mode \
  --output results_moderate_replay.json
```

### Retrospective Validation — Full Profile Sweep

```bash
python corrected_public_engine_v1_1.py \
  --cases-dir /path/to/canonical_cases/ \
  --profiles permissive moderate strict very_strict \
  --mode replay_mode \
  --output results_all_profiles_replay.json
```

### Simulation Context — Canonical Full Mode

```bash
python corrected_public_engine_v1_1.py \
  --cases-dir /path/to/canonical_cases/ \
  --profiles permissive moderate strict very_strict \
  --mode canonical_full_mode \
  --output results_all_profiles_full.json
```

## Canonical Parameters (Hash-Locked)

### Gate Features (5)

| Gate | Feature | Direction | Moderate Threshold |
|------|---------|-----------|-------------------|
| G1 Safety | `intrinsic_safety` | ≥ threshold | 0.50 |
| G2 Evidence | `evidence_strength` | ≥ threshold | 0.50 |
| G3 Bias/Equity | `bias_harm_index` | ≤ threshold | 0.50 |
| G4 Calibration | `uncertainty_calibration` | ≥ threshold | 0.40 |
| G5 Traceability | `traceability_integrity` | ≥ threshold | 0.40 |

### Compensatory Formula

```
score = 0.30 × intrinsic_safety
      + 0.20 × evidence_strength
      + 0.20 × (1 − bias_harm_index)     ← BIAS INVERTED
      + 0.15 × uncertainty_calibration
      + 0.15 × traceability_integrity
```

Threshold: `mean(safety_gate, evidence_gate, bias_gate)` from profile = **0.50** for moderate.

### Threshold Profiles

| Profile | S | E | B | C | T |
|---------|-----|-----|-----|-----|-----|
| Permissive | 0.30 | 0.30 | 0.70 | 0.30 | 0.30 |
| Moderate | 0.50 | 0.50 | 0.50 | 0.40 | 0.40 |
| Strict | 0.70 | 0.70 | 0.30 | 0.60 | 0.60 |
| Very Strict | 0.80 | 0.80 | 0.20 | 0.70 | 0.70 |

## Requirements

- Python 3.10+ (stdlib only — no external dependencies)
- Input: JSON case files with `case_id` and `features` dict
- Output: JSON with gate results, compensatory scores, and verdicts

## Provenance and Reproducibility

- Canonical source: `historical-replay-governance-simulation/src/policy/governance_engine.py`
- Baseline lock: CBS_v1 (48/48 parity verified across both modes)
- Engine hash (SHA-256): `875f73150fae43695ecc6659581e8e25b365ad6171c9e13629fb01e923ab311c`
- Reproducibility artefact: see accompanying Zenodo deposit for the full reproducibility bundle (datasets, manifests, run instructions, expected outputs)
