# Repository Inventory (Cleanup Audit v0.6)

- Repository: `/srv/hermes_projects/agent_microbial_communities`
- Audit branch: `cleanup-audit-v0.6`
- Default branch: `main`
- Audit mode: read-only analysis + documentation updates only (no deletions, no code changes, no analysis reruns)


## 1) Current branches

```
* cleanup-audit-v0.6
  darkdivnet-microbiome-ideas
  dataset-inspection
  dataset-qc-v2
  document-phase2-venv
  fix-phase2-formatting
  main
  phase1-analysis-cleanup
  phase1-coupling-analysis
  phase1-ecological-exploration
  phase2-visualization-and-validation
  phase3-environmental-partitioning
  phase4-inference-and-interpretation
  phase5-bac-integration
  semantic-scholar-hardening
  remotes/origin/darkdivnet-microbiome-ideas
  remotes/origin/document-phase2-venv
  remotes/origin/fix-phase2-formatting
  remotes/origin/main
  remotes/origin/phase1-analysis-cleanup
  remotes/origin/phase1-coupling-analysis
  remotes/origin/phase1-ecological-exploration
  remotes/origin/phase2-visualization-and-validation
  remotes/origin/phase3-environmental-partitioning
  remotes/origin/phase4-inference-and-interpretation
  remotes/origin/phase5-bac-integration
  remotes/origin/semantic-scholar-hardening
```

## 2) Tags

```
v0.2-phase2-coupling-stable
v0.3-phase2-visualization-docs
v0.4-true-phase2-branches
v0.5-phase4-inference
```

## 3) Major project milestones (v0.3, v0.4, v0.5)

Detected milestone tags:
- v0.3: `v0.3-phase2-visualization-docs`
- v0.4: `v0.4-true-phase2-branches`
- v0.5: `v0.5-phase4-inference`

Milestone evidence (tags + commit-message grep):
```
TAGS:
v0.2-phase2-coupling-stable
v0.3-phase2-visualization-docs
v0.4-true-phase2-branches
v0.5-phase4-inference
COMMITS mentioning milestones:
```

## 4) Active analysis scripts (tracked)

```
scripts/analysis/euk_its_overlap_audit.py
scripts/analysis/phase1_coupling_analysis.py
scripts/analysis/phase1_robustness_analysis.py
scripts/analysis/phase2_validate_outputs.py
scripts/analysis/phase2_visualize_coupling.py
scripts/analysis/phase3_environmental_partitioning.py
scripts/analysis/phase4_coupling_inference.py
scripts/analysis/phase5_bac_integration.py
scripts/03_ordination.py
scripts/02_define_cohort.py
scripts/04_cross_kingdom_coupling.py
```

## 5) Active HPC scripts (tracked)

```
scripts/hpc/phase5_bac_integration_array.slurm
```

## 6) Active tests (tracked)

```
tests/test_phase1_coupling_analysis.py
```

## 7) Expected results directories

```
results
results/dataset_qc_v2
results/euk_its_overlap_audit
results/feasibility
results/literature_search_records
results/phase1_5_conservative_ordination
results/phase1_5_conservative_ordination/figures
results/phase1_coupling
results/phase1_ecological_exploration
results/phase1_robustness
results/phase2_confirmatory_coupling
results/phase2_confirmatory_coupling/__pycache__
results/phase2_confirmatory_coupling/figures
results/phase3_environmental_partitioning
results/phase4_coupling_inference
results/phase4_coupling_inference/figures
results/phase5_bac_integration
results/phase5_bac_integration/checkpoints
results/phase5_bac_integration/figures
```

Phase presence and file counts:
```
PHASE 1: PRESENT
  results/phase1_5_conservative_ordination -> 17 files
  results/phase1_5_conservative_ordination/figures -> 6 files
  results/phase1_coupling -> 9 files
  results/phase1_ecological_exploration -> 5 files
  results/phase1_robustness -> 9 files
PHASE 1.5: PRESENT
  results/phase1_5_conservative_ordination -> 17 files
  results/phase1_5_conservative_ordination/figures -> 6 files
PHASE 2: PRESENT
  results/phase2_confirmatory_coupling -> 17 files
  results/phase2_confirmatory_coupling/__pycache__ -> 2 files
  results/phase2_confirmatory_coupling/figures -> 4 files
PHASE 3: PRESENT
  results/phase3_environmental_partitioning -> 6 files
PHASE 4: PRESENT
  results/phase4_coupling_inference -> 6 files
  results/phase4_coupling_inference/figures -> 3 files
PHASE 5: PRESENT
  results/phase5_bac_integration -> 32 files
  results/phase5_bac_integration/checkpoints -> 24 files
  results/phase5_bac_integration/figures -> 3 files
```

