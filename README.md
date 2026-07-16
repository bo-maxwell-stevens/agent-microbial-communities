# Cross-Kingdom Soil Microbial Community Coupling Analysis

## Scientific purpose
This repository tests how strongly soil microbial domains (AMF, BAC, EUK, ITS) co-vary across shared samples, and whether that coupling is structured by abiotic gradients and plant-diversity hypotheses in Dryland DarkDivNet-style field data. The manuscript workflow moves from data quality control and cohort definition to deterministic coupling analysis, inferential validation, BAC-expanded integration, environmental/plant-driver modeling, and final synthesis/figure regeneration.

## Repository structure

- `data/` — read-only raw inputs (OTU/ASV tables, feature metadata, and sample metadata).
- `scripts/` — top-level sequential entrypoints (`01`-`04`) and utility runners.
- `scripts/analysis/` — phase-specific analysis scripts used after Phase 2.
- `scripts/hpc/` — Slurm array wrappers for Rocket production runs (Phase 5A/5B/5C).
- `src/` — shared analysis modules (data loading, preprocessing, coupling metrics, ordination helpers).
- `tests/` — regression, integrity, and unit tests for workflow outputs and shared modules.
- `results/` — phase outputs, checkpoints, and synthesis artifacts.
- `figures/` — manuscript figure package (`main/`, `supplemental/`, `source_data/`, captions, package report).
- `manuscript/` — manuscript versions and release-ready narrative files.
- `docs/` — methods notes, execution guides, audits, and verification reports.

## Analysis workflow

Run in the order below for manuscript reproduction.

| Step | Script | Purpose | Major outputs | Execution |
|---|---|---|---|---|
| 1 | `scripts/01_data_qc.py` | Cross-modality sample harmonization, depth/prevalence QC, parse/repro metadata. | `results/dataset_qc_v2/` (harmonization tables, prevalence/depth summaries, reproducibility metadata), `docs/dataset_qc_v2_report.md` | Local |
| 2 | `scripts/02_define_cohort.py` | Define shared analysis cohort and planning artifacts from canonical overlap. | `results/phase1_ecological_exploration/` (`cohort_definition.json`, overlap and planning files) | Local |
| 3 | `scripts/03_ordination.py` | Deterministic ordination and preprocessing-sensitivity diagnostics for shared cohort. | `results/phase1_5_conservative_ordination/` (ordination summaries, prevalence summary, figures) | Local |
| 4 | `scripts/04_cross_kingdom_coupling.py` | Phase 2 confirmatory pairwise coupling across branches/thresholds. | `results/phase2_confirmatory_coupling/phase2_coupling_summary.csv` and companion phase outputs | Local |
| 5 | `scripts/analysis/phase2_validate_outputs.py` | Validate Phase 2 summary schema/content. | `results/phase2_confirmatory_coupling/validation_summary.txt` | Local |
| 6 | `scripts/analysis/phase4_coupling_inference.py` | Add permutation/CI inference and phase-level figures to deterministic coupling. | `results/phase4_coupling_inference/` (`phase4_summary.csv`, `phase4_mantel_inference.csv`, `phase4_procrustes_bootstrap.csv`, figures) | Local |
| 7 | `scripts/analysis/phase5_bac_integration.py` | Expand coupling framework to BAC-inclusive four-domain comparisons (24 combos). | `results/phase5_bac_integration/` summaries, inference tables, checkpoint files, figures | Rocket production (local smoke test supported) |
| 8 | `scripts/analysis/phase5b_environmental_drivers.py` | dbRDA-style environmental-driver analysis over pair × branch combinations. | `results/phase5b_environmental_drivers/` (`phase5b_dbRDA_summary.csv`, predictor ranking tables, checkpoints, figures) | Rocket production (local smoke test supported) |
| 9 | `scripts/analysis/phase5c_plant_diversity_hypotheses.py` | Hypothesis-driven plant-diversity model comparisons beyond abiotic base. | `results/phase5c_plant_diversity/` model comparison tables, hypothesis summary, checkpoints, figures | Rocket production (local smoke test supported) |
| 10 | `scripts/analysis/phase5d_synthesis.py` | Synthesis-only integration of completed Phase 2/4/5/5B/5C outputs (no new inferential runs). | `results/phase5d_synthesis/` final ranking/synthesis tables and summary figures | Local |
| 11 | `scripts/figures/regenerate_manuscript_figures.py` | Rebuild manuscript figure package from current synthesis outputs. | `figures/main/`, `figures/supplemental/`, `figures/source_data/`, `figures/FIGURE_PACKAGE_REPORT.md` | Local |

