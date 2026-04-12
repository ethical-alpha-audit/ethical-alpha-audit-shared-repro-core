# Claim traceability (shared core)

Rows marked **VERIFIED** have direct execution evidence from the QA session noted in the Evidence column. Other statuses are **NOT VERIFIED** (no evidence) or **FAILED** (evidence of failure).

| ID | Claim | Evidence | Status |
|----|--------|----------|--------|
| T1 | `outputs/tables/smoke_test_results.csv` matches pin in `config/expected_outputs.json` | `python scripts/validate_outputs.py` → `VALIDATION PASSED` after `python reproduce_all.py` in the 2026-04-12 QA session (run identity not asserted by this doc revision) | **VERIFIED** |
| T2 | `outputs/figures/smoke_test_summary.txt` matches pin | same as T1 | **VERIFIED** |
| T3 | `outputs/tables/utilities_validation.csv` matches pin | same as T1 | **VERIFIED** |
| T4 | `outputs/figures/demo_pipeline_summary.txt` matches pin | same as T1 | **VERIFIED** |
| T5 | `config/trace_map.json` paths correspond to governed outputs | T1–T4 VERIFIED; `scripts/validate_notebook_standard.py` passed in same `reproduce_all.py` run | **VERIFIED** |
| P1 | `eaa.paths.repo_root()` importable | `python -c "from eaa.paths import repo_root; print(repo_root())"` success (2026-04-12) | **VERIFIED** |
| P2 | `eaa.notebooks.archival` importable | `python -c "import eaa.notebooks.archival"` success (2026-04-12) | **VERIFIED** |
| P3 | `engine.corrected_public_engine_v1_1.evaluate_case` exists | `python -c "import engine.corrected_public_engine_v1_1 as eng; assert hasattr(eng, 'evaluate_case')"` success (2026-04-12) | **VERIFIED** |
| N1 | Technical plan notebooks in `config/notebook_plan.json` execute with fresh kernel | `reproduce_all.py` notebook step: three notebooks returned `status: ok` (2026-04-12) | **VERIFIED** |
| R1 | Full `reproduce_all.py` pipeline completes including shared-logic parity | `python reproduce_all.py` exit code 0; final line `ALL STEPS PASSED`; `PARITY VERIFICATION PASSED` from `scripts/verify_shared_logic_parity.py` (2026-04-12) | **VERIFIED** |
| R2 | `config/shared_logic_manifest.json` matches `git show HEAD:<path>` for all entries | Same session as R1; parity step passed (2026-04-12) | **VERIFIED** |
| N2 | Every `*.ipynb` under `notebooks/` is valid JSON and executes | 17 unique paths under `notebooks/` (deduped by `Path.resolve()`); in-memory execute with outputs cleared, `python3` kernel, all `OK` including `notebooks/example_notebook.ipynb` (2026-04-12) | **VERIFIED** |
| G1 | Portfolio `eaa_system/system_snapshot.json` is the governing source for `repos.shared-core.commit`; this file does not duplicate that hash. Traceability holds when this repository's HEAD matches the snapshot field. | 2026-04-12 reconciliation: compared `git rev-parse HEAD` to `repos.shared-core.commit` read from `eaa_system/system_snapshot.json` | **VERIFIED** |
| U1 | Unit tests pass | `python -m pytest -q` → `3 passed` (2026-04-12) | **VERIFIED** |

**Summary:** **14 / 14** rows **VERIFIED**; **0 NOT VERIFIED**; **0 FAILED**.
