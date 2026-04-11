import hashlib
import json
import subprocess
import sys
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


def git_blob_bytes_at_head(rel_path: str) -> tuple[bytes | None, str | None]:
    """Return (blob_bytes, None) from `git show HEAD:<path>`, or (None, reason).

    Manifest SHA-256 values match git's stored objects (LF-normalized for text).
    Hashing the working tree on Windows can false-fail when `.gitattributes`
    checks out CRLF; reading the blob avoids comparing platform-specific bytes.
    """
    try:
        proc = subprocess.run(
            ["git", "show", f"HEAD:{rel_path}"],
            cwd=BASE_DIR,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        return None, str(exc)
    if proc.returncode != 0:
        err = (proc.stderr or b"").decode(errors="replace").strip()
        return None, err or f"git exit {proc.returncode}"
    return proc.stdout, None


def verify() -> list[str]:
    mf_path = BASE_DIR / "config" / "shared_logic_manifest.json"
    manifest = json.loads(mf_path.read_text(encoding="utf-8"))
    failures = []
    for item in manifest["entries"]:
        rel = item["path"]
        expected = item["sha256"]
        p = BASE_DIR / rel
        blob, git_err = git_blob_bytes_at_head(rel)
        used_fallback = False
        if blob is not None:
            got = sha256_bytes(blob)
        else:
            if not p.is_file():
                failures.append(
                    f"Missing file: {rel} (git blob read failed: {git_err})"
                )
                continue
            # Last resort: working-tree bytes may differ from manifest on Windows (CRLF).
            print(
                f"parity: on-disk fallback for {rel} (git blob unavailable: {git_err})",
                file=sys.stderr,
            )
            got = sha256_file(p)
            used_fallback = True
        if got != expected:
            suffix = (
                " [on-disk fallback after git blob read failed]"
                if used_fallback
                else ""
            )
            failures.append(
                f"Hash drift {rel}: manifest={expected} actual={got}{suffix}"
            )
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
