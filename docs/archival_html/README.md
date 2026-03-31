# Archival HTML exports

Static HTML renderings of the primary reader-facing (story) notebooks, generated for long-term archival and reviewer accessibility per Rule 9 of "Ten Simple Rules for Reproducible Research in Jupyter Notebooks" (Rule et al.).

These files are read-only snapshots. For interactive exploration, run the paired `*_interactive.ipynb` notebooks. For cryptographic validation of outputs, run `python reproduce_all.py` from the repository root.

| File | Source notebook |
|------|----------------|
| `01_smoke_test.html` | `notebooks/archival_shared/01_smoke_test.ipynb` |
| `02_utilities_validation.html` | `notebooks/archival_shared/02_utilities_validation.ipynb` |
| `03_demo_pipeline.html` | `notebooks/archival_shared/03_demo_pipeline.ipynb` |
| `01_gate_explorer_story.html` | `notebooks/website_interactive/01_gate_explorer_story.ipynb` |
| `00_about_layer.html` | `notebooks/website_interactive/00_about_layer.ipynb` |

**Format note:** HTML is used as the archival static format for portability and reviewer readability. PDF export is not included because the lightweight HTML rendering is more robust and does not introduce brittle external dependencies.
