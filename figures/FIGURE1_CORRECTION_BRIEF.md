# Figure 1 correction brief (grounded)

## What is wrong in the current draft figure
- The existing Figure 1 package content is workflow-oriented but does not encode verified cohort/domain/overlap counts directly in panel labels.
- Country and biome totals are not currently grounded in repository metadata; any draft values for those should be removed unless externally verified metadata is provided.
- Map panel should be constrained to coordinates that exist in repository data.

## Exact corrected numbers to use
- Canonical sample inventory: **143**
- Sites with available site_id/region coordinates metadata: **99**
- Samples with metadata available (META): **99**
- Four-domain overlap (BAC+ITS+EUK+AMF): **112**
- Final analytical cohort (all four domains + metadata): **84**
- Domain counts: BAC **140**, ITS **139**, EUK **135**, AMF **120**
- Pairwise overlaps: BAC↔ITS **137**, BAC↔EUK **135**, BAC↔AMF **117**, ITS↔EUK **132**, ITS↔AMF **117**, EUK↔AMF **114**

## Can map points be drawn from real coordinates?
- **Yes.** Latitude/longitude are available for the metadata-backed subset (99 samples/sites), including the full final cohort.

## Biome colors availability
- A generic `region` code is available.
- Explicit biome-class labels were not found in inspected metadata/result tables.
- Recommendation: **omit biome-color legend** unless a verified biome mapping table is added.

## Recommended simplified Figure 1 layout
1. **Panel A (Study system):** world map with verified coordinate points only; note that country totals are unavailable from current metadata.
2. **Panel B (Dataset construction):** funnel/flow: 143 canonical → 99 metadata-available and 112 four-domain overlap → 84 final cohort.
3. **Panel C (Analytical framework):** Phase 2 + 5A + 5B pair/branch scope labels with verified combinations.
4. **Panel D (Hypothesis framework):** Phase 5C hypotheses A-G and pair/branch scope.

## Exact prompt for ChatGPT/image model
"Create a clean, publication-style 4-panel scientific figure titled 'Figure 1. Study overview and analytical workflow'.
Panel A (Study system): plot only verified sample coordinates from figure1_site_coordinates.csv where latitude/longitude are non-null; show points on a world map; do not display country totals; optional legend note 'country-level metadata unavailable in repository'.
Panel B (Dataset construction): show a grounded flow with exact counts: canonical inventory n=143; metadata-available n=99; four-domain overlap (BAC+ITS+EUK+AMF) n=112; final analytical cohort (all four domains + metadata) n=84. Show per-domain availability counts BAC=140, ITS=139, EUK=135, AMF=120 and pairwise overlaps BAC-ITS=137, BAC-EUK=135, BAC-AMF=117, ITS-EUK=132, ITS-AMF=117, EUK-AMF=114.
Panel C (Analytical framework): annotate Phase 2 scope as EUK-ITS, AMF-ITS, AMF-EUK across presence/absence and CLR branches (thresholds 0.05 and 0.10). Annotate Phase 5A scope as BAC-AMF, BAC-EUK, BAC-ITS, AMF-ITS, AMF-EUK, EUK-ITS across presence/absence and CLR; annotate Phase 5B scope as BAC-ITS, AMF-ITS, AMF-EUK, EUK-ITS across presence/absence and CLR.
Panel D (Hypothesis framework): show Phase 5C hypotheses A-G evaluated across BAC-ITS, AMF-ITS, AMF-EUK, EUK-ITS in both presence/absence and CLR branches.
Use neutral colors and avoid claims about biome classes unless provided as verified data."

## Sources used
- results/dataset_qc_v2/canonical_sample_inventory.csv
- results/feasibility/sample_presence_matrix.csv
- results/phase1_coupling/cohort_summary.csv
- results/phase2_confirmatory_coupling/sample_cohort_used.csv
- results/phase2_confirmatory_coupling/phase2_coupling_summary.csv
- results/phase5_bac_integration/phase5_combo_manifest.csv
- results/phase5b_environmental_drivers/phase5b_combo_manifest.csv
- results/phase5c_plant_diversity/phase5c_model_comparison.csv
- results/phase5c_plant_diversity/phase5c_hypothesis_summary.csv
- data/Final_data_with_diversity_prefixed.csv
