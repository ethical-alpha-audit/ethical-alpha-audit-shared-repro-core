import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    inv_path = BASE_DIR / "config" / "shared_logic_inventory.json"
    inv = json.loads(inv_path.read_text(encoding="utf-8"))
    out_path = BASE_DIR / Path(inv.get("manifest_output_path", "config/shared_logic_manifest.json"))
    paths = list(inv["governed_paths"])
    if inv.get("manifest_output_path") in paths:
        print("Inventory must not list manifest_output_path inside governed_paths.", file=sys.stderr)
        sys.exit(1)
    entries = []
    for rel in paths:
        p = BASE_DIR / rel
        if not p.is_file():
            print(f"MISSING governed file: {rel}", file=sys.stderr)
            sys.exit(1)
        entries.append({"path": rel, "sha256": sha256_file(p)})
    doc = {
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "inventory_schema_version": inv.get("schema_version"),
        "entries": sorted(entries, key=lambda x: x["path"]),
    }
    out_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path.relative_to(BASE_DIR)} with {len(entries)} entries.")


if __name__ == "__main__":
    main()
