from __future__ import annotations

import os
import sys
from pathlib import Path

import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd
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


def _get_engine_module():
    root = repo_root()
    engine_path = str(root / "engine")
    if engine_path not in sys.path:
        sys.path.insert(0, engine_path)
    import corrected_public_engine_v1_1 as eng
    return eng


def _build_scenarios(eng):
    return [
        {
            "label": "smoke_core_001 (replay reference)",
            "case": {
                "case_id": "smoke_core_001",
                "features": {
                    "intrinsic_safety": 0.58,
                    "evidence_strength": 0.55,
                    "bias_harm_index": 0.44,
                    "uncertainty_calibration": 0.52,
                    "traceability_integrity": 0.53,
                },
            },
            "mode": eng.MODE_REPLAY,
        },
        {
            "label": "demo_replay_pass (full mode)",
            "case": {
                "case_id": "demo_replay_pass",
                "features": {
                    "intrinsic_safety": 0.62,
                    "evidence_strength": 0.60,
                    "bias_harm_index": 0.40,
                    "uncertainty_calibration": 0.58,
                    "traceability_integrity": 0.57,
                },
            },
            "mode": eng.MODE_CANONICAL_FULL,
        },
        {
            "label": "demo_gate_fail (full mode)",
            "case": {
                "case_id": "demo_gate_fail",
                "features": {
                    "intrinsic_safety": 0.35,
                    "evidence_strength": 0.60,
                    "bias_harm_index": 0.40,
                    "uncertainty_calibration": 0.58,
                    "traceability_integrity": 0.57,
                },
            },
            "mode": eng.MODE_CANONICAL_FULL,
        },
        {
            "label": "demo_fullmode_abstention",
            "case": {
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
            "mode": eng.MODE_CANONICAL_FULL,
        },
    ]


def launch_gate_explorer_ui() -> None:
    """Launch bounded, presentation-only widget interface."""
    try:
        _launch_gate_explorer_ui_impl()
    except Exception as exc:  # pragma: no cover - Binder/kernel UX guardrail
        display(
            widgets.HTML(
                "<p><b>Demonstration could not start.</b> Try "
                "<em>Kernel → Restart Kernel and Run All Cells</em>.</p>"
                f"<pre style='white-space:pre-wrap'>{exc!r}</pre>"
            )
        )


def _launch_gate_explorer_ui_impl() -> None:
    eng = _get_engine_module()
    scenarios = _build_scenarios(eng)

    scenario_dd = widgets.Dropdown(
        options=[s["label"] for s in scenarios],
        value=scenarios[0]["label"],
        description="Scenario:",
        style={"description_width": "initial"},
    )

    profile_dd = widgets.Dropdown(
        options=["permissive", "moderate", "strict", "very_strict"],
        value="moderate",
        description="Profile:",
        style={"description_width": "initial"},
    )

    components_toggle = widgets.Checkbox(value=True, description="Show gate/component values")
    details_toggle = widgets.Checkbox(value=True, description="Show SCM/abstention details (full mode)")
    show_chart_toggle = widgets.Checkbox(value=True, description="Show chart")
    show_summary_toggle = widgets.Checkbox(value=True, description="Show verdict & interpretation")

    controls_box = widgets.VBox([
        scenario_dd,
        profile_dd,
        components_toggle,
        details_toggle,
        show_chart_toggle,
        show_summary_toggle,
    ])

    chart_out = widgets.Output(layout={"border": "1px solid #ccc", "padding": "6px"})
    verdict_out = widgets.Output(layout={"border": "1px solid #ccc", "padding": "6px"})
    interp_out = widgets.Output(layout={"border": "1px solid #ccc", "padding": "6px"})

    gate_cols = [
        ("gate_safety", "Safety"),
        ("gate_evidence", "Evidence"),
        ("gate_bias", "Bias cap"),
        ("gate_calibration", "Calibration"),
        ("gate_traceability", "Traceability"),
    ]

    def render() -> None:
        scenario = next(s for s in scenarios if s["label"] == scenario_dd.value)
        result = eng.evaluate_case(
            scenario["case"], profile_name=profile_dd.value, mode=scenario["mode"]
        )
        gate_values = [result[k] for k, _ in gate_cols]

        with chart_out:
            clear_output(wait=True)
            if show_chart_toggle.value:
                plt.close("all")
                fig, ax = plt.subplots(figsize=(7, 3.5))
                ax.bar([lbl for _, lbl in gate_cols], gate_values, color="#2c6e49")
                ax.set_ylim(0, 1.05)
                ax.set_ylabel("Pass (1) / Fail (0)")
                ax.set_title(f"{scenario['label']} — {profile_dd.value}")
                plt.tight_layout()
                plt.show()
            else:
                print("Chart hidden.")

        with verdict_out:
            clear_output(wait=True)
            if show_summary_toggle.value:
                summary = pd.Series(
                    {
                        "governance_outcome": result["governance_outcome"],
                        "approved": result["approved"],
                        "compensatory_score": result["compensatory_score"],
                        "mode": result["mode"],
                    }
                )
                print("Verdict summary (display only):")
                display(summary)

                if components_toggle.value:
                    print("\\nGate/component values:")
                    print(f"All gates pass: {result['all_gates_pass']}")
                    for key, label in gate_cols:
                        print(f"  {label}: {result[key]}")
                    print(f"Failed gates (binding constraints): {result.get('binding_constraints', [])}")
                    print(f"Compensatory approved: {result['compensatory_approved']}")
            else:
                print("Verdict summary hidden.")

        with interp_out:
            clear_output(wait=True)
            if show_summary_toggle.value:
                mode = result.get("mode")
                approved = int(result.get("approved"))

                print(
                    "Interpretation: The bar chart shows gate pass/fail (1=pass, 0=fail) under the selected profile. "
                    "For the bias gate, lower bias-harm index is better."
                )
                if mode == eng.MODE_REPLAY:
                    print("Replay mode: final decision follows gate outcomes only.")
                else:
                    print("Full mode: SCM abstention/fallback checks can veto approval after gates are evaluated.")

                print("Result: APPROVAL." if approved == 1 else "Result: REJECTION.")

                if mode == eng.MODE_CANONICAL_FULL and details_toggle.value:
                    if "abstention_rate" in result:
                        abst_trig = int(result.get("abstention_triggered", 0))
                        fallback_ok = int(result.get("fallback_adequate", 0))
                        print(
                            f"SCM details: abstention_rate={result.get('abstention_rate')}, "
                            f"abstention_triggered={abst_trig}, fallback_adequate={fallback_ok}."
                        )

                if approved == 1:
                    print("Why: The selected scenario satisfies approval conditions under the chosen mode/profile.")
                else:
                    if result.get("all_gates_pass") == 0:
                        print("Why: One or more governance gates failed under the chosen profile.")
                    elif mode == eng.MODE_CANONICAL_FULL:
                        print("Why: Gates passed, but full-mode abstention/fallback veto blocked approval.")
            else:
                print("Interpretation hidden.")

    def _on_change(change):
        if change.get("name") == "value":
            render()

    for w in (
        scenario_dd,
        profile_dd,
        components_toggle,
        details_toggle,
        show_chart_toggle,
        show_summary_toggle,
    ):
        w.observe(_on_change, names="value")

    display(widgets.VBox([controls_box, chart_out, verdict_out, interp_out]))
    render()
