# Ethical Alpha Audit Shared Repro Core

## Quick start

From the repository root:

```bash
python -m pip install -r requirements.txt
python reproduce_all.py
```

The harness executes every notebook in `config/notebook_plan.json`, regenerates `logs/actual_manifest.json`, and validates each declared output byte-for-byte against the SHA-256 pins in `config/expected_outputs.json`.

**This repository reproduces all results without modification:** the locked outputs under `outputs/` match the pinned digests, and validation fails if any file is missing or altered.

## Expected outputs

| Path | Role |
|------|------|
| `outputs/tables/smoke_test_results.csv` | Single-case replay-mode engine smoke record |
| `outputs/figures/smoke_test_summary.txt` | Narrative summary for the smoke test |
| `outputs/tables/utilities_validation.csv` | Direct engine helper checks (gates, abstention helper, hash fixture) |
| `outputs/figures/demo_pipeline_summary.txt` | Batch summary for canonical full mode |

Traceability from file to notebook: `config/trace_map.json`.

## Deterministic guarantee

- **Engine:** `engine/corrected_public_engine_v1_1.py` is the single authoritative integration; notebooks import it rather than reimplementing logic.
- **Execution order:** `config/notebook_plan.json` is fixed; `reproduce_all.py` is the only supported entry point for full validation.
- **Python hashing:** `config/harness_settings.json` sets `python_hash_seed` (consumed by `reproduce_all.py` and the notebook runner).
- **Integrity:** Expected outputs use **pinned SHA-256** values. `scripts/validate_outputs.py` rejects missing files, wrong digests, or tampering—validation is cryptographic, not presence-only.

For a concise narrative of the workflow, see `docs/reproducibility_statement.md`.

## Repository structure

| Area | Purpose |
|------|---------|
| `engine/` | Authoritative public governance engine (v1.1) |
| `manifests/` | Engine-related manifest JSON (supporting artefacts) |
| `config/` | Notebook plan, expected outputs (hash pins), trace map, harness settings |
| `notebooks/archival_shared/` | Active validation notebooks executed by the harness |
| `notebooks/reference/` | Reference notebooks **not** in the active execution chain |
| `scripts/` | Notebook runner, manifest builder, output validator |
| `tests/` | Lightweight structure / harness tests |
| `outputs/` | Declared validation artefacts only (plus `.gitkeep` placeholders) |
| `logs/` | Runtime manifests (`actual_manifest.json` after a full run) |
| `reproduce_all.py` | One-command reproduction and validation |

## Purpose

This repository is the **shared reproducibility core** for the Ethical Alpha Audit public stack: deterministic harness, public engine wiring, config contracts, and archival notebooks. It is **not** a paper-specific submission repository.

## What this repository does not contain

- Paper-specific submission bundles, reviewer-only document chains, or private manuscript drops  
  (those belong in paper-specific repositories.)

## Release discipline

Release-ready means: engine present, plan valid, outputs generated and **hash-locked** in `config/expected_outputs.json`, and `python reproduce_all.py` passing against those pins after a clean generation run.

## Notes on manuscript-related folders

Any manuscript-related placeholders must be clearly non-release material and not confused with publication artefacts.

## Archiving

For Zenodo-oriented metadata prepared alongside the repository, see `zenodo.json`. Deposit-specific DOIs are assigned **only** when a version is published on Zenodo (not embedded here).
