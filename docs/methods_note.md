# Methods note

## Computational workflow

1. **Inputs:** Fixed synthetic governance feature vectors defined inline in `eaa/notebooks/archival.py` (notebook shim `archival_notebook_helpers.py`). No external datasets are required for the shared-core validation path.

2. **Pre-processing:** None. Feature vectors are consumed directly by the engine.

3. **Analysis sequence:** Three notebooks executed in order via `python reproduce_all.py`:
   - `01_smoke_test_execute.ipynb` — single-case replay-mode evaluation
   - `02_utilities_validation_execute.ipynb` — gate, compensatory, and abstention helper validation
   - `03_demo_pipeline_execute.ipynb` — three-case batch in canonical_full_mode

4. **Output generation:** Each notebook writes deterministic artefacts to `outputs/tables/` (CSV) or `outputs/figures/` (TXT narrative summaries).

5. **Validation:** `scripts/hash_manifest.py` computes SHA-256 digests of all declared outputs; `scripts/validate_outputs.py` compares these against the pinned values in `config/expected_outputs.json`. Validation fails if any file is missing or any digest differs.

6. **Known limitations:** The shared core validates only the engine wiring and harness infrastructure using synthetic cases. It does not reproduce the full retrospective validation (12 historical AI failure cases) or the PhysioNet benchmark evaluation; those are maintained in paper-specific repositories.
