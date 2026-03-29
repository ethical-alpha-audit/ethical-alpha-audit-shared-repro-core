# Shared Reproducibility Core Repository  
**Reusable utilities, validation routines, schemas, loaders, and plotting tools shared across downstream analysis repos.**

This root README unifies two previously separate roles:

1. **Shared Core Library** (primary, reusable cross‑repo functionality)  
2. **Deterministic Paper Harness** (repository‑specific smoke tests & validation demos)

Both roles remain distinct, but now appear in a structured, integrated way.

---

# 1. Purpose

## 1.1 Shared Core Purpose
This repository provides:

- Common loaders and helpers  
- Reproducibility utilities  
- Validation routines  
- Shared schemas  
- Plotting helpers used in multiple paper repositories  

It is the shared backbone to ensure **deterministic, traceable, reproducible results** across research outputs.

## 1.2 Deterministic Harness Purpose
A lightweight, deterministic execution harness is included to:

- Smoke‑test the shared core  
- Validate utilities work in a clean environment  
- Produce stable example outputs  
- Provide a minimal demonstration pipeline  

This harness is intentionally simple and is expected to evolve as the repo matures.

---

# 2. Release Target

Planned release tag: **`v1.0.0-initial`**

The release will include:

- Public GitHub repository  
- Zenodo‑linked archival snapshot  
- Reproducibility manifest & hash bundle  
- Notebook set  
- Manuscript + supplement  
- Version‑locked environment files  

---

# 3. Required Public-Facing Components

- GitHub repository with version tags  
- Zenodo archived release  
- Ordered Jupyter notebook set  
- Versioned manuscript and supplementary materials  
- Reproducibility manifest with output hashes  

---

# 4. Suggested First-Release Checklist

1. Finalise manuscript title, author list, and metadata  
2. Replace placeholder DOI/repo links in manuscript with final release values  
3. Populate `data/README.md` with schema, provenance, and access notes  
4. Freeze environments:  
   - `environment.yml`  
   - `requirements.txt`  
   - `environment.lock`  
5. Run `python reproduce_all.py` end‑to‑end  
6. Regenerate:  
   - `repro_manifest.json`  
   - `MANIFEST.sha256`  
7. Create GitHub release: `v1.0.0-initial`  
8. Confirm Zenodo successfully captured the GitHub release  
9. Insert Zenodo DOI into manuscript and release notes  

---

# 5. Repository Structure & Folder Expectations

| Folder | Purpose |
|--------|---------|
| `manuscript/` | Manuscript, supplement, reviewer response |
| `notebooks/` | Ordered reproducible notebooks (top‑to‑bottom execution) |
| `src/` | Reusable shared-core code |
| `data/` | Raw, processed, and documentation subfolders |
| `outputs/` | Generated figures, tables, logs, artefacts |
| `tests/` | Deterministic tests and reproducibility checks |
| `docs/` | Methods, provenance notes, architectural documentation |
| `config/` | Configuration contracts (trace map, presentation config) |

---

# 6. Notebook Inventory (Shared Core)

- **`01_core_demo.ipynb`** — Demonstration of shared utilities  
- **`02_validation_demo.ipynb`** — Core validation routine showcase  

---

# 7. Deterministic Harness (Paper-Specific)

The deterministic harness bundled with this repo is configured for:

**Repository:** `eaa-shared-repro-core`  
**Role:** Smoke testing, deterministic validation, demonstration pipeline

## Included notebook order
1. **01_smoke_test.ipynb**  
   - Outputs:  
     - `outputs/tables/smoke_test_results.csv`  
     - `outputs/figures/smoke_test_summary.txt`  
2. **02_utilities_validation.ipynb**  
   - Output: `outputs/tables/utilities_validation.csv`  
3. **03_demo_pipeline.ipynb**  
   - Output: `outputs/figures/demo_pipeline_summary.txt`  

## Usage
```bash
python reproduce_all.py
```

Update the notebook plan and output list as soon as real notebooks and artefacts are added.

---

# 8. Immediate Next Actions

- Fill in manuscript metadata  
- Replace stub notebooks with real content  
- Ensure Zenodo integration is enabled  
- Generate a clean first tagged release  

---

# 9. Contact & Maintenance

This repository is maintained as part of the shared reproducibility infrastructure.  
Please coordinate changes affecting the shared core with other repos depending on it.
