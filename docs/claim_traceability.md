# Claim traceability (shared core)

Rows marked **VERIFIED** have direct execution evidence from the QA session noted in the Evidence column. Other statuses are **NOT VERIFIED** (no evidence) or **FAILED** (evidence of failure).

| ID | Claim | Evidence | Status |
|----|--------|----------|--------|
| T1 | `outputs/tables/smoke_test_results.csv` matches pin in `config/expected_outputs.json` | `python scripts/validate_outputs.py` → `VALIDATION PASSED` (2026-04-11) | **VERIFIED** |
| T2 | `outputs/figures/smoke_test_summary.txt` matches pin | same as T1 | **VERIFIED** |
| T3 | `outputs/tables/utilities_validation.csv` matches pin | same as T1 | **VERIFIED** |
| T4 | `outputs/figures/demo_pipeline_summary.txt` matches pin | same as T1 | **VERIFIED** |
| T5 | `config/trace_map.json` paths correspond to governed outputs | T1–T4 VERIFIED; structural map unchanged in repo | **VERIFIED** |
| P1 | `eaa.paths.repo_root()` importable | `python -c "from eaa.paths import repo_root; print(repo_root())"` success (2026-04-11) | **VERIFIED** |
| P2 | `eaa.notebooks.archival` importable | `python -c "import eaa.notebooks.archival"` success (2026-04-11) | **VERIFIED** |
| P3 | `engine.corrected_public_engine_v1_1.evaluate_case` exists | `python -c "import engine.corrected_public_engine_v1_1 as eng; assert hasattr(eng, 'evaluate_case')"` success (2026-04-11) | **VERIFIED** |
| N1 | Technical plan notebooks in `config/notebook_plan.json` execute with fresh kernel | `reproduce_all.py` notebook step: all three returned `status: ok`; durations 16.4s / 8.2s / 9.4s (2026-04-11) | **VERIFIED** |
| R1 | Full `reproduce_all.py` pipeline completes including shared-logic parity | `python reproduce_all.py` exit code 1; `scripts/verify_shared_logic_parity.py` reported hash drift on `eaa/__init__.py` and `scripts/hash_manifest.py` (2026-04-11) | **FAILED** |
| R2 | `config/shared_logic_manifest.json` matches `git show HEAD:<path>` for all entries | Same failure as R1 | **NOT VERIFIED** |
| N2 | Every `*.ipynb` under `notebooks/` is valid JSON and executes | `notebooks/example_notebook.ipynb` is not valid notebook JSON (`nbformat.reader.NotJSONError`) (2026-04-11) | **FAILED** |
| G1 | Portfolio `eaa_system/system_snapshot.json` binds `repos.shared-core.commit` to this repo HEAD | Snapshot shows `"shared-core": {"commit": null, ...}`; local `git rev-parse HEAD` = `00a2892014577823772f46bddeae8cacaa1db9f0` (2026-04-11) | **NOT VERIFIED** |
| U1 | Unit tests pass | `python -m pytest -q` → `3 passed` (2026-04-11) | **VERIFIED** |

**Summary:** **10 / 14** rows **VERIFIED**; **2 FAILED** (R1 full pipeline / N2 example notebook); **2 NOT VERIFIED** (R2 parity sub-claim redundant with R1; G1 snapshot binding).
