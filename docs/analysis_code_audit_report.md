# Analysis Code Audit Report

- Generated: 2026-06-03T15:43:45.192419Z
- Mode: Read-first static audit (no code edits in audited scripts).
- Scope: Phase 2 coupling, Phase 4 inference, Phase 5A/5B/5C/5D, and manuscript-mapping script scan.

## Revised verification plan used for execution

1. Static script audit and risk inventory.
2. Manuscript numeric-claim extraction and source verification against committed outputs.
3. Pair-scope transition verification across phases and manuscript language.
4. Targeted scientific-risk tests (alignment/transforms/distances/permutations/model mapping/regression checks).
5. Compile + pytest + diff hygiene checks; report unresolved risks honestly.

## Manuscript-preparation script scan

No Python scripts under `scripts/` were found that explicitly read/write `manuscript/`, `manuscript_v*`, or `results/manuscript_preparation` paths. Manuscript mapping appears file/artifact-driven rather than script-rendered.

## Per-script audit

### `scripts/run_phase2_confirmatory_coupling.py`

- Purpose: Run Phase 2 Confirmatory Coupling Analysis

Branch-specific confirmatory coupling:
- presence/absence: prevalence filter -> binary -> Jaccard -> deterministic PCoA
- CLR: prevalence filter -> relative abundance -> CLR -> Euclidean -> deterministic PCA

Mantel Spearman is computed directly on branch-specific full distance matrices
(not reduced ordination embeddings).
- Inputs (detected path literals): `results/phase2_confirmatory_coupling`
- Outputs (detected path literals): `results/phase2_confirmatory_coupling`
- Key transformations / statistical methods: CLR transform, Euclidean distance, Mantel, Presence/absence transform, Procrustes
- Random/permutation/seed handling (sample lines):
  - None detected by static scan.
- Possible correctness risks:
  - fillna() usage detected; confirm imputation choices are scientifically justified and documented.
  - Transformations detected; verify non-finite guards are applied after CLR/log transforms.
- Alignment with manuscript methods: **high** (keyword-overlap heuristic; confirmed with downstream numeric and regression checks).
- Script size: 208 lines.

### `scripts/analysis/phase4_coupling_inference.py`

- Purpose: Phase 4 Coupling Inference

Adds inferential support to deterministic Phase 2 coupling analysis:
- Mantel permutation p-values (two-sided, label permutation)
- 95% bootstrap confidence intervals for Mantel Spearman
- Procrustes bootstrap stability with 95% confidence intervals

All stochastic procedures are seeded for deterministic reproducibility.
- Inputs (detected path literals): `results/phase2_confirmatory_coupling`, `results/phase4_coupling_inference`
- Outputs (detected path literals): `results/phase2_confirmatory_coupling`, `results/phase4_coupling_inference`
- Key transformations / statistical methods: CLR transform, Euclidean distance, Mantel, Presence/absence transform, Procrustes
- Random/permutation/seed handling (sample lines):
  - `- Mantel permutation p-values (two-sided, label permutation)`
  - `All stochastic procedures are seeded for deterministic reproducibility.`
  - `RANDOM_SEED = 20260601`
  - `N_PERMUTATIONS = 999`
  - `rng: np.random.Generator,`
  - `idx = rng.integers(0, n, size=n)`
  - `def mantel_permutation_pvalue(`
  - `rng: np.random.Generator,`
  - `n_permutations: int,`
  - `for i in range(n_permutations):`
  - `perm = rng.permutation(n)`
  - `if (i + 1) % 100 == 0 or (i + 1) == n_permutations:`
- Possible correctness risks:
  - Merge operations present; verify join cardinality assumptions and potential row duplication/drop during joins.
  - fillna() usage detected; confirm imputation choices are scientifically justified and documented.
  - Transformations detected; verify non-finite guards are applied after CLR/log transforms.
- Alignment with manuscript methods: **high** (keyword-overlap heuristic; confirmed with downstream numeric and regression checks).
- Script size: 505 lines.

### `scripts/analysis/phase5_bac_integration.py`

- Purpose: Phase 5A BAC Integration

Extends deterministic Phase 2 + Phase 4 coupling framework to include BAC as a fourth domain:
- Mantel permutation p-values (two-sided, label permutation)
- 95% bootstrap confidence intervals for Mantel Spearman
- Procrustes bootstrap stability with 95% confidence intervals