## 8) Data dependencies (from active analysis script defaults)

```
scripts/analysis/euk_its_overlap_audit.py:26:    p.add_argument("--metadata", default="data/Final_data_with_diversity_prefixed.csv")
scripts/analysis/euk_its_overlap_audit.py:27:    p.add_argument("--euk-feature-metadata", default="data/EUK_feature_metadata.tsv")
scripts/analysis/euk_its_overlap_audit.py:28:    p.add_argument("--its-feature-metadata", default="data/ITS_feature_metadata.tsv")
scripts/analysis/euk_its_overlap_audit.py:29:    p.add_argument("--euk-table", default="data/EUK_OTU_table_final.tsv")
scripts/analysis/euk_its_overlap_audit.py:30:    p.add_argument("--its-table", default="data/ITS_OTU_table_final.tsv")
scripts/analysis/phase1_coupling_analysis.py:36:    p.add_argument("--metadata", default="data/Final_data_with_diversity_prefixed.csv")
scripts/analysis/phase1_coupling_analysis.py:37:    p.add_argument("--amf", default="data/AMF_OTU_table_final.tsv")
scripts/analysis/phase1_coupling_analysis.py:38:    p.add_argument("--bac", default="data/BAC_OTU_table_final.tsv")
scripts/analysis/phase1_coupling_analysis.py:39:    p.add_argument("--euk", default="data/EUK_OTU_table_final.tsv")
scripts/analysis/phase1_coupling_analysis.py:40:    p.add_argument("--its", default="data/ITS_OTU_table_final.tsv")
scripts/analysis/phase1_robustness_analysis.py:43:    p.add_argument("--metadata", default="data/Final_data_with_diversity_prefixed.csv")
scripts/analysis/phase1_robustness_analysis.py:44:    p.add_argument("--amf", default="data/AMF_OTU_table_final.tsv")
scripts/analysis/phase1_robustness_analysis.py:45:    p.add_argument("--bac", default="data/BAC_OTU_table_final.tsv")
scripts/analysis/phase1_robustness_analysis.py:46:    p.add_argument("--euk", default="data/EUK_OTU_table_final.tsv")
scripts/analysis/phase1_robustness_analysis.py:47:    p.add_argument("--its", default="data/ITS_OTU_table_final.tsv")
scripts/analysis/phase3_environmental_partitioning.py:31:        Loads environmental and microbial data from the `data/` directory.
scripts/analysis/phase3_environmental_partitioning.py:43:        env_path = "data/Final_data_with_diversity_prefixed.csv"
scripts/analysis/phase3_environmental_partitioning.py:44:        micro_path = "data/AMF_OTU_table_final.tsv"
```

Core files referenced repeatedly:
- `data/Final_data_with_diversity_prefixed.csv`
- `data/AMF_OTU_table_final.tsv`
- `data/BAC_OTU_table_final.tsv`
- `data/EUK_OTU_table_final.tsv`
- `data/ITS_OTU_table_final.tsv`
- `data/*_feature_metadata.tsv`

## 9) Rocket dependencies

Primary Rocket/Slurm entrypoints:
- `scripts/hpc/phase5_bac_integration_array.slurm`
- `docs/phase5_hpc_execution.md`

Key runtime expectations:
- Slurm commands: `sbatch`, `squeue`, `sacct`
- Project dir on Rocket: `~/projects/agent_microbial_communities`
- Environment activation in Slurm script: `source ~/projects/agent_microbial_communities/.venv/bin/activate`

