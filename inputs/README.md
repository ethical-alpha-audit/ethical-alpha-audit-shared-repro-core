# Inputs (shared core)

Per `eaa_system/attachment_requirements.json`, the shared-core repo defines **`required_files`: []** for this directory. No manuscript or supplementary attachments are required here.

Downstream paper repositories use their own `inputs/` trees with explicit required files. This folder exists so tooling and QA can rely on a stable path (`ethical-alpha-audit-shared-repro-core/inputs/`) without special cases.

Optional local assets may be placed here for development only; they must remain general-purpose and must not embed paper-specific submission logic.
