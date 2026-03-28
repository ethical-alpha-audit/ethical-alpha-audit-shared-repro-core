from pathlib import Path

def test_repo_scaffold_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "README.md").exists()
    assert (root / "notebooks").exists()
    assert (root / "data" / "README.md").exists()
    assert (root / "reproduce_all.py").exists()