Evidence:
```
Rocket mentions:
docs/phase5_hpc_execution.md:3:This guide runs Phase 5A BAC integration as **one combo per task** on Rocket/Slurm while keeping local serial mode available.
docs/phase5_hpc_execution.md:41:## 3) Slurm array submission (Rocket)
docs/phase5_hpc_execution.md:45:scripts/hpc/phase5_bac_integration_array.slurm
docs/phase5_hpc_execution.md:51:sbatch scripts/hpc/phase5_bac_integration_array.slurm
docs/phase5_hpc_execution.md:63:squeue -u $USER
docs/phase5_hpc_execution.md:69:sacct -j <JOBID> --format=JobIDRaw,JobName,State,ExitCode,NodeList -P -n
```

## 10) Current project structure tree (depth 2)

```
.denario_env
.denario_env/bin
.denario_env/etc
.denario_env/include
.denario_env/lib
.denario_env/lib64
.denario_env/pyvenv.cfg
.denario_env/share
.git
.git/COMMIT_EDITMSG
.git/FETCH_HEAD
.git/HEAD
.git/ORIG_HEAD
.git/branches
.git/config
.git/description
.git/hooks
.git/index
.git/info
.git/logs
.git/objects
.git/opencode
.git/refs
.gitignore
.pytest_cache
.pytest_cache/.gitignore
.pytest_cache/CACHEDIR.TAG
.pytest_cache/README.md
.pytest_cache/v
.venv
.venv/bin
.venv/etc
.venv/include
.venv/lib
.venv/lib64
.venv/pyvenv.cfg
.venv/share
AGENTS.md
README.md
configs
confirm_cohorting_patterns_from_scratch.coordinator-test-only-to-verify-intents-or-directory-desync
data
data/AMF_OTU_table_final.tsv
data/AMF_feature_metadata.tsv
data/BAC_OTU_table_final.tsv
data/BAC_feature_metadata.tsv
data/EUK_OTU_table_final.tsv
data/EUK_feature_metadata.tsv
data/Final_data_with_diversity_prefixed.csv
data/ITS_OTU_table_final.tsv
data/ITS_feature_metadata.tsv
data_denario_links
data_denario_links/AMF_OTU_table_final.txt
data_denario_links/AMF_feature_metadata.txt
data_denario_links/BAC_OTU_table_final.txt
data_denario_links/BAC_feature_metadata.txt
data_denario_links/EUK_OTU_table_final.txt
data_denario_links/EUK_feature_metadata.txt
data_denario_links/ITS_OTU_table_final.txt
data_denario_links/ITS_feature_metadata.txt
denario_runs
denario_runs/idea_generation_output
denario_runs/input_files
docs
docs/agent_goals.md
docs/analysis_feasibility_matrix.md
docs/darkdivnet_microbiome_data_science_plan.md
docs/dataset_qc_v2_report.md
docs/dataset_qc_v2_workflow.md
docs/environmental_confounding_assessment.md
docs/euk_its_overlap_audit.md
docs/kingdom_decoupling_hypothesis_assessment.md
docs/literature_synthesis_darkdivnet_microbiome.md
docs/phase1_coupling_analysis.md
docs/phase1_interpretation_cautions.md
docs/phase1_robustness_analysis.md
docs/phase2_cleanup_audit.md
docs/phase2_visualization_and_validation.md
docs/phase3_environmental_partitioning.md
docs/phase5_bac_integration_plan.md
docs/phase5_hpc_execution.md
docs/project_overview.md
docs/recommended_phase1_analysis.md
docs/research_ideas_darkdivnet_microbiome.md
docs/sample_integration_feasibility.md
docs/semantic_scholar_setup.md
docs/sequencing_depth_and_sparsity.md
idea_generation_output
idea_generation_output/LLM_calls.txt
idea_generation_output/idea.log
input_files
input_files/data_description.md
input_files/plots
notebooks
opencode.json
opencode.json.backup
prompts
pytest.ini
reports
results
results/dataset_inventory_summary.csv
results/dataset_qc_v2
results/environmental_associations.csv
results/euk_its_overlap_audit
results/feasibility
results/literature_search_records
results/literature_test_output.txt
results/mantel_results.txt
results/phase1_5_conservative_ordination
results/phase1_coupling
results/phase1_ecological_exploration
results/phase1_robustness
results/phase2_confirmatory_coupling
results/phase3_environmental_partitioning
results/phase4_coupling_inference
results/phase5_bac_integration
results/residual_mantel_results.txt
scripts
scripts/__pycache__
scripts/analysis
scripts/01_data_qc.py
scripts/feasibility
scripts/hpc
scripts/literature
scripts/run_dataset_qc_v2.sh
scripts/run_denario_exploration.py
scripts/03_ordination.py
scripts/02_define_cohort.py
scripts/run_phase1_ecological_exploration.sh
scripts/04_cross_kingdom_coupling.py
scripts/run_phase2_confirmatory_coupling_with_patch.py
scripts/test_denario_idea.py
scripts/test_denario_minimal.py
src
src/phase1_ecological_exploration
tests
tests/__pycache__
tests/fixtures
tests/outputs
tests/test_phase1_coupling_analysis.py
venv
venv/bin
venv/include
venv/lib
venv/lib64
venv/pyvenv.cfg
venv/share
```

