# Phase 5B Environmental Drivers — Scientific & HPC Implementation Spec

## Scope
Phase 5B evaluates environmental predictors of cross-domain coupling with a **dbRDA-style** constrained workflow and HPC-resumable checkpointing.

## Approved predictor policy

### Primary model (mandatory)
- `pH_KCl`
- `N_pct`
- `bio12now.100`
- `alpha`
- `compl`

### Geography sensitivity model (only as sensitivity)
- primary predictors + `lat`, `lon`

### Explicit exclusions
- `PC1`, `PC2`, `PC3`, `PC4`
- `beta.perc`, `compl.perc`
- `pool`, `dark`, `gamma`
- microbial-derived variables
- ordination-derived variables
- never combine `N_pct` with `C_pct`

## Pair/branch design (Phase 5B combos)
Pairs:
- `BAC↔ITS`
- `AMF↔ITS`
- `EUK↔ITS`
- `AMF↔EUK`

Branches:
- `presence/absence`
- `CLR`

Manifest cardinality:
- `4 pairs × 2 branches = 8 combos`

## Analysis implementation
Script: `scripts/analysis/phase5b_environmental_drivers.py`

For each combo (pair + branch), script runs **both tiers**:
1. primary model
2. geography sensitivity model

Per tier, it reports:
- `r2`
- `adjusted_r2`
- `pseudo_f`
- permutation p-value (`N_PERMUTATIONS`, default `999`)
- leave-one-predictor-out ranking (`delta_r2`, `delta_adj_r2`)

## HPC resumability modes
- `--write-manifest`
- `--single-combo --combo-index <0..7>`
- `--combine-checkpoints`
- `--output-dir <path>`
- `--permutations <int>` (default 999)
- `--figures-only`

### Checkpoint contract
Each single-combo run writes exactly one checkpoint file:
- `results/phase5b_environmental_drivers/checkpoints/combo_<index>.csv`

Checkpoint contains both summary and predictor-ranking records for:
- primary
- geography_sensitivity

## Combined outputs (after all 8 checkpoints)
- `phase5b_dbRDA_summary.csv`
- `phase5b_predictor_ranking.csv`
- `phase5b_pair_rankings.csv`
- `phase5b_manifest.csv`
- `phase5b_run_metadata.json`
- figures (if enabled)

## Reproducibility
- deterministic seed base with combo-index offset
- fixed default permutation count (999)
- explicit combo manifest

## Validation gates
- `.venv/bin/python -m py_compile scripts/analysis/phase5b_environmental_drivers.py`
- `.venv/bin/python scripts/analysis/phase5b_environmental_drivers.py --write-manifest`
- `pytest -q`
- `git diff --check`

## Smoke-test expectation
If only one checkpoint exists, `--combine-checkpoints` should fail with a missing-combos message. This is expected operational behavior (not a scientific failure).
