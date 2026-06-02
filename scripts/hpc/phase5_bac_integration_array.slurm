#!/bin/bash
#SBATCH --job-name=phase5_bac_array
#SBATCH --account=uthpc
#SBATCH --partition=main
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=04:00:00
#SBATCH --array=0-23
#SBATCH --output=logs/phase5_bac_array_%A_%a.out
#SBATCH --error=logs/phase5_bac_array_%A_%a.err

set -euo pipefail

PROJECT_DIR="$HOME/projects/agent_microbial_communities"
cd "$PROJECT_DIR"

# Environment activation (pick one path that exists)
source ~/projects/agent_microbial_communities/.venv/bin/activate

python3 scripts/analysis/phase5_bac_integration.py \
  --single-combo \
  --combo-index "${SLURM_ARRAY_TASK_ID}"

# After array completion, run combine mode separately:
# python3 scripts/analysis/phase5_bac_integration.py --combine-checkpoints
