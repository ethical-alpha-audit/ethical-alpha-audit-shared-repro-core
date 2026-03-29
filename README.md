# Ethical Alpha Audit Shared Repro Core

## Purpose

This repository is the shared reproducibility core for the Ethical Alpha Audit public reproducibility stack.

It is a shared authority/support repository, not a paper-specific submission repository.

Its role is to provide:

- the shared deterministic harness
- the shared public engine integration
- shared config contracts and validation structure
- shared smoke, utilities, and demo pipeline notebooks for core validation

## What this repository contains

- `engine/` for the authoritative public engine integration
- `manifests/` for engine-related manifest files
- `config/` for notebook execution order, expected outputs, trace mapping, presentation config, and harness settings
- `notebooks/archival_shared/` for active shared-core notebooks
- `notebooks/reference/` for retained reference notebooks that are not part of the active execution chain
- `scripts/` and `tests/` for harness and validation support
- `reproduce_all.py` as the shared-core execution entry point

## What this repository does not contain

This repository should not be used as the active home for:

- paper-specific submission bundles
- paper-specific reviewer Word document chains
- paper-specific release-bound archival outputs
- private manuscript materials intended to remain unpublished before journal acceptance

Those belong in paper-specific repositories.

## Active notebook execution chain

The active shared-core notebook plan is:

1. `notebooks/archival_shared/01_smoke_test.ipynb`
2. `notebooks/archival_shared/02_utilities_validation.ipynb`
3. `notebooks/archival_shared/03_demo_pipeline.ipynb`

These notebooks are used for shared-core validation and smoke testing, not as paper-specific archival notebooks.

## Execution and validation rules

- Outputs must be written only to `outputs/`
- Validation must be run through `python reproduce_all.py`
- Fresh-output integrity rules apply: stale files must not be used as proof of reproducibility
- `environment.lock` remains authoritative where present
- Shared-core validation outputs are governed by `config/expected_outputs.json`
- Output traceability is governed by `config/trace_map.json`

## Release discipline

Do not treat this repository as release-ready unless:

- the engine integration is present and correct
- the notebook plan is valid JSON and matches the active notebook inventory
- expected outputs are defined for the active notebooks
- outputs are generated through a clean run
- manifests and validation artefacts are current

## Notes on manuscript-related folders

If manuscript-related placeholder folders or notes are retained in this repository, they must be clearly treated as non-release support material and must not be confused with paper-specific publication artefacts.
