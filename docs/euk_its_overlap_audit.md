# EUK–ITS Overlap Audit (Contamination/Redundancy-Aware Interpretation)

## Purpose
Audit whether strong EUK–ITS reduced-space coupling is inflated by taxonomic overlap (fungi are a subset of eukaryotes), and determine how EUK–ITS should be interpreted in phase-1 reporting.

This is an interpretation/sensitivity audit, not a new manuscript claim.

## Inputs
- `data/EUK_feature_metadata.tsv`
- `data/ITS_feature_metadata.tsv`
- `data/EUK_OTU_table_final.tsv`
- `data/ITS_OTU_table_final.tsv`
- `data/Final_data_with_diversity_prefixed.csv`

Script:
- `scripts/analysis/euk_its_overlap_audit.py`

Outputs:
- `results/euk_its_overlap_audit/euk_taxonomic_summary.csv`
- `results/euk_its_overlap_audit/euk_fungal_fraction_by_sample.csv`
- `results/euk_its_overlap_audit/euk_its_subset_coupling.csv`
- `results/euk_its_overlap_audit/run_metadata.json`
- `results/euk_its_overlap_audit/warnings.log`

## 1) EUK/ITS metadata structure
- EUK metadata columns: `OTU`, `taxonomy`
- ITS metadata includes `taxonomy` plus lifestyle/trait annotations.

Interpretation relevance:
- EUK metadata are sufficient for fungal partitioning because features have stable IDs (`OTU*`) and taxonomy strings with kingdom-level labels.

## 2) Does EUK contain fungal assignments?
Yes.

From `euk_taxonomic_summary.csv` (overlap n=94):
- **Fungi:** 30,756 / 58,205 features (**52.84%**) and 1,551,370 reads (**63.70%**) 
- Metazoa: 7,592 features (13.04%), 200,243 reads (8.22%)
- Viridiplantae: 5,119 features (8.79%), 394,744 reads (16.21%)
- Other protist/euk: 12,158 features (20.89%), 250,969 reads (10.30%)
- Unknown/unclassified: 2,580 features (4.43%), 38,226 reads (1.57%)

Conclusion: EUK includes substantial fungal signal at both feature and read levels.

## 3) Sample-level fungal fraction in EUK
From `euk_fungal_fraction_by_sample.csv`:
- Mean fungal fraction: **0.6515**
- Median fungal fraction: **0.6737**
- IQR: ~0.522 to ~0.809
- Range: 0.126 to 1.000

So many samples are fungal-dominated in EUK reads, but with substantial variation.

## 4) EUK subset vs ITS coupling
From `euk_its_subset_coupling.csv` (CLR+PCA reduced-space):

### EUK_all vs ITS
- Procrustes: 0.254
- Mantel-like Spearman: 0.270
- RV: 0.255
- Embedding-distance Pearson: 0.330

### EUK_fungal vs ITS
- Procrustes: 0.178
- Mantel-like Spearman: 0.196
- RV: 0.173
- Embedding-distance Pearson: 0.262

### EUK_nonfungal vs ITS
- Procrustes: 0.294
- Mantel-like Spearman: 0.291
- RV: 0.299
- Embedding-distance Pearson: 0.349

Audit interpretation:
- EUK–ITS coupling is **not solely carried by fungal-assigned EUK features** in this reduced-space analysis.
- EUK_nonfungal vs ITS remained comparably strong (and here stronger than EUK_fungal vs ITS).
- This argues against a purely trivial “same-taxon channel” explanation.

However, taxonomic non-independence still exists conceptually (EUK includes fungi by design), so headline interpretation must remain conservative.

## 5) Positive control vs main cross-kingdom result
Recommended framing:
- Treat EUK–ITS primarily as a **pipeline-positive-control / sensitivity result** due to inherent taxonomic overlap risk.
- Do **not** use EUK–ITS as primary headline evidence of independent cross-kingdom coupling.
- Secondary note: persistence in EUK_nonfungal subset suggests coupling is not entirely fungal bleed-through, but this remains exploratory.

## 6) Which pairings are more independent for headline emphasis
Prefer emphasizing pairings with greater biological/taxonomic independence:
- `AMF–BAC`
- `BAC–ITS`
- `BAC–EUK_nonfungal` (where subset definition is feasible)
- `AMF–EUK_nonfungal` (where feasible)
- `AMF–ITS` with explicit caveats

De-emphasize as headline novelty:
- `EUK–ITS` (retain as sensitivity/positive-control section)

## 7) Limitations and cautions
- EUK taxonomy labels are string-derived and may include annotation uncertainty.
- Reduced-space coupling does not establish direct interaction networks or causal ecological mechanisms.
- Fungal/nonfungal partition quality depends on taxonomy completeness and correctness.
- This audit does not justify causal claims.

## Bottom line
- EUK contains substantial fungal signal.
- Fungal partitioning is feasible with current metadata.
- EUK–ITS remains coupled after removing fungal-assigned EUK features, so the pattern is not purely fungal-overlap artifact.
- Despite that, EUK–ITS should be treated mainly as **positive-control/sensitivity evidence**, not as the strongest independent headline cross-kingdom claim.