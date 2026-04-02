import json
import sys
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter

BASE_DIR = Path(__file__).resolve().parents[1]
EXPORT_DIR = BASE_DIR / "docs" / "notebook_exports"


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def export_all() -> list[str]:
    plan = load_json(BASE_DIR / "config" / "notebook_plan.json")
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    exporter = HTMLExporter()
    exporter.exclude_input_prompt = True
    exporter.exclude_output_prompt = True
    written = []
    for item in plan["execution_order"]:
        rel = item if isinstance(item, str) else item["path"]
        nb_path = BASE_DIR / rel
        if not nb_path.is_file():
            raise FileNotFoundError(f"Notebook not found: {nb_path}")
        with open(nb_path, encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        body, _resources = exporter.from_notebook_node(nb)
        out_html = EXPORT_DIR / f"{nb_path.stem}.html"
        out_html.write_text(body, encoding="utf-8")
        written.append(str(out_html.relative_to(BASE_DIR)))
    return written


def main() -> None:
    paths = export_all()
    for p in paths:
        print(f"Exported {p}")
    print("HTML export complete.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"EXPORT FAILED: {exc}", file=sys.stderr)
        sys.exit(1)
