"""Ethical Alpha Audit shared archival and paths (SHARED CORE — single authoring site).

Public entry points for downstream reuse:
    - ``repo_root`` — resolve the shared-core repository root.
For notebook presentation logic, import ``eaa.notebooks.archival`` (see ``docs/public_interfaces.md``).
"""

from eaa.paths import repo_root

__all__ = ["repo_root"]
