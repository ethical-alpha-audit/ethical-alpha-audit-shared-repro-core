"""
Technical reference notebooks — display-only exhibits.

Not part of config/notebook_plan.json. Does not write canonical outputs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from eaa.paths import repo_root  # noqa: E402


def run_core_reference_demo() -> None:
    """Single-case replay evaluation for the smoke reference vector — display only."""
    root = repo_root()
    sys.path.insert(0, str(root / "engine"))
    import corrected_public_engine_v1_1 as eng

    case = {
        "case_id": "smoke_core_001",
        "features": {
            "intrinsic_safety": 0.58,
            "evidence_strength": 0.55,
            "bias_harm_index": 0.44,
            "uncertainty_calibration": 0.52,
            "traceability_integrity": 0.53,
        },
    }
    r = eng.evaluate_case(case, profile_name="moderate", mode=eng.MODE_REPLAY)
    digest = eng.hash_output(r)
    print("Technical reference — core API (display only; no writes under outputs/)")
    print(f"  case_id:               {r['case_id']}")
    print(f"  governance_outcome:    {r['governance_outcome']}")
    print(f"  all_gates_pass:        {r['all_gates_pass']}")
    print(f"  compensatory_score:    {r['compensatory_score']}")
    print(f"  compensatory_approved: {r['compensatory_approved']}")
    print(f"  approved:              {r['approved']}")
    print(f"  result_sha256:         {digest}")
    print()
    print(
        "For hash-locked CSV/summary artefacts, run notebooks/archival_shared/technical/01_smoke_test_execute.ipynb "
        "via reproduce_all.py."
    )


def run_validation_overview_demo() -> None:
    """Summarize cryptographic output contract — does not run the full harness."""
    root = repo_root()
    data = json.loads((root / "config" / "expected_outputs.json").read_text(encoding="utf-8"))
    files = data.get("files", [])
    print("Technical reference — validation contract (expected_outputs.json)")
    print(f"  Pin count: {len(files)}")
    for item in files:
        path = item.get("path", "")
        req = item.get("required", False)
        sha = item.get("sha256", "")
        short = f"{sha[:16]}…" if len(sha) > 16 else sha
        print(f"  - {path}")
        print(f"      required={req}  sha256={short}")
    print()
    print("Full validation: python reproduce_all.py (from repository root).")
