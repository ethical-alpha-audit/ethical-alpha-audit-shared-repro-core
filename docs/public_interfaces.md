# Public interfaces (shared core)

Stable surfaces intended for reuse across paper repositories and CI. Anything not listed here should be treated as internal unless documented elsewhere.

## Python packages and modules

| Surface | Role |
|--------|------|
| `eaa.paths.repo_root()` | Resolve repository root via `EAA_REPO_ROOT` or anchor files (`engine/`, `config/`, `reproduce_all.py`). |
| `eaa.notebooks.archival` | Canonical implementations for archival/interactive notebook behaviour (widgets, contract runs). Story notebooks under `notebooks/archival_shared/` should call into this module rather than duplicating logic. |
| `notebooks/archival_shared/archival_notebook_helpers.py` | Thin re-export of `eaa.notebooks.archival` for path-stable imports from notebook working directories. |

## Authoritative engine

| Surface | Role |
|--------|------|
| `engine/corrected_public_engine_v1_1.py` | Single authoritative governance evaluation API (`evaluate_case`, profiles, modes). Notebooks add `engine/` to `sys.path` and import this module by name. |

## Reproduction entry point

| Surface | Role |
|--------|------|
| `reproduce_all.py` | Ordered pipeline: notebook standard check → execute plan → manifest → output hash validation → HTML export → shared-logic parity. |

## Configuration contracts

| Path | Role |
|------|------|
| `config/notebook_plan.json` | Ordered list of technical execute notebooks. |
| `config/expected_outputs.json` | Declared outputs and SHA-256 pins for `scripts/validate_outputs.py`. |
| `config/harness_settings.json` | `python_hash_seed`, timeouts, fail-fast, output clearing. |
| `config/shared_logic_inventory.json` | Inputs to `scripts/verify_shared_logic_parity.py`. |

## Layout note

Library code for this repo lives under **`eaa/`** and **`engine/`** at the repository root (there is no separate `src/` tree by design).