## 11) .gitignore audit

Current .gitignore:
```
# Local/private data
data/
raw_data/
private/
secrets/
.env
*.key
*.pem

# Outputs
results/
outputs/
reports/intermediate/

# Python/Jupyter
.venv/
__pycache__/
.ipynb_checkpoints/
*.pyc

# OS/editor
.DS_Store
.vscode/

.denario_env/
!results/phase2_confirmatory_coupling/phase2_coupling_summary.csv
```

Evaluation of requested paths:
```
path	ignored_now
venv/	no
scripts/analysis/env/	no
.pytest_cache/	yes
denario_runs/	no
data_denario_links/	no
idea_generation_output/	no
input_files/	no
opencode.json	no
opencode.json.backup	no
```

Recommended additions (not yet applied):
- `venv/`
- `scripts/analysis/env/`
- `denario_runs/`
- `data_denario_links/`
- `idea_generation_output/`
- `input_files/`
- `opencode.json.backup`
- optional policy choice: `opencode.json`

(`.pytest_cache/` is already ignored.)

## 12) Untracked content classification (A/B/C/D)

Legend:
- A = Safe delete
- B = Archive candidate
- C = Keep
- D = Unknown

```
path\tsize_bytes\tcategory\treferenced_anywhere(exact-path)\trationale
B	data_denario_links	620	Archive candidate	no (0)	Generated/experimental Denario artifacts
B	denario_runs	12368	Archive candidate	no (0)	Generated/experimental Denario artifacts
B	idea_generation_output	512	Archive candidate	no (0)	Generated/experimental Denario artifacts
B	input_files	1236	Archive candidate	no (0)	Generated/experimental Denario artifacts
B	opencode.json	587	Archive candidate	no (0)	Local tool config; likely user-local, not project source
A	opencode.json.backup	577	Safe delete	no (0)	Backup/temp file
C	scripts/analysis/env	338578527	Keep	no (0)	Local environment directory (rebuildable, but likely in use)
D	scripts/analysis/external_validation_summary_writer.py	744	Unknown	no (0)	Analysis script exists but not wired into current tracked pipeline
D	scripts/analysis/phase2_confirmatory_coupling_analysis.py	2296	Unknown	no (0)	Analysis script exists but not wired into current tracked pipeline
B	scripts/run_denario_exploration.py	1714	Archive candidate	no (0)	Denario experiment scripts not in current pipeline
A	scripts/run_phase2_confirmatory_coupling_with_patch.py	1	Safe delete	no (0)	Placeholder/empty patch helper
B	scripts/test_denario_idea.py	5218	Archive candidate	no (0)	Denario experiment scripts not in current pipeline
B	scripts/test_denario_minimal.py	1126	Archive candidate	no (0)	Denario experiment scripts not in current pipeline
D	tests/fixtures	366	Unknown	no (0)	Test fixture directory untracked; unclear intended test integration
C	venv	440292831	Keep	yes (5)	Local environment directory (rebuildable, but likely in use)
```

## 13) Top-level directory purpose, size, recommendation