## Running locally

### Environment

Use the project virtual environment in the repository root.

```bash
cd /srv/hermes_projects/agent_microbial_communities
source .venv/bin/activate
```

If `.venv/` is missing, repository documentation (`docs/repository_cleanup_plan.md`) records this minimal recreation command:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Core numbered scripts (`01`-`04`)

```bash
.venv/bin/python3 scripts/01_data_qc.py
.venv/bin/python3 scripts/02_define_cohort.py
.venv/bin/python3 scripts/03_ordination.py
.venv/bin/python3 scripts/04_cross_kingdom_coupling.py
```

### Downstream local scripts

```bash
.venv/bin/python3 scripts/analysis/phase2_validate_outputs.py
.venv/bin/python3 scripts/analysis/phase4_coupling_inference.py
.venv/bin/python3 scripts/analysis/phase5d_synthesis.py
.venv/bin/python3 scripts/figures/regenerate_manuscript_figures.py
```

## Running on Rocket HPC

Current production HPC path in Slurm wrappers:

- `~/projects/agent_microbial_communities`

Phases executed on Rocket in production are Phase 5A/5B/5C via Slurm arrays:

- `scripts/hpc/phase5_bac_integration_array.slurm`
- `scripts/hpc/phase5b_environmental_drivers_array.slurm`
- `scripts/hpc/phase5c_plant_diversity_hypotheses_array.slurm`

Typical pattern:

1. Write manifest locally in repo on Rocket (`--write-manifest`).
2. Submit array wrapper with `sbatch`.
3. Monitor with `squeue`/`sacct`.
4. Combine checkpoints after all array tasks succeed (`--combine-checkpoints`).

Expected production outputs:

- Phase 5A: `results/phase5_bac_integration/` final coupling/inference tables + figures.
- Phase 5B: `results/phase5b_environmental_drivers/` dbRDA summaries, predictor rankings, figures.
- Phase 5C: `results/phase5c_plant_diversity/` hypothesis/model summaries and figures.

## Testing

### Targeted regression/integrity tests

```bash
PYTHONPATH=. .venv/bin/pytest -q \
  tests/test_analysis_verification_data_integrity.py \
  tests/test_analysis_verification_regression.py
```

### Full suite

```bash
PYTHONPATH=. .venv/bin/pytest -q
```

Current local run status in this repository state:

- Targeted verification: `16 passed`
- Full suite: `90 passed, 1 warning`

Regression philosophy:

- verify required canonical outputs exist before interpretation,
- guard deterministic numerical behavior (seeding and stable transforms),
- detect schema/value drift in coupling and synthesis tables before manuscript updates.

## Results

Major phase outputs are written under `results/` using phase-scoped directories (`dataset_qc_v2`, `phase1_ecological_exploration`, `phase1_5_conservative_ordination`, `phase2_confirmatory_coupling`, `phase4_coupling_inference`, `phase5_bac_integration`, `phase5b_environmental_drivers`, `phase5c_plant_diversity`, `phase5d_synthesis`). Manuscript-ready figure assets are produced under `figures/` and manuscript text assets under `manuscript/`.

## Reproducibility

- Deterministic analysis design is enforced in core coupling/inference workflows (fixed seeds and explicit transformation branches).
- Regression tests validate both scientific outputs and shared numerical utilities.
- Shared preprocessing modules in `src/preprocessing.py` centralize prevalence filtering, transforms, and distance calculations.
- Shared coupling metrics in `src/coupling_metrics.py` centralize Mantel and Procrustes computations across phases.

## Development philosophy

- Scientific correctness before optimization.
- Regression validation before refactoring.
- Deterministic outputs as a release baseline.
