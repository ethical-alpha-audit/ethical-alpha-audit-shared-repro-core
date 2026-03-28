# Shared Core Repo Integration Checklist

1. Replace placeholder notebooks with the real notebooks while preserving filenames or update notebook_plan.json.
2. Confirm every notebook writes only to /outputs.
3. Replace placeholder expected SHA256 values after the first validated release-candidate run.
4. Lock notebook order before submission.
5. Re-run python reproduce_all.py before every release tag and manuscript update.
