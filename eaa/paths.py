"""Repository root discovery for shared archival tooling."""

from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
    """Resolve repository root from env override or parent-anchor scan."""
    env_root = os.environ.get("EAA_REPO_ROOT")
    if env_root:
        p = Path(env_root).expanduser().resolve()
        if (p / "engine" / "corrected_public_engine_v1_1.py").is_file():
            return p

    start = Path.cwd().resolve()
    anchors = [
        Path("engine") / "corrected_public_engine_v1_1.py",
        Path("config") / "notebook_plan.json",
        Path("reproduce_all.py"),
    ]
    for p in (start, *start.parents):
        if all((p / a).exists() for a in anchors):
            return p
    raise RuntimeError(
        f"Repository root not found from cwd={start}. Expected anchors: {anchors}"
    )
