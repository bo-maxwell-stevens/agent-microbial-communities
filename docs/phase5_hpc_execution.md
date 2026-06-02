# Phase 5A HPC Execution (Job Array)

This guide runs Phase 5A BAC integration as **one combo per task** on Rocket/Slurm while keeping local serial mode available.

## Preconditions
- Repo root: `/srv/hermes_projects/agent_microbial_communities`
- Branch: `phase5-bac-integration`
- Script: `scripts/analysis/phase5_bac_integration.py`
- Expected combos: **24** (`6 pairs × 2 branches × 2 thresholds`)

## 1) Local one-combo smoke test
From repo root:

```bash
source venv/bin/activate
python3 scripts/analysis/phase5_bac_integration.py --write-manifest
python3 scripts/analysis/phase5_bac_integration.py --single-combo --combo-index 0
```

Expected checkpoint file:

```bash
results/phase5_bac_integration/checkpoints/combo_0.csv
```

## 2) Manifest creation
The manifest is written to:

```bash
results/phase5_bac_integration/phase5_combo_manifest.csv
```

It must have **24 rows** and columns:
- `combo_index`
- `pair`
- `domain_1`
- `domain_2`
- `branch`
- `threshold`

## 3) Slurm array submission (Rocket)
Template file:

```bash
scripts/hpc/phase5_bac_integration_array.slurm
```

Set account/partition placeholders in the file, then submit:

```bash
sbatch scripts/hpc/phase5_bac_integration_array.slurm
```

The array runs task IDs `0-23`, one combo per task:

```bash
python3 scripts/analysis/phase5_bac_integration.py --single-combo --combo-index ${SLURM_ARRAY_TASK_ID}
```

## 4) Monitoring command

```bash
squeue -u $USER
```

Optional detailed monitoring for one array job:

```bash
sacct -j <JOBID> --format=JobIDRaw,JobName,State,ExitCode,NodeList -P -n
```

## 5) Combine command (run after array completion)

```bash
python3 scripts/analysis/phase5_bac_integration.py --combine-checkpoints
```

Combine mode writes:
- `results/phase5_bac_integration/phase5_bac_coupling_summary.csv`
- `results/phase5_bac_integration/phase5_bac_mantel_inference.csv`
- `results/phase5_bac_integration/phase5_bac_procrustes_bootstrap.csv`
- `results/phase5_bac_integration/phase5_bac_rank_summary.csv`
- `results/phase5_bac_integration/figures/mantel_effect_sizes.png`
- `results/phase5_bac_integration/figures/procrustes_effect_sizes.png`
- `results/phase5_bac_integration/figures/domain_pair_rankings.png`

## 6) Validation gates
1. `python3 -m py_compile scripts/analysis/phase5_bac_integration.py`
2. Manifest row count is 24.
3. One-combo smoke test writes exactly one checkpoint (`combo_<index>.csv`).
4. `--combine-checkpoints` succeeds only when all 24 combo checkpoints are present.
5. `pytest -q` passes.
6. `git diff --check` has no whitespace errors.

## Notes on resumability
- Array tasks are independent by `combo_index`.
- Re-running a completed combo without deleting its checkpoint intentionally fails to avoid accidental overwrite.
- Local full serial run is still available (run script with no mode flags).