All stochastic procedures are seeded for deterministic reproducibility.
- Inputs (detected path literals): `results/phase2_confirmatory_coupling`, `results/phase5_bac_integration`
- Outputs (detected path literals): `results/phase2_confirmatory_coupling`, `results/phase5_bac_integration`
- Key transformations / statistical methods: CLR transform, Euclidean distance, Mantel, Presence/absence transform, Procrustes
- Random/permutation/seed handling (sample lines):
  - `- Mantel permutation p-values (two-sided, label permutation)`
  - `All stochastic procedures are seeded for deterministic reproducibility.`
  - `RANDOM_SEED = 20260601`
  - `N_PERMUTATIONS = 999`
  - `rng: np.random.Generator,`
  - `idx = rng.integers(0, n, size=n)`
  - `def mantel_permutation_pvalue(`
  - `rng: np.random.Generator,`
  - `n_permutations: int,`
  - `for i in range(n_permutations):`
  - `perm = rng.permutation(n)`
  - `if (i + 1) % 100 == 0 or (i + 1) == n_permutations:`
- Possible correctness risks:
  - Merge operations present; verify join cardinality assumptions and potential row duplication/drop during joins.
  - fillna() usage detected; confirm imputation choices are scientifically justified and documented.
  - Transformations detected; verify non-finite guards are applied after CLR/log transforms.
- Alignment with manuscript methods: **high** (keyword-overlap heuristic; confirmed with downstream numeric and regression checks).
- Script size: 671 lines.

### `scripts/analysis/phase5b_environmental_drivers.py`

- Purpose: Phase 5B Environmental Drivers

Resumable HPC-oriented dbRDA-style workflow for approved Phase 5B predictors.

Modes:
- --write-manifest: write 8-row pair×branch combo manifest.
- --single-combo --combo-index N: run exactly one combo and write one checkpoint CSV.
- --combine-checkpoints: combine all checkpoint CSVs into final outputs.
- (no mode flags): run full serial workflow locally.

Policy constraints:
- Primary predictors: pH_KCl, N_pct, bio12now.100, alpha, compl
- Sensitivity extension only: + lat, lon
- Exclusions enforced: PC1..PC4, beta.perc, compl.perc, pool, dark, gamma
- N_pct and C_pct cannot be used together.
- Inputs (detected path literals): `results/phase2_confirmatory_coupling/sample_cohort_used.csv`, `results/phase5b_environmental_drivers`
- Outputs (detected path literals): `results/phase2_confirmatory_coupling/sample_cohort_used.csv`, `results/phase5b_environmental_drivers`
- Key transformations / statistical methods: Adjusted R², CLR transform, Euclidean distance, Presence/absence transform, dbRDA
- Random/permutation/seed handling (sample lines):
  - `DEFAULT_PERMUTATIONS = 999`
  - `BASE_RANDOM_SEED = 20260602`
  - `def permutation_pvalue(Y: np.ndarray, X: np.ndarray, n_perm: int, seed: int) -> tuple[float, float]:`
  - `rng = np.random.default_rng(seed)`
  - `if n_perm <= 0:`
  - `for _ in range(n_perm):`
  - `idx = rng.permutation(n)`
  - `p = (count + 1) / (n_perm + 1)`
  - `def combo_seed(combo_index: int) -> int:`
  - `return int(BASE_RANDOM_SEED + combo_index * 10007)`
  - `permutations: int,`
  - `seed: int,`
- Possible correctness risks:
  - Sample intersection logic exists; ensure ordering is explicitly synchronized before pairwise distances/statistics.
  - dropna() usage detected; verify no unintended sample loss biases pairwise comparisons.
  - fillna() usage detected; confirm imputation choices are scientifically justified and documented.
  - Metadata + community matrix handling co-located; verify only intended predictor columns enter models.
- Alignment with manuscript methods: **high** (keyword-overlap heuristic; confirmed with downstream numeric and regression checks).
- Script size: 690 lines.

### `scripts/analysis/phase5c_plant_diversity_hypotheses.py`

- Purpose: Phase 5C Plant Diversity Hypotheses

