# Data directory

## Why this directory is empty

This shared reproducibility core does **not** ship external datasets. All outputs are generated from **fixed internal feature vectors** hardcoded in `eaa/notebooks/archival.py` (notebooks import via `notebooks/archival_shared/archival_notebook_helpers.py`). These vectors are synthetic governance cases designed to exercise the engine's gate, compensatory, and abstention/fallback logic paths.

**Reproducibility is achieved without external data** because:

1. The governance engine (`engine/corrected_public_engine_v1_1.py`) is a pure function of its inputs — no trained model weights, no database lookups, no network calls.
2. Input feature vectors are frozen in source code and versioned alongside the engine.
3. Outputs are deterministic for any given input and are hash-locked in `config/expected_outputs.json`.

Paper-specific repositories that use real datasets (e.g., PhysioNet benchmark data, historical AI failure case files) maintain their own `data/` directories with provenance documentation. This shared core is intentionally data-free to avoid coupling the reproducibility harness to dataset access or licensing constraints.

## For paper-specific datasets

Refer to the individual paper submission repositories referenced in the accompanying manuscripts.
