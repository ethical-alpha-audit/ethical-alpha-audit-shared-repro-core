
from pathlib import Path


def test_eaa_package_exports_repo_root():
    import eaa

    assert hasattr(eaa, "repo_root")
    assert callable(eaa.repo_root)
    root = eaa.repo_root()
    assert (root / "reproduce_all.py").is_file()


def test_harness_core_files_exist():
    base = Path(__file__).resolve().parents[1]
    required = [
        base / "reproduce_all.py",
        base / "config" / "notebook_plan.json",
        base / "config" / "expected_outputs.json",
        base / "config" / "harness_settings.json",
        base / "inputs",
    ]
    for path in required:
        assert path.exists(), f"Missing required file: {path}"
