"""
Back-compat import surface for notebooks under notebooks/archival_shared/.

Canonical implementation is authored only in SHARED CORE under eaa/notebooks/archival.py.
Consumers outside this repository must hold verified copies and pass parity CI.
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from eaa.notebooks.archival import (  # noqa: E402
    launch_01_smoke_interactive,
    launch_02_utilities_interactive,
    launch_03_demo_pipeline_interactive,
    run_01_smoke_test_contract_only,
    run_01_smoke_test_notebook,
    run_02_utilities_validation_contract_only,
    run_02_utilities_validation_notebook,
    run_03_demo_pipeline_contract_only,
    run_03_demo_pipeline_notebook,
)

__all__ = [
    "launch_01_smoke_interactive",
    "launch_02_utilities_interactive",
    "launch_03_demo_pipeline_interactive",
    "run_01_smoke_test_contract_only",
    "run_01_smoke_test_notebook",
    "run_02_utilities_validation_contract_only",
    "run_02_utilities_validation_notebook",
    "run_03_demo_pipeline_contract_only",
    "run_03_demo_pipeline_notebook",
]
