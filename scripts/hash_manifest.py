import hashlib
import json
import os
import tempfile
from pathlib import Path
from datetime import datetime, UTC

BASE_DIR = Path(__file__).resolve().parents[1]


def _write_json_atomic(path: Path, data: dict) -> None:
    """Write JSON via a temp file + replace (more reliable on Windows than reopen-in-place)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        dir=path.parent,
        delete=False,
        prefix=f"{path.stem}.",
        suffix=".tmp.json",
    ) as tmp:
        tmp.write(payload)
        tmp.flush()
        tmp_path = tmp.name
    os.replace(tmp_path, path)

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def build_manifest():
    config_path = BASE_DIR / "config" / "expected_outputs.json"
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    manifest = {"generated_at": datetime.now(UTC).isoformat(), "files": []}
    for item in config["files"]:
        file_path = BASE_DIR / item["path"]
        if file_path.exists():
            manifest["files"].append({"path": item["path"], "sha256": sha256_file(file_path), "exists": True})
        else:
            manifest["files"].append({"path": item["path"], "sha256": "", "exists": False})
    out_path = BASE_DIR / "logs" / "actual_manifest.json"
    _write_json_atomic(out_path, manifest)
    return out_path

if __name__ == "__main__":
    path = build_manifest()
    print(f"Manifest written to {path}")
