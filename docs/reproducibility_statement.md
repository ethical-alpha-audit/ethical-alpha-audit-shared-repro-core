# Reproducibility statement

## How to reproduce

From the repository root, with dependencies installed per `requirements.txt` (or `environment.yml`), run:

```bash
python reproduce_all.py
```

That command is the **only** execution entry point required for shared-core validation. It runs the configured notebooks in order, records byte-level digests of every declared output into `logs/actual_manifest.json`, and checks those artefacts against the locked expectations in `config/expected_outputs.json`.

## Deterministic generation

All artefacts listed in `config/expected_outputs.json` are produced **only** by the archival **technical** execute notebooks listed in `config/notebook_plan.json` under `notebooks/archival_shared/technical/`, using the authoritative public engine in `engine/corrected_public_engine_v1_1.py`. The harness pins `PYTHONHASHSEED` via `config/harness_settings.json` so Python hash behaviour is stable for the run. Together this yields **deterministically generated outputs** for the locked release state: the same checked-in sources and locked outputs reproduce the same bytes as the pinned SHA-256 values.

## Manifest-based validation and hash locking

**Manifest.** After notebook execution, `scripts/hash_manifest.py` hashes every file declared in `expected_outputs.json` and writes `logs/actual_manifest.json` with path, SHA-256, and presence flags.

**Hash locking.** `config/expected_outputs.json` carries a non-empty `sha256` field for each required output. `scripts/validate_outputs.py` compares the manifest to those pins: validation **fails** if a required file is missing, or if its digest differs from the pin. This upgrades checks from “file exists” to **cryptographic integrity**.

**Non-compensatory execution.** The harness does not substitute alternate notebooks, engines, or outputs: it only runs the ordered plan and validates the declared paths. Manual edits to locked outputs are detected automatically because they change digests.

## Manual steps

**None** are required for verification beyond installing dependencies and running `python reproduce_all.py`. There are no interactive cells, private data drops, or undocumented preprocessing steps in the shared-core chain.

## Archival note

This statement describes the **shared reproducibility core** validation path. It does not claim scope beyond the contracts in `config/` and the artefacts under `outputs/` as listed in `expected_outputs.json`.
