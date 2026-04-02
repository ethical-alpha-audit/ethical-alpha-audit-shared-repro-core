# Ethical Alpha Audit Shared Repro Core

> **Zenodo DOI:** [![DOI](https://zenodo.org/badge/1194625255.svg)](https://doi.org/10.5281/zenodo.19322345)

## Reviewer quick validation (no execution required)

To verify that every reported output is intact and untampered, **no notebook execution is needed**. From an unzipped copy of this repository:

```bash
python scripts/validate_outputs.py
```

**Expected result:** `VALIDATION PASSED`

This single command checks every declared output file against its pinned SHA-256 digest in `config/expected_outputs.json`. If any file is missing, altered, or corrupted, the validator prints `VALIDATION FAILED` and lists the specific discrepancy. A passing result confirms that the checked-in artefacts are byte-for-byte identical to the outputs produced by the deterministic execution chain.

**To additionally re-execute the full pipeline** (optional — requires Python dependencies):

```bash
python -m pip install -r requirements.txt
python reproduce_all.py
```

## What is being validated

This repository contains four deterministic output files produced by a governance engine that evaluates AI deployment readiness. Each file is generated from fixed input data hardcoded in the source, passed through the engine's decision logic, and written to disk. The resulting bytes are then fingerprinted with SHA-256 and the fingerprints are stored in `config/expected_outputs.json`.

| File | What it contains |
|------|-----------------|
| `outputs/tables/smoke_test_results.csv` | A single governance case evaluated in replay mode — records the pass/fail verdict, gate outcomes, and compensatory score |
| `outputs/figures/smoke_test_summary.txt` | A plain-language narrative of the smoke test purpose, method, and result |
| `outputs/tables/utilities_validation.csv` | Direct checks of the engine's helper functions — gate evaluation, compensatory scoring, abstention rate computation, and batch hashing |
| `outputs/figures/demo_pipeline_summary.txt` | A three-case batch showing contrasting outcomes: approval, hard gate failure, and abstention-triggered rejection |

Because inputs are fixed and the engine is deterministic, these outputs are the same every time the code runs — on any platform, in any environment. The SHA-256 pins in `config/expected_outputs.json` are the ground truth: if the validator says `PASSED`, the outputs match exactly what the engine produces.

## Quick start (full reproduction)

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

**Artefact taxonomy note:** `outputs/tables/` contains tabular artefacts (CSV). `outputs/figures/` contains narrative summaries (TXT) that correspond to the "figures" slot in the manuscript output contract. In this shared core, summaries are text-based rather than graphical because the primary outputs are governance verdicts and digests; graphical figures are produced in the paper-specific repositories.

Traceability from file to notebook: `config/trace_map.json`.

## Reproducibility Notebooks

The following links open **narrative** notebooks (no code on NBViewer). Full validation runs the **technical** execute notebooks via the harness.

### Experiment narrative (NBViewer)
#### Archival
1. **Smoke Test**  
   Verifies environment integrity, deterministic settings, and numerical stability.
   https://nbviewer.org/github/ethical-alpha-audit/ethical-alpha-audit-shared-repro-core/blob/main/notebooks/archival_shared/01_smoke_test.ipynb
2. **Utilities Validation**  
   Validates core utility functions, statistical components, and supporting infrastructure used throughout the pipeline.
   https://nbviewer.org/github/ethical-alpha-audit/ethical-alpha-audit-shared-repro-core/blob/main/notebooks/archival_shared/02_utilities_validation.ipynb
3. **Demonstration Pipeline**  
   Executes the full governance evaluation pipeline on the reference dataset, reproducing the primary outputs reported in the manuscript.
   https://nbviewer.org/github/ethical-alpha-audit/ethical-alpha-audit-shared-repro-core/blob/main/notebooks/archival_shared/03_demo_pipeline.ipynb
#### Reference
1. **Core Execute**  
   Technical — core API echo.
   https://nbviewer.org/github/ethical-alpha-audit/ethical-alpha-audit-shared-repro-core/blob/main/notebooks/archival_shared/01_smoke_test.ipynb
2. **Core Story**  
   Core engine API — reference narrative.
   https://nbviewer.org/github/ethical-alpha-audit/ethical-alpha-audit-shared-repro-core/blob/main/notebooks/archival_shared/02_utilities_validation.ipynb
3. **Validation Execute**  
   Technical — validation contract echo.
   https://nbviewer.org/github/ethical-alpha-audit/ethical-alpha-audit-shared-repro-core/blob/main/notebooks/archival_shared/03_demo_pipeline.ipynb
4. **Validation Story**  
   Executes the full governance evaluation pipeline on the reference dataset, reproducing the primary outputs reported in the manuscript.
   https://nbviewer.org/github/ethical-alpha-audit/ethical-alpha-audit-shared-repro-core/blob/main/notebooks/archival_shared/03_demo_pipeline.ipynb
#### Website Interactive
1. **About Layer**  
   Notebook suite orientation.
   https://nbviewer.org/github/ethical-alpha-audit/ethical-alpha-audit-shared-repro-core/blob/main/notebooks/archival_shared/01_smoke_test.ipynb
2. **Gate Explorer Interactive**  
   Gate & verdict explorer — interactive instrument
   https://nbviewer.org/github/ethical-alpha-audit/ethical-alpha-audit-shared-repro-core/blob/main/notebooks/archival_shared/02_utilities_validation.ipynb
3. **Gate Explorer Story**  
   Interactive gate exploration — narrative.
   https://nbviewer.org/github/ethical-alpha-audit/ethical-alpha-audit-shared-repro-core/blob/main/notebooks/archival_shared/03_demo_pipeline.ipynb
   
### Harness vs NBViewer

`python reproduce_all.py` executes `notebooks/archival_shared/technical/*_execute.ipynb` (see `config/notebook_plan.json`). NBViewer links above point at **markdown-only** story notebooks. Paired **`*_interactive.ipynb`** files provide **ipywidgets**; serve with [Voila](https://voila.readthedocs.io/) for a code-free UI (`voila.json`).

### Static notebook exports (no setup required)

Read-only HTML renderings of all narrative notebooks are included in `docs/archival_html/`. These can be opened in any browser — no Jupyter, no Python, no network access needed.

- [`01_smoke_test.html`](docs/archival_html/01_smoke_test.html) — smoke test narrative with expected output snapshot
- [`02_utilities_validation.html`](docs/archival_html/02_utilities_validation.html) — utilities validation narrative
- [`03_demo_pipeline.html`](docs/archival_html/03_demo_pipeline.html) — demo pipeline narrative with expected output snapshot
- [`01_gate_explorer_story.html`](docs/archival_html/01_gate_explorer_story.html) — interactive gate explorer narrative
- [`00_about_layer.html`](docs/archival_html/00_about_layer.html) — notebook suite orientation

### Interactive execution

#### Local installlation or Docker
Interactive notebooks can be run locally after installing dependencies, or via Docker. 

#### Binder
Clicking the Binder link below allows you to run GitHub repositories in an interactive environment directly in your browser

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ethical-alpha-audit/ethical-alpha-audit-shared-repro-core.git/main)

#### Ethical Alpha Audit website
This research is also hosted on the research pages of the Ethical Alpha Audit.

https://www.ethicalalphaaudit.com/

### Notes

- For cryptographic validation of outputs, run `python reproduce_all.py` from the repository root.
- Deterministic execution uses `config/harness_settings.json` and version-controlled sources; see Zenodo for DOI-linked releases.
- Sessions running via Voila or Docker are temporary.

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
| `notebooks/archival_shared/` | Archival story + interactive pairs; **`technical/`** notebooks are executed by the harness |
| `notebooks/reference/` | Reference notebooks **not** in the active execution chain |
| `scripts/` | Notebook runner, manifest builder, output validator |
| `tests/` | Lightweight structure / harness tests |
| `outputs/` | Declared validation artefacts only (hash-locked in `config/expected_outputs.json`) |
| `logs/` | Runtime manifests (`actual_manifest.json` after a full run) |
| `docs/` | Reproducibility statement, methods note, provenance, archival HTML exports |
| `data/` | Intentionally empty — see `data/README.md` for rationale |
| `reproduce_all.py` | One-command reproduction and validation |

## Purpose

This repository is the **shared reproducibility core** for the Ethical Alpha Audit public stack: deterministic harness, public engine wiring, config contracts, and archival notebooks. It is **not** a paper-specific submission repository.

## What this repository does not contain

- Paper-specific submission bundles, reviewer-only document chains, or private manuscript drops (those belong in paper-specific repositories)
- External datasets — all outputs are generated from fixed internal feature vectors hardcoded in source code; full reproducibility requires no data downloads, no access credentials, and no third-party licensing

## Release discipline

Release-ready means: engine present, plan valid, outputs generated and **hash-locked** in `config/expected_outputs.json`, and `python reproduce_all.py` passing against those pins after a clean generation run.

## Archiving

For Zenodo-oriented metadata prepared alongside the repository, see `.zenodo.json`. Deposit-specific DOIs are assigned **only** when a version is published on Zenodo (not embedded here).

## Reproducibility assurance

This repository has been independently audited for reproducibility. The cryptographic output contract (`config/expected_outputs.json`) is enforced by a validator that passes against the checked-in artefacts without notebook re-execution. All metadata placeholders have been resolved, all dependencies are version-pinned, and static HTML archival exports are provided for long-term reviewer accessibility.
