#!/bin/bash
#SBATCH --job-name=phase5c_plant_hyp
#SBATCH --account=uthpc
#SBATCH --partition=main
#SBATCH --array=0-11
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=04:00:00
#SBATCH --output=logs/phase5c_plant_hyp_%A_%a.out
#SBATCH --error=logs/phase5c_plant_hyp_%A_%a.err

set -euo pipefail

REPO_ROOT="$HOME/projects/agent_microbial_communities"
SCRIPT="scripts/analysis/phase5c_plant_diversity_hypotheses.py"
PERMUTATIONS="${PERMUTATIONS:-999}"

cd "$REPO_ROOT"
source "$REPO_ROOT/.venv/bin/activate"
mkdir -p logs results/phase5c_plant_diversity/checkpoints

python3 "$SCRIPT" \
  --single-combo \
  --combo-index "${SLURM_ARRAY_TASK_ID}" \
  --permutations "$PERMUTATIONS" \
  --clr-distance-strategy direct_aitchison \
  --include-geography-sensitivity
