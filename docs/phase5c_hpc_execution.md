# Phase 5C HPC execution (Rocket)

## Scope
Phase 5C tests hypothesis-based DarkDivNet biodiversity model sets against cross-domain microbial coupling, beyond the abiotic base:

- Abiotic base: `pH_KCl + N_pct + bio12now.100`
- Hypotheses A..G (primary):
  - A: abiotic base
  - B: + alpha
  - C: + dark
  - D: + pool
  - E: + compl
  - F: + alpha + dark
  - G: + pool + compl
- Geography is sensitivity-only (`latitude + longitude`) and is run via `--include-geography-sensitivity`.

Combos: 4 microbial pairs × 2 branches = 8 SLURM array tasks.

## 1) Write manifest
```bash
cd ~/projects/agent_microbial_communities
source .venv/bin/activate
python3 scripts/analysis/phase5c_plant_diversity_hypotheses.py --write-manifest
```

Expected manifest: `results/phase5c_plant_diversity/phase5c_combo_manifest.csv` with 8 rows.

## 2) Submit array (DO NOT run until approved)
```bash
cd ~/projects/agent_microbial_communities
mkdir -p logs
sbatch scripts/hpc/phase5c_plant_diversity_hypotheses_array.slurm
```

Optional permutation override:
```bash
PERMUTATIONS=499 sbatch scripts/hpc/phase5c_plant_diversity_hypotheses_array.slurm
```

## 3) Monitor
```bash
squeue -u stevens
sacct -j <jobid> --format=JobID,State,Elapsed,MaxRSS
ls -lh logs/phase5c_plant_hyp_<jobid>_*.{out,err}
```

## 4) Combine checkpoints (after all 0..7 complete)
```bash
cd ~/projects/agent_microbial_communities
source .venv/bin/activate
python3 scripts/analysis/phase5c_plant_diversity_hypotheses.py \
  --combine-checkpoints \
  --permutations 499 \
  --include-geography-sensitivity
```

## 5) Required outputs
Under `results/phase5c_plant_diversity/`:

- `phase5c_model_comparison.csv`
- `phase5c_predictor_effects.csv`
- `phase5c_pair_rankings.csv`
- `phase5c_hypothesis_summary.csv`
- `phase5c_model_delta_adj_r2.png`
- `phase5c_hypothesis_rankings.png`
- `phase5c_pair_comparisons.png`

Checkpoint folder:
- `checkpoints/combo_0.csv` … `combo_7.csv`
