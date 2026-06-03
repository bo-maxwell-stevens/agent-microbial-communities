# Methods Draft

## Scope lock and provenance
This Methods package summarizes only completed analyses and existing outputs anchored on branch phase5d-synthesis. No analysis scripts were rerun and no scientific result files were modified during manuscript packaging.

## Input data and cohort alignment
Input OTU tables for AMF, EUK, ITS, and BAC were read from the project data directory and aligned to a fixed cohort manifest. The analysis cohort included 84 samples.

## Pairing and branch design across phases
Coupling analyses used explicit pairwise designs with two processing branches (presence/absence and CLR) and prevalence thresholds 0.05 and 0.10. Phase Two covered EUK↔ITS, AMF↔ITS, and AMF↔EUK. BAC integration expanded the design to BAC-inclusive cross-domain combinations while preserving the same threshold and branch structure.

## Feature preprocessing and transformations
CLR preprocessing used pseudocount 1e-6 and component cap 10. Presence/absence processing used binary conversion with Jaccard distances. CLR processing used Euclidean distances after centered log-ratio transformation.

## Coupling inference and uncertainty estimation
Phase Four and BAC-integration inference used random seed 20260601, permutation count 999, and bootstrap count 120. Confidence intervals followed percentile bounds 2.5 and 97.5 where bootstrap summaries were reported.

## Environmental driver model specification
Environmental driver analysis used default threshold 0.05, permutation count 999, and base seed 20260602. Primary predictor policy used pH_KCl, N_pct, bio12now.100, alpha, and compl; geography sensitivity added lat and lon. Policy checks prohibited simultaneous N_pct and C_pct inclusion.

## Plant-diversity hypothesis specification
Plant-diversity modeling used threshold 0.05, permutations 999, base seed 20260603, pseudocount 1e-6, and component cap 10. Seven primary hypothesis models (A through G) tested additive plant-diversity effects over an abiotic baseline.

## Cross-phase synthesis decision rules
Synthesis labels used explicit thresholds: coupling strength ≥ 0.50, environmental adjusted R² ≥ 0.20, plant-diversity delta adjusted R² ≥ 0.01, and a low-plant rule at plant delta < 0.005 for abiotic-dominant interpretation.

## Manuscript-source inspection coverage
Manuscript package context was anchored by inspection of docs/manuscript_blueprint.md, docs/results_storyboard.md, docs/results_draft.md, and docs/introduction_package.md, plus all required analysis scripts from Phase Two, Phase Four, and Phase Five subphases.

## Software environment and reproducibility controls
Packaging and validation used project virtual environment execution via .venv/bin/python. Runtime versions in this pass were Python 3.12.3, numpy 2.4.5, pandas 3.0.3, scipy 1.17.1, and scikit-learn 1.8.0. Deterministic controls included fixed seeds 20260601, 20260602, and 20260603, plus deterministic solver configuration and fixed branch/threshold manifests.
