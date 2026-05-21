# Phase 2 Visualization and Validation

## Purpose
The goal of this phase is to add visualization and validation for the existing Phase 2 confirmatory coupling workflow. These additions provide insights into coupling metrics and ensure that summary outputs meet quality standards.

---

## Inputs
- `results/phase2_confirmatory_coupling/phase2_coupling_summary.csv`: Summary of Phase 2 coupling metrics.

---

## Scripts Added
1. **Visualization Script:**
   - `scripts/analysis/phase2_visualize_coupling.py`
   - Generates:
     - Heatmaps for `procrustes_fit` and `mantel_spearman` metrics.
     - Grouped bar plots by domain pair, transformation, and prevalence threshold.
   - Figures are saved in: `results/phase2_confirmatory_coupling/figures/`

2. **Validation Script:**
   - `scripts/analysis/phase2_validate_outputs.py`
   - Performs lightweight validation:
     - Confirms numeric and required columns.
     - Checks for missing values and general CSV integrity.
   - Output file: `results/phase2_confirmatory_coupling/validation_summary.txt`

---

### Virtual Environment Requirement

The Phase 2 visualization and validation scripts require the project's Python virtual environment because `seaborn`, `matplotlib`, and `pandas` are installed there, not necessarily in the system Python.

#### Recommended Commands:
```bash
cd /srv/hermes_projects/agent_microbial_communities
source venv/bin/activate
python3 scripts/analysis/phase2_validate_outputs.py
python3 scripts/analysis/phase2_visualize_coupling.py
```
---

## Figures Generated
- Heatmap: `heatmap_procrustes_fit.png`
- Heatmap: `heatmap_mantel_spearman.png`
- Grouped bar plot: `grouped_bar_mantel.png`
- Grouped bar plot: `grouped_bar_procrustes.png`

---

## Validation Checks
The following checks are performed:
1. File existence for `phase2_coupling_summary.csv`.
2. Specific columns—`procrustes_fit`, `mantel_spearman`, `domain_pair`, `transformation`, `threshold`—are present.
3. `procrustes_fit` and `mantel_spearman` metrics are numeric.
4. No missing values are present in key columns.
5. No malformed data structures (e.g., multiline artifacts).

---

## Biological Interpretation
### Current Findings
- EUK ↔ ITS shows the strongest and most stable coupling.
- AMF coupling exists but is weaker and preprocessing-sensitive.

### Limitations
- Current workflow does not save multidimensional embeddings for ordination visualizations, which limits alignment-based visual output.
- Causal and interaction-strength interpretations are beyond the scope of these analyses.

### Recommended Next Steps
- Save multidimensional embeddings for visual alignment plots in future runs.
- Include error bars or confidence intervals for all plotted metrics.
- Explore coupling relationships under varying ecological scenarios or time points.
