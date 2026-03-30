"""
Archival shared notebooks — presentation/runtime implementation.

All scientific evaluation uses engine/corrected_public_engine_v1_1.py only.
This module holds imports, path setup, bounded widget UI, and canonical
output writes so notebook files stay reader-first.
"""
from __future__ import annotations

import csv
import os
import sys
from pathlib import Path

import ipywidgets as widgets
from IPython.display import clear_output, display


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


def launch_01_smoke_interactive() -> None:
    """Bounded scenario exploration (display only; no contract files)."""
    ROOT = repo_root()
    sys.path.insert(0, str(ROOT / "engine"))
    import corrected_public_engine_v1_1 as eng

    ARCHIVAL_CASE = {
        "case_id": "smoke_core_001",
        "features": {
            "intrinsic_safety": 0.58,
            "evidence_strength": 0.55,
            "bias_harm_index": 0.44,
            "uncertainty_calibration": 0.52,
            "traceability_integrity": 0.53,
        },
    }

    EXPLORATION_CASES = {
        "Archival contract (replay)": ARCHIVAL_CASE,
        "Low intrinsic safety (replay)": {
            "case_id": "explore_low_safety",
            "features": {
                "intrinsic_safety": 0.35,
                "evidence_strength": 0.60,
                "bias_harm_index": 0.40,
                "uncertainty_calibration": 0.58,
                "traceability_integrity": 0.57,
            },
        },
    }

    def evaluate_replay(case: dict) -> dict:
        return eng.evaluate_case(case, profile_name="moderate", mode=eng.MODE_REPLAY)

    explore_out = widgets.Output(layout={"border": "1px solid #ccc", "padding": "6px"})
    dd = widgets.Dropdown(
        options=list(EXPLORATION_CASES.keys()),
        value="Archival contract (replay)",
        description="Scenario:",
        style={"description_width": "initial"},
    )

    def _render_exploration(label: str) -> None:
        with explore_out:
            clear_output(wait=True)
            case = EXPLORATION_CASES[label]
            r = evaluate_replay(case)
            print(f"Scenario: {label}  |  case_id={case['case_id']}")
            print(f"  governance_outcome: {r['governance_outcome']}")
            print(f"  approved: {r['approved']}  |  all_gates_pass: {r['all_gates_pass']}")
            print(f"  compensatory_score: {r['compensatory_score']}")

    def _on_dd(change) -> None:
        if change.get("name") == "value" and change.get("new") is not None:
            _render_exploration(change["new"])

    dd.observe(_on_dd, names="value")
    _render_exploration(dd.value)
    display(dd)
    display(explore_out)


def run_01_smoke_test_contract_only() -> None:
    """Write smoke_test CSV + summary from the fixed archival case only."""
    ROOT = repo_root()
    sys.path.insert(0, str(ROOT / "engine"))
    import corrected_public_engine_v1_1 as eng

    OUT_TAB = ROOT / "outputs" / "tables"
    OUT_FIG = ROOT / "outputs" / "figures"
    OUT_TAB.mkdir(parents=True, exist_ok=True)
    OUT_FIG.mkdir(parents=True, exist_ok=True)

    ARCHIVAL_CASE = {
        "case_id": "smoke_core_001",
        "features": {
            "intrinsic_safety": 0.58,
            "evidence_strength": 0.55,
            "bias_harm_index": 0.44,
            "uncertainty_calibration": 0.52,
            "traceability_integrity": 0.53,
        },
    }

    result = eng.evaluate_case(ARCHIVAL_CASE, profile_name="moderate", mode=eng.MODE_REPLAY)
    result_hash = eng.hash_output(result)

    csv_path = OUT_TAB / "smoke_test_results.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "case_id",
                "profile_name",
                "mode",
                "governance_outcome",
                "all_gates_pass",
                "compensatory_score",
                "compensatory_approved",
                "approved",
                "result_sha256",
            ]
        )
        w.writerow(
            [
                result["case_id"],
                result["profile_name"],
                result["mode"],
                result["governance_outcome"],
                result["all_gates_pass"],
                result["compensatory_score"],
                result["compensatory_approved"],
                result["approved"],
                result_hash,
            ]
        )

    summary_path = OUT_FIG / "smoke_test_summary.txt"
    lines = [
        "Shared-core smoke test (01_smoke_test)",
        "========================================",
        "",
        "Purpose: This notebook runs one fixed synthetic governance case through the",
        "corrected public engine v1.1 in replay_mode (five gates plus compensatory",
        "scoring only, matching the static historical replay path).",
        "",
        "Why this matters: A successful run proves the checked-out engine module",
        "executes end-to-end and that we can serialize a deterministic record under",
        "config/expected_outputs.json for automated manifest validation.",
        "",
        "Outputs produced (this notebook only):",
        "- outputs/tables/smoke_test_results.csv — tabular record for the case.",
        "- outputs/figures/smoke_test_summary.txt — this narrative summary.",
        "",
        f"Governance outcome:                  {result['governance_outcome']}",
        f"All gates pass (replay):             {result['all_gates_pass']}",
        f"Compensatory approved:               {result['compensatory_approved']}",
        f"Final approved flag (replay):       {result['approved']}",
        f"SHA-256 (canonical JSON result):    {result_hash}",
        "",
    ]
    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Smoke test artifacts written.")


