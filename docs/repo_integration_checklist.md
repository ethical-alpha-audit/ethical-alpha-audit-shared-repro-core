# Shared Core Repo Integration Checklist

1. Confirm every notebook writes only to `outputs/`.
2. Verify expected SHA-256 values in `config/expected_outputs.json` match a validated execution run.
3. Lock notebook order in `config/notebook_plan.json` before submission.
4. Re-run `python reproduce_all.py` before every release tag and manuscript update.
5. Verify `CITATION.cff` metadata is complete and valid.
6. Verify `.zenodo.json` matches current repository description.
7. Confirm static HTML archival exports in `docs/archival_html/` are current.