Hypothesis-driven dbRDA-style workflow evaluating DarkDivNet biodiversity metrics
against cross-domain microbial coupling, beyond abiotic baseline drivers.

Primary hypothesis model set (A-G):
A: abiotic_base
B: abiotic_base + alpha
C: abiotic_base + dark
D: abiotic_base + pool
E: abiotic_base + compl
F: abiotic_base + alpha + dark
G: abiotic_base + pool + compl

Geography remains sensitivity-only (+lat,+lon); all primary inference should use
model_scope=primary.

Modes:
- --write-manifest
- --single-combo --combo-index N
- --combine-checkpoints
- (no mode flags): full serial run
- Inputs (detected path literals): `results/phase2_confirmatory_coupling/sample_cohort_used.csv`, `results/phase5c_plant_diversity`
- Outputs (detected path literals): `results/phase2_confirmatory_coupling/sample_cohort_used.csv`, `results/phase5c_plant_diversity`
- Key transformations / statistical methods: Adjusted R², CLR transform, Euclidean distance, Presence/absence transform, dbRDA
- Random/permutation/seed handling (sample lines):
  - `DEFAULT_PERMUTATIONS = 999`
  - `BASE_RANDOM_SEED = 20260603`
  - `def permutation_pvalue(Y: np.ndarray, X: np.ndarray, n_perm: int, seed: int) -> tuple[float, float]:`
  - `rng = np.random.default_rng(seed)`
  - `if n_perm <= 0:`
  - `for _ in range(n_perm):`
  - `idx = rng.permutation(n)`
  - `p = (count + 1) / (n_perm + 1)`
  - `def combo_seed(combo_index: int) -> int:`
  - `return int(BASE_RANDOM_SEED + combo_index * 20011)`
  - `permutations: int,`
  - `seed: int,`
- Possible correctness risks:
  - Merge operations present; verify join cardinality assumptions and potential row duplication/drop during joins.
  - Sample intersection logic exists; ensure ordering is explicitly synchronized before pairwise distances/statistics.
  - dropna() usage detected; verify no unintended sample loss biases pairwise comparisons.
  - fillna() usage detected; confirm imputation choices are scientifically justified and documented.
  - Metadata + community matrix handling co-located; verify only intended predictor columns enter models.
- Alignment with manuscript methods: **high** (keyword-overlap heuristic; confirmed with downstream numeric and regression checks).
- Script size: 975 lines.

### `scripts/analysis/phase5d_synthesis.py`

- Purpose: Phase 5D synthesis: integrate completed Phase 2/4/5/5B/5C outputs.

This script is intentionally read-from-results-only and does not rerun prior analyses.
- Inputs (detected path literals): `results/phase5_bac_integration/phase5_bac_coupling_summary.csv`, `results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv`, `results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv`, `results/phase5c_plant_diversity/phase5c_hypothesis_summary.csv`, `results/phase5c_plant_diversity/phase5c_model_comparison.csv`
- Outputs (detected path literals): `results/phase5_bac_integration/phase5_bac_coupling_summary.csv`, `results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv`, `results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv`, `results/phase5c_plant_diversity/phase5c_hypothesis_summary.csv`, `results/phase5c_plant_diversity/phase5c_model_comparison.csv`
- Key transformations / statistical methods: Adjusted R², Mantel, Procrustes, dbRDA
- Random/permutation/seed handling (sample lines):
  - None detected by static scan.
- Possible correctness risks:
  - Merge operations present; verify join cardinality assumptions and potential row duplication/drop during joins.
  - fillna() usage detected; confirm imputation choices are scientifically justified and documented.
- Alignment with manuscript methods: **moderate** (keyword-overlap heuristic; confirmed with downstream numeric and regression checks).
- Script size: 421 lines.



## Addendum (2026-06-04T09:54:44.111854+00:00)

- Strict 999 remediation verification rerun completed.
- Canonical Phase statuses: Phase4=yes, Phase5A=yes, Phase5B=yes, Phase5C=yes (all expected permutation fields = 999).
- Validation gates rerun: py_compile pass; targeted pytest pass (16); full pytest pass (21); git diff --check pass.
- Pre-999 backups preserved in `results/archive_pre_999_sync/20260604T090054Z/` and `results/archive_pre_999_sync/20260604T094703Z/`.
