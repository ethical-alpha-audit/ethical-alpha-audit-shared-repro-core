import json
import sys
from pathlib import Path

import nbformat

BASE_DIR = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _plan_paths(plan: dict) -> list[str]:
    out = []
    for item in plan["execution_order"]:
        out.append(item if isinstance(item, str) else item["path"])
    return out


def validate() -> list[str]:
    failures = []
    expected = load_json(BASE_DIR / "config" / "expected_outputs.json")
    baseline = load_json(BASE_DIR / "config" / "baseline_output_hashes.json")
    if expected["files"] != baseline["files"]:
        failures.append("expected_outputs.json and baseline_output_hashes.json must list identical path+sha256 entries")

    trace = load_json(BASE_DIR / "config" / "trace_map.json")
    plan = load_json(BASE_DIR / "config" / "notebook_plan.json")
    plan_notebooks = _plan_paths(plan)

    # Output-keyed trace_map (path -> { notebook, role }); derive notebook -> outputs
    nb_to_outputs: dict[str, list[str]] = {}
    traced_outputs: set[str] = set()
    for out_path, spec in trace.items():
        if not isinstance(spec, dict) or "notebook" not in spec:
            failures.append(f"trace_map.json bad entry for {out_path!r}")
            continue
        traced_outputs.add(out_path)
        nb_to_outputs.setdefault(spec["notebook"], []).append(out_path)

    for nb in plan_notebooks:
        if nb not in nb_to_outputs:
            failures.append(f"trace_map.json has no outputs claiming notebook: {nb}")

    for item in expected["files"]:
        if item["path"] not in traced_outputs:
            failures.append(
                f"expected output {item['path']} is not listed in trace_map.json"
            )

    for rel in plan_notebooks:
        nb_path = BASE_DIR / rel
        if not nb_path.suffix == ".ipynb":
            failures.append(f"Plan entry is not .ipynb: {rel}")
            continue
        with open(nb_path, encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        try:
            nbformat.validate(nb)
        except Exception as exc:
            failures.append(f"{rel}: nbformat validation failed: {exc}")
            continue
        meta = nb.metadata.get("kernelspec", {})
        lang = meta.get("language", "")
        name = meta.get("name", "")
        if lang != "python" or name != "python3":
            failures.append(
                f"{rel}: require kernelspec language=python and name=python3 (got language={lang!r} name={name!r})"
            )
        if len(nb.cells) < 2:
            failures.append(f"{rel}: need at least 2 cells")
            continue
        if nb.cells[0].get("cell_type") != "markdown":
            failures.append(f"{rel}: first cell must be markdown (reader-first contract)")
        if nb.cells[1].get("cell_type") != "code":
            failures.append(f"{rel}: second cell must be code (execute harness contract)")

    return failures


def main() -> None:
    failures = validate()
    if failures:
        print("NOTEBOOK STANDARD VALIDATION FAILED")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("NOTEBOOK STANDARD VALIDATION PASSED")


if __name__ == "__main__":
    main()
