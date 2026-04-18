"""Import-surface checks: catch broken imports and accidental circular dependencies."""

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_module_from_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_eaa_and_engine_import_chain():
    """eaa package and engine module load without cycles."""
    root = _repo_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    import eaa  # noqa: F401

    importlib.import_module("eaa.paths")
    importlib.import_module("eaa.notebooks.archival")

    sys.path.insert(0, str(root / "engine"))
    importlib.import_module("corrected_public_engine_v1_1")


def test_notebook_helper_shims_importable():
    """Path-stable notebook helpers resolve to eaa.paths (no duplicate repo_root)."""
    root = _repo_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    ref = _load_module_from_path(
        "eaa_test_ref_helpers",
        root / "notebooks" / "reference" / "reference_notebook_helpers.py",
    )
    assert callable(ref.repo_root)
    assert ref.repo_root() == root

    ui = _load_module_from_path(
        "eaa_test_ui_gate_explorer",
        root / "notebooks" / "website_interactive" / "ui_gate_explorer.py",
    )
    assert callable(ui.repo_root)
    assert ui.repo_root() == root