def run_01_smoke_test_notebook() -> None:
    """Back-compat: exploration then contract (same observable behaviour as prior single notebook)."""
    launch_01_smoke_interactive()
    run_01_smoke_test_contract_only()


def launch_02_utilities_interactive() -> None:
    """Feature-preset exploration (display only; no CSV)."""
    ROOT = repo_root()
    sys.path.insert(0, str(ROOT / "engine"))
    import corrected_public_engine_v1_1 as eng

    ARCHIVAL_FEATURES = {
        "intrinsic_safety": 0.60,
        "evidence_strength": 0.58,
        "bias_harm_index": 0.42,
        "uncertainty_calibration": 0.55,
        "traceability_integrity": 0.56,
    }

    FEATURE_PRESETS = {
        "Archival contract vector": ARCHIVAL_FEATURES,
        "Higher safety emphasis": {
            "intrinsic_safety": 0.75,
            "evidence_strength": 0.58,
            "bias_harm_index": 0.42,
            "uncertainty_calibration": 0.55,
            "traceability_integrity": 0.56,
        },
    }

    def summarize_utilities(features: dict) -> dict:
        profile = eng.CANONICAL_THRESHOLD_PROFILES["moderate"]
        gates = eng.evaluate_gates(features, profile)
        comp = eng.compute_compensatory_score(features)
        am = eng.compute_abstention_rate(0.5)
        auc = eng.compute_abstention_rate(features["uncertainty_calibration"])
        return {
            "all_gates_pass": gates["all_gates_pass"],
            "binding_n": len(gates["binding_constraints"]),
            "compensatory_score": round(comp, 6),
            "abstention_mid": round(am, 6),
            "abstention_uc": round(auc, 6),
        }

    u_out = widgets.Output(layout={"border": "1px solid #ccc", "padding": "6px"})
    udd = widgets.Dropdown(
        options=list(FEATURE_PRESETS.keys()),
        value="Archival contract vector",
        description="Feature preset:",
        style={"description_width": "initial"},
    )

    def _render_u(label: str) -> None:
        with u_out:
            clear_output(wait=True)
            feats = FEATURE_PRESETS[label]
            s = summarize_utilities(feats)
            print(f"Preset: {label}")
            for k, v in s.items():
                print(f"  {k}: {v}")

    def _on_u(change) -> None:
        if change.get("name") == "value" and change.get("new") is not None:
            _render_u(change["new"])

    udd.observe(_on_u, names="value")
    _render_u(udd.value)
    display(udd)
    display(u_out)


