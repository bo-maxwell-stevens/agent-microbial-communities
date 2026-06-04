#!/bin/bash
#SBATCH --job-name=phase5b_env_array
#SBATCH --account=uthpc
#SBATCH --partition=main
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=04:00:00
#SBATCH --array=0-7
#SBATCH --output=logs/phase5b_env_array_%A_%a.out
#SBATCH --error=logs/phase5b_env_array_%A_%a.err

set -euo pipefail

PROJECT_DIR="$HOME/projects/agent_microbial_communities"
cd "$PROJECT_DIR"

source ~/projects/agent_microbial_communities/.venv/bin/activate

python3 scripts/analysis/phase5b_environmental_drivers.py \
  --single-combo \
  --combo-index "${SLURM_ARRAY_TASK_ID}" \
  --permutations 999 \
  --clr-distance-strategy direct_aitchison

# After all array tasks complete, combine explicitly:
# python3 scripts/analysis/phase5b_environmental_drivers.py --combine-checkpoints
