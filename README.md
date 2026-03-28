	# Shared Reproducibility Core Repo

## Purpose
Shared utilities, schemas, helpers, loaders, validation routines, and common plotting functions used across the paper repos.

## Release target
Current planned release tag: `v1.0.0-initial`

## Required public-facing components
- GitHub repository
- Zenodo release archive linked to GitHub releases
- Jupyter notebook set
- Versioned manuscript and supplementary package
- Reproducibility manifest and output hashes

## Suggested first-release checklist
1. Confirm manuscript title and author metadata.
2. Replace placeholder DOI and repository links in the manuscript with real links at release time.
3. Populate the `data/README.md` with access, schema, provenance, and restriction notes.
4. Freeze the environment in `requirements.txt`, `environment.yml`, and `environment.lock`.
5. Run `python reproduce_all.py`.
6. Regenerate `repro_manifest.json` and `MANIFEST.sha256`.
7. Create GitHub release `v1.0.0-initial`.
8. Confirm Zenodo archived the release correctly.
9. Record the Zenodo DOI in the manuscript and release notes.

## Notebook inventory
- `01_core_demo.ipynb` - Demonstrate shared core helpers
- `02_validation_demo.ipynb` - Demonstrate validation routines

## Folder expectations
- `manuscript/` for manuscript, supplement, and reviewer notes
- `notebooks/` for ordered notebooks that run top-to-bottom
- `src/` for reusable code
- `data/` for raw, processed, and documentation
- `outputs/` for generated figures, tables, logs, and release bundles
- `tests/` for reproducibility checks
- `docs/` for methods and provenance notes

## Immediate next actions
- Fill in manuscript metadata placeholders
- Replace stub notebooks with live content
- Connect the repository to Zenodo
- Generate a clean first tagged release

# eaa-shared-repro-core - Paper-Specific Deterministic Harness

## Purpose
This harness is pre-filled for the repository:
eaa-shared-repro-core

## Repo role
Pilot harness here first. Use for smoke tests, utility validation, and deterministic examples.

## Included notebook order
- 1. 01_smoke_test.ipynb
  - output: outputs/tables/smoke_test_results.csv
  - output: outputs/figures/smoke_test_summary.txt
- 2. 02_utilities_validation.ipynb
  - output: outputs/tables/utilities_validation.csv
- 3. 03_demo_pipeline.ipynb
  - output: outputs/figures/demo_pipeline_summary.txt

## Usage
```bash
python reproduce_all.py
```

Edit the notebook plan and expected outputs once real notebooks and artefacts are ready.