def run_02_utilities_validation_contract_only() -> None:
    """Write utilities_validation.csv from the archival feature vector only."""
    ROOT = repo_root()
    sys.path.insert(0, str(ROOT / "engine"))
    import corrected_public_engine_v1_1 as eng

    ARCHIVAL_FEATURES = {
        "intrinsic_safety": 0.60,
        "evidence_strength": 0.58,
        "bias_harm_index": 0.42,
        "uncertainty_calibration": 0.55,
        "traceability_integrity": 0.56,
    }

    FEATURES = ARCHIVAL_FEATURES

    profile = eng.CANONICAL_THRESHOLD_PROFILES["moderate"]
    gates = eng.evaluate_gates(FEATURES, profile)
    comp_score = eng.compute_compensatory_score(FEATURES)
    abstention_mid = eng.compute_abstention_rate(0.5)
    abstention_uc = eng.compute_abstention_rate(FEATURES["uncertainty_calibration"])

    fixture = {"case_id": "hash_fixture", "features": FEATURES}
    batch = eng.evaluate_batch([fixture], profile_names=["moderate"], mode=eng.MODE_REPLAY)
    batch_hash = eng.hash_output(batch)

    rows = [
        ("evaluate_gates_all_pass", gates["all_gates_pass"]),
        ("binding_constraints_count", len(gates["binding_constraints"])),
        ("compensatory_score", round(comp_score, 6)),
        ("abstention_rate_at_uc_0.5", round(abstention_mid, 6)),
        ("abstention_rate_case_uc", round(abstention_uc, 6)),
        ("hash_batch_fixture_sha256", batch_hash),
    ]

    out_path = ROOT / "outputs" / "tables" / "utilities_validation.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["check_name", "value"])
        for name, val in rows:
            w.writerow([name, val])

    print("Utilities validation CSV written.")


def run_02_utilities_validation_notebook() -> None:
    """Back-compat: exploration then contract write."""
    launch_02_utilities_interactive()
    run_02_utilities_validation_contract_only()


def launch_03_demo_pipeline_interactive() -> None:
    """Slider over fixed archival cases in canonical full mode (display only)."""
    ROOT = repo_root()
    sys.path.insert(0, str(ROOT / "engine"))
    import corrected_public_engine_v1_1 as eng

    ARCHIVAL_CASES = [
        {
            "case_id": "demo_replay_pass",
            "features": {
                "intrinsic_safety": 0.62,
                "evidence_strength": 0.60,
                "bias_harm_index": 0.40,
                "uncertainty_calibration": 0.58,
                "traceability_integrity": 0.57,
            },
        },
        {
            "case_id": "demo_gate_fail",
            "features": {
                "intrinsic_safety": 0.35,
                "evidence_strength": 0.60,
                "bias_harm_index": 0.40,
                "uncertainty_calibration": 0.58,
                "traceability_integrity": 0.57,
            },
        },
        {
            "case_id": "demo_fullmode_abstention",
            "features": {
                "intrinsic_safety": 0.62,
                "evidence_strength": 0.60,
                "bias_harm_index": 0.40,
                "uncertainty_calibration": 0.42,
                "traceability_integrity": 0.50,
                "fallback_safety_delta": 0.15,
            },
        },
    ]

    def evaluate_full_single(case: dict) -> dict:
        return eng.evaluate_case(case, profile_name="moderate", mode=eng.MODE_CANONICAL_FULL)

    idx_out = widgets.Output(layout={"border": "1px solid #ccc", "padding": "6px"})
    slider = widgets.IntSlider(
        value=0,
        min=0,
        max=len(ARCHIVAL_CASES) - 1,
        step=1,
        description="Case index:",
        continuous_update=False,
    )

    def _render_idx(i: int) -> None:
        with idx_out:
            clear_output(wait=True)
            case = ARCHIVAL_CASES[i]
            r = evaluate_full_single(case)
            print(f"case_id={case['case_id']}")
            print(f"  outcome: {r['governance_outcome']}  approved={r['approved']}")
            if "abstention_rate" in r:
                print(
                    f"  abstention_rate={r['abstention_rate']} "
                    f"triggered={r['abstention_triggered']} "
                    f"fallback_adequate={r['fallback_adequate']}"
                )

    def _on_s(change) -> None:
        if change.get("name") == "value":
            _render_idx(int(change["new"]))

    slider.observe(_on_s, names="value")
    _render_idx(int(slider.value))
    display(slider)
    display(idx_out)


