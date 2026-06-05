# Phase 5B HPC Execution (Rocket Job Array)

Repository: `/srv/hermes_projects/agent_microbial_communities`  
Branch: `phase5b-environmental-drivers`

## 1) Required inputs
- `data/AMF_OTU_table_final.tsv`
- `data/BAC_OTU_table_final.tsv`
- `data/EUK_OTU_table_final.tsv`
- `data/ITS_OTU_table_final.tsv`
- `data/Final_data_with_diversity_prefixed.csv`
- `results/phase2_confirmatory_coupling/sample_cohort_used.csv`
- `scripts/analysis/phase5b_environmental_drivers.py`

## 2) Environment setup (Rocket)
```bash
cd ~/projects/agent_microbial_communities
source .venv/bin/activate
python -c "import numpy,pandas,scipy,sklearn,matplotlib; print("ENVIRONMENT_OK")"
```

## 3) Manifest command
```bash
python3 scripts/analysis/phase5b_environmental_drivers.py --write-manifest
```
Manifest path:
- `results/phase5b_environmental_drivers/phase5b_combo_manifest.csv`

Expected rows: **12** (`6 pairs × 2 branches`).

## 4) Single-combo smoke test
```bash
python3 scripts/analysis/phase5b_environmental_drivers.py --single-combo --combo-index 0 --permutations 49
```
Expected checkpoint:
- `results/phase5b_environmental_drivers/checkpoints/combo_0.csv`

## 5) Full array submission (when approved later)
Slurm template:
- `scripts/hpc/phase5b_environmental_drivers_array.slurm`

Submission command:
```bash
sbatch scripts/hpc/phase5b_environmental_drivers_array.slurm
```

## 6) Monitoring
```bash
squeue -u $USER
```

```bash
sacct -j <JOBID> --format=JobIDRaw,JobName,State,ExitCode,Elapsed,NodeList -P -n
```

## 7) Combine command (after all 8 checkpoints exist)
```bash
python3 scripts/analysis/phase5b_environmental_drivers.py --combine-checkpoints
```

Combined outputs:
- `results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv`
- `results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv`
- `results/phase5b_environmental_drivers/phase5b_pair_rankings.csv`
- `results/phase5b_environmental_drivers/phase5b_manifest.csv`
- `results/phase5b_environmental_drivers/phase5b_run_metadata.json`
- figures under `results/phase5b_environmental_drivers/figures/`

## 8) Validation checklist
- [ ] `.venv/bin/python -m py_compile scripts/analysis/phase5b_environmental_drivers.py`
- [ ] `python3 scripts/analysis/phase5b_environmental_drivers.py --write-manifest` creates 12-row manifest
- [ ] one-combo smoke test writes `checkpoints/combo_0.csv`
- [ ] `pytest -q` passes
- [ ] `git diff --check` is clean
- [ ] combine mode succeeds only when all 8 checkpoints are present

## Operational note
If combine fails after smoke test because only 1/8 checkpoints exists, this is expected orchestration behavior and not a scientific failure.
