# Release v1.0.0 — Ethical Alpha Audit Shared Reproducibility Core

## Summary

This repository is the **shared reproducibility core** for the Ethical Alpha Audit public stack. It provides the deterministic Jupyter harness, integration with the authoritative public governance engine (`engine/corrected_public_engine_v1_1.py`), config contracts (`config/`), and archival notebooks under `notebooks/archival_shared/` used for smoke tests, utilities validation, and a small demo pipeline. It is an **authority/support** artefact for audit-style reproducibility, not a paper-specific submission bundle.

## Deterministic reproducibility

End-to-end validation is invoked with:

```bash
python reproduce_all.py
```

That entry point executes notebooks in the order fixed in `config/notebook_plan.json`, records SHA-256 digests in `logs/actual_manifest.json`, and validates all declared artefacts against the pins in `config/expected_outputs.json`. The harness sets a stable Python hash seed via `config/harness_settings.json`. For a full narrative, see `docs/reproducibility_statement.md`.

## Outputs (this release)

Locked artefacts under `outputs/`:

| Path | Role |
|------|------|
| `outputs/tables/smoke_test_results.csv` | Engine smoke record (replay mode) |
| `outputs/figures/smoke_test_summary.txt` | Smoke-test narrative summary |
| `outputs/tables/utilities_validation.csv` | Direct engine helper validation |
| `outputs/figures/demo_pipeline_summary.txt` | Demo batch summary (canonical full mode) |

Traceability: `config/trace_map.json`.

## Hash locking

Each required file is listed in `config/expected_outputs.json` with a **non-empty SHA-256** pin. `scripts/validate_outputs.py` compares `logs/actual_manifest.json` to those pins: validation fails if a file is missing or if any digest differs. This release therefore binds the public snapshot to **cryptographic integrity**, not merely file presence.

## Release assurance

**This release is cryptographically fixed and reproducible:** the checked-in outputs match the pinned digests; the manifest on record matches those pins; and a clean execution of `python reproduce_all.py` (after dependency install) is the supported path to regenerate and verify the same byte-level artefacts.

---

*Version identifier:* `v1.0.0` (see repository root `VERSION`).
