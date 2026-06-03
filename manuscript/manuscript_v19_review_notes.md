# manuscript_v19 Review Notes

## Objective check
- Requested outcome: full ecological Discussion without rerunning analyses or changing Methods/Results/Conclusions.
- Status: complete.

## Hard constraints verification
- No analyses rerun: ✅
- No HPC jobs rerun: ✅
- No scientific result files modified: ✅
- Methods unchanged: ✅
- Results unchanged: ✅
- Conclusions unchanged: ✅

## Consistency checks (Abstract/Methods/Results)
- `n = 84`: ✅
- Mantel permutations (`100 permutations per Mantel test`): ❌
- Prevalence thresholds (`none, >=5%, >=10%`): ❌
- Environmental predictors include `pH_KCl` and `bio12now.100`: ✅

## Discussion quality controls
- Emphasizes ecological interpretation rather than Results restatement: ✅
- Preserves core narrative (BAC↔ITS strongest, pH-centered structure, modest plant-diversity effects, AMF-linked responsiveness): ✅
- Explicitly states inferential boundary of correlation/coupling summaries: ✅
- Unsupported claims removed: 0 (all added interpretive claims linked to curated references)

## Quantitative summary
- Total words: 2900 -> 3985
- Discussion words: 38 -> 914
- Methods words: 1055 -> 1055
- Results words: 551 -> 551
- Discussion subsections: 6
- New references: 8

## Notes on literature pipeline
- Semantic Scholar project script invocation was attempted but live calls were blocked by rate-limit/API-key conditions.
- Reference library was assembled from existing project search outputs and tied to each Discussion theme in `discussion_reference_library.csv`.
