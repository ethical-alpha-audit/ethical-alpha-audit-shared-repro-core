# Stage 2 shared governance (R2 alignment)

## Stage 2 preamble (locked)

- **Write surface:** Git branch `stage2-r2-align` in this repository only (no sibling-directory work in Stage 2).
- **Exact shared-artifact inventory:** See `config/shared_logic_inventory.json` — every governed path is enumerated; there are no wildcard-only rules for parity or vendoring.
- **Baseline files hash-locked for zero-regression:** `config/expected_outputs.json` and aligned copy `config/baseline_output_hashes.json` pin:
  - `outputs/tables/smoke_test_results.csv`
  - `outputs/figures/smoke_test_summary.txt`
  - `outputs/tables/utilities_validation.csv`
  - `outputs/figures/demo_pipeline_summary.txt`
- **Output ↔ notebook mapping:** `config/trace_map.json` lists each pinned output path with its owning execute notebook (and role); `notebook_plan.json` does not embed per-notebook expected hashes.

## Transitional vs long-term sharing (explicit)

- **Stage 2 default:** Verified **copy + CI drift detection** (manifest parity) across repositories is the deliberately **low-friction transitional** operating model.
- **Not the ideal end state:** Long-term governance may move to a **submodule** or **internal package** so consumers install one artefact instead of copying trees. That is an **architectural follow-up**, not an open ambiguity.
- **Authoring rule:** Shared logic (including everything under `eaa/`) is **authored only once** in **SHARED CORE**. Paper 4 may **only** consume **verified copies** checked against `config/shared_logic_manifest.json`.

## Operational commands

- After editing any path in `governed_paths`, run `python scripts/hash_shared_logic.py` and commit the updated `config/shared_logic_manifest.json`.
- Full harness: `python reproduce_all.py` (validates notebook standard, executes planned notebooks, hashes outputs, validates pins, exports HTML, verifies shared-logic parity).

## HTML exports

Canonical static exports live under `docs/notebook_exports/` (from `scripts/export_html.py`). Older `docs/html` or `docs/archival_html` layouts, if present elsewhere, are deprecated in favour of this directory.