def run_03_demo_pipeline_contract_only() -> None:
    """Write demo_pipeline_summary.txt from the fixed archival batch only."""
    ROOT = repo_root()
    sys.path.insert(0, str(ROOT / "engine"))
    import corrected_public_engine_v1_1 as eng

    OUT_FIG = ROOT / "outputs" / "figures"
    OUT_FIG.mkdir(parents=True, exist_ok=True)

    ARCHIVAL_CASES = [
        {
            "case_id": "demo_replay_pass",
            "features": {
                "intrinsic_safety": 0.62,
                "evidence_strength": 0.60,
                "bias_harm_index": 0.40,
                "uncertainty_calibration": 0.58,
                "traceability_integrity": 0.57,
            },
        },
        {
            "case_id": "demo_gate_fail",
            "features": {
                "intrinsic_safety": 0.35,
                "evidence_strength": 0.60,
                "bias_harm_index": 0.40,
                "uncertainty_calibration": 0.58,
                "traceability_integrity": 0.57,
            },
        },
        {
            "case_id": "demo_fullmode_abstention",
            "features": {
                "intrinsic_safety": 0.62,
                "evidence_strength": 0.60,
                "bias_harm_index": 0.40,
                "uncertainty_calibration": 0.42,
                "traceability_integrity": 0.50,
                "fallback_safety_delta": 0.15,
            },
        },
    ]

    CASES = ARCHIVAL_CASES

    batch = eng.evaluate_batch(CASES, profile_names=["moderate"], mode=eng.MODE_CANONICAL_FULL)
    approved = sum(
        1 for cid in batch if batch[cid]["profiles"]["moderate"]["approved"]
    )
    rejected = len(batch) - approved
    digest = eng.hash_output(batch)

    lines = [
        "Shared-core demo pipeline (03_demo_pipeline)",
        "============================================",
        "",
        "Purpose: This notebook runs a small, fixed batch of cases in canonical_full_mode,",
        "so both non-compensatory gates and SCM-derived abstention / fallback logic are",
        "exercised alongside the compensatory layer.",
        "",
        "How it works: Each case is a dict consumed by the engine's evaluate_batch helper.",
        "The moderate threshold profile from the engine's canonical table is used.",
        "",
        "Why this matters: The batch shows contrasting outcomes (approval with defaults,",
        "hard gate failure, and abstention with inadequate fallback) using the same public",
        "entry points the shared core documents.",
        "",
        "Output (this notebook only):",
        "- outputs/figures/demo_pipeline_summary.txt",
        "",
        f"Cases in batch:           {len(CASES)}",
        f"Approved (moderate):      {approved}",
        f"Rejected (moderate):      {rejected}",
        f"Batch digest (SHA-256):   {digest}",
        "",
        "Per-case governance outcomes (moderate profile):",
    ]
    for c in CASES:
        r = batch[c["case_id"]]["profiles"]["moderate"]
        extra = ""
        if "abstention_rate" in r:
            extra = (
                f" abstention_rate={r['abstention_rate']} "
                f"abstention_triggered={r['abstention_triggered']} "
                f"fallback_adequate={r['fallback_adequate']}"
            )
        lines.append(
            f"- {c['case_id']}: {r['governance_outcome']} (approved={r['approved']}){extra}"
        )

    out_path = OUT_FIG / "demo_pipeline_summary.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Demo pipeline summary written.")


def run_03_demo_pipeline_notebook() -> None:
    """Back-compat: interactive preview then contract write."""
    launch_03_demo_pipeline_interactive()
    run_03_demo_pipeline_contract_only()
