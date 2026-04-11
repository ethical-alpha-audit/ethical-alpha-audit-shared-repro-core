import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_bytes_at_head(rel_path: str) -> bytes | None:
    """Canonical bytes for manifest hashing: match git objects at HEAD (LF for text).

    Working-tree reads can embed CRLF on Windows under `.gitattributes`; parity
    verification uses blob bytes, so the manifest must record the same.
    """
    try:
        proc = subprocess.run(
            ["git", "show", f"HEAD:{rel_path}"],
            cwd=BASE_DIR,
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


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
        blob = git_blob_bytes_at_head(rel)
        digest = sha256_bytes(blob) if blob is not None else sha256_file(p)
        entries.append({"path": rel, "sha256": digest})
    doc = {
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "inventory_schema_version": inv.get("schema_version"),
        "entries": sorted(entries, key=lambda x: x["path"]),
    }
    out_path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_path.relative_to(BASE_DIR)} with {len(entries)} entries.")


if __name__ == "__main__":
    main()
