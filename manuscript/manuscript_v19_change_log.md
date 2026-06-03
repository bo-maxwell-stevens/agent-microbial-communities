# manuscript_v19 Change Log

## Scope
- Built `manuscript_v19.md` from `manuscript_v18.md` with **Discussion-focused expansion only**.
- Kept **Methods, Results, and Conclusions unchanged** (verified by section hash comparison).
- Added supporting literature citations and corresponding entries in References.
- Created `discussion_reference_library.csv` from project Semantic Scholar records.

## Major edits
1. Replaced one-sentence placeholder Discussion with a full ecological interpretation section.
2. Added six Discussion subsections:
   - Cross-domain structure is strong but uneven
   - Environmental filtering is a first-order organizer, with pH as a recurrent axis
   - Plant-diversity effects are modest in magnitude but biologically non-random
   - Coupling interpreted through dark-diversity and completeness logic
   - Deterministic vs stochastic assembly: interpretation without overreach
   - Inference boundaries and future integration priorities
3. Added 8 references used in Discussion interpretation.
4. Added `manuscript/discussion_reference_library.csv` (12 curated references from existing project search records).

## Validation summary
- Total words: 2900 -> 3985
- Discussion words: 38 -> 914
- Methods words: 1055 -> 1055 (unchanged)
- Results words: 551 -> 551 (unchanged)
- Discussion subsection count: 6
- New references added: 8

## Semantic Scholar execution note
- Project script execution was attempted in this session but live calls returned HTTP 429 with missing API-key message.
- `discussion_reference_library.csv` was therefore built from existing repository search records under `results/literature_search_records/`.