```
path\tsize_bytes\tpurpose\trecommendation
.denario_env	2301244988	python environments / code	KEEP
.venv	1801841465	python environments / code	KEEP
venv	440292831	python environments / code	KEEP
scripts	339010011	python environments / code	KEEP
data	153214953	source datasets	KEEP
results	12424177	analysis outputs	KEEP
.git	2245341	git metadata	KEEP
src	108421	core project assets	KEEP
docs	71489	core project assets	KEEP
tests	15937	core project assets	KEEP
denario_runs	12368	denario experiment/generated artifacts	ARCHIVE or DELETE
.pytest_cache	1626	pytest cache	DELETE
input_files	1236	denario experiment/generated artifacts	ARCHIVE or DELETE
data_denario_links	620	denario experiment/generated artifacts	ARCHIVE or DELETE
idea_generation_output	512	denario experiment/generated artifacts	ARCHIVE or DELETE
configs	0	empty placeholder	REVIEW then DELETE if unused
confirm_cohorting_patterns_from_scratch.coordinator-test-only-to-verify-intents-or-directory-desync	0	empty placeholder	REVIEW then DELETE if unused
notebooks	0	empty placeholder	REVIEW then DELETE if unused
prompts	0	empty placeholder	REVIEW then DELETE if unused
reports	0	empty placeholder	REVIEW then DELETE if unused
```

## 14) Environment audit

Environment sizes:
```
.venv	1801841465
.denario_env	2301244988
venv	440292831
scripts/analysis/env	338578527
```

Current usage interpretation:
- Local Phase 2: docs explicitly use `source venv/bin/activate` (`docs/phase2_visualization_and_validation.md`).
- Local Phase 4: no explicit env activation in phase4 script; runs in whichever Python env is active.
- Local Phase 5 (local docs): `docs/phase5_hpc_execution.md` currently shows `source venv/bin/activate` for local invocation.
- Rocket HPC: `scripts/hpc/phase5_bac_integration_array.slurm` explicitly activates `.venv` at `~/projects/agent_microbial_communities/.venv/bin/activate`.

Recommended canonical strategy:
1. Standardize on `.venv` for all local + HPC workflows.
2. Deprecate `venv/` and `scripts/analysis/env/` after validation.
3. Keep `.denario_env/` only if Denario work remains active; otherwise archive/remove.

## 15) Empty directory audit

```
path\tsafe_to_remove\tnotes
.denario_env/include/python3.12	no	environment internals (remove only with env cleanup)
.git/branches	no	git internals
.git/objects/info	no	git internals
.git/objects/pack	no	git internals
.venv/include/python3.12	no	environment internals (remove only with env cleanup)
configs	yes	empty
confirm_cohorting_patterns_from_scratch.coordinator-test-only-to-verify-intents-or-directory-desync	yes	empty
denario_runs/input_files/plots	yes	empty
input_files/plots	yes	empty
notebooks	yes	empty
prompts	yes	empty
reports	yes	empty
scripts/analysis/env/include/python3.12	no	environment internals (remove only with env cleanup)
venv/include/python3.12	no	environment internals (remove only with env cleanup)
```

## 16) Git safety audit

Current branch: `cleanup-audit-v0.6`

Tracked-file status only:
```

```

Branches ahead/behind `main`:
```
branch\tahead\tbehind
cleanup-audit-v0.6	1	0
darkdivnet-microbiome-ideas	0	29
dataset-inspection	1	38
dataset-qc-v2	0	37
document-phase2-venv	0	8
fix-phase2-formatting	0	9
main	0	0
phase1-analysis-cleanup	0	5
phase1-coupling-analysis	0	11
phase1-ecological-exploration	0	19
phase2-visualization-and-validation	0	10
phase3-environmental-partitioning	0	1
phase4-inference-and-interpretation	0	0
phase5-bac-integration	1	0
semantic-scholar-hardening	0	34
```

Branches already merged into `main`:
```
  darkdivnet-microbiome-ideas
  dataset-qc-v2
  document-phase2-venv
  fix-phase2-formatting
  main
  phase1-analysis-cleanup
  phase1-coupling-analysis
  phase1-ecological-exploration
  phase2-visualization-and-validation
  phase3-environmental-partitioning
  phase4-inference-and-interpretation
  semantic-scholar-hardening
```

Branches safe to delete **after confirming no longer needed** (already merged into `main`):
```
  darkdivnet-microbiome-ideas
  dataset-qc-v2
  document-phase2-venv
  fix-phase2-formatting
  phase1-analysis-cleanup
  phase1-coupling-analysis
  phase1-ecological-exploration
  phase2-visualization-and-validation
  phase3-environmental-partitioning
  phase4-inference-and-interpretation
  semantic-scholar-hardening
```
