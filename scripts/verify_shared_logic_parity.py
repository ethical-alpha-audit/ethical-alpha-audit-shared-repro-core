import hashlib
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def verify() -> list[str]:
    mf_path = BASE_DIR / "config" / "shared_logic_manifest.json"
    manifest = json.loads(mf_path.read_text(encoding="utf-8"))
    failures = []
    for item in manifest["entries"]:
        rel = item["path"]
        expected = item["sha256"]
        p = BASE_DIR / rel
        if not p.is_file():
            failures.append(f"Missing file: {rel}")
            continue
        got = sha256_file(p)
        if got != expected:
            failures.append(f"Hash drift {rel}: manifest={expected} actual={got}")
    return failures


def main() -> None:
    failures = verify()
    if failures:
        print("PARITY VERIFICATION FAILED")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print("PARITY VERIFICATION PASSED")


if __name__ == "__main__":
    main()
