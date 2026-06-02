# Repository Cleanup Plan (Execution Playbook)

- Repository: `/srv/hermes_projects/agent_microbial_communities`
- Branch context: `cleanup-audit-v0.6`
- Safety policy: no scientific code edits; no analysis reruns; no destructive action until explicit approval.

## Baseline findings (from inventory audit)

- Untracked top-level entries: 15
- Largest reclaim targets:
  - `venv/` ≈ 440,292,831 B
  - `scripts/analysis/env/` ≈ 338,578,527 B
  - `.denario_env/` ≈ 2,301,244,988 B (ignored)
  - `.venv/` ≈ 1,801,841,465 B (ignored)
- `.gitignore` currently misses several local/generated paths.

---

## Phase A: `.gitignore` hardening (first, non-destructive)

| action | exact command | est. space saved | risk |
|---|---|---:|---|
| add local env + generated artifacts ignore rules | `cat >> .gitignore <<EOF\nvenv/\nscripts/analysis/env/\ndenario_runs/\ndata_denario_links/\nidea_generation_output/\ninput_files/\nopencode.json.backup\n# optional policy:\n# opencode.json\nEOF` | 0 B (prevents future clutter) | low |
| verify ignore behavior | `git check-ignore -v venv/ scripts/analysis/env/ denario_runs/ data_denario_links/ idea_generation_output/ input_files/ opencode.json.backup` | 0 B | low |

Notes:
- Keep `.pytest_cache/` unchanged (already ignored).
- `opencode.json` should be policy-driven: ignore only if always local-only.

---

## Phase B: archive moves (non-destructive history preservation)

Create an archive folder (tracked or ignored by policy) and move experimental material there.

| action | exact command | est. space saved in repo root | risk |
|---|---|---:|---|
| create archive staging area | `mkdir -p archive/legacy_denario_$(date +%Y%m%d)` | 0 B | low |
| archive denario script prototypes | `mv scripts/run_denario_exploration.py scripts/test_denario_idea.py scripts/test_denario_minimal.py archive/legacy_denario_$(date +%Y%m%d)/` | ~8 KB from active tree | medium |
| archive generated denario folders | `mv denario_runs idea_generation_output input_files data_denario_links archive/legacy_denario_$(date +%Y%m%d)/` | ~15 KB from active tree | medium |
| archive uncertain analysis/test additions | `mv scripts/analysis/external_validation_summary_writer.py scripts/analysis/phase2_confirmatory_coupling_analysis.py tests/fixtures archive/legacy_denario_$(date +%Y%m%d)/` | ~3 KB from active tree | medium |

Notes:
- This phase intentionally preserves material instead of deleting.
- If archive directory should remain local-only, add `archive/` to `.gitignore`.

---

## Phase C: environment consolidation (largest savings)

Canonical strategy recommendation: **standardize on `.venv`** for local + Rocket workflows.

| action | exact command | est. space saved | risk |
|---|---|---:|---|
| confirm active interpreter in docs/scripts | `grep -RIn "venv/bin/activate\|.venv/bin/activate\|scripts/analysis/env" docs scripts` | 0 B | low |
| remove duplicate local env `venv/` after validation | `rm -rf venv` | ~440 MB | medium |
| remove nested env `scripts/analysis/env/` after validation | `rm -rf scripts/analysis/env` | ~339 MB | medium |
| optional: remove `.denario_env/` if Denario retired | `rm -rf .denario_env` | ~2.30 GB | high |

Notes:
- Do **not** remove `.venv/` if it is the canonical runtime.
- Recreate canonical env when needed: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` (or project-specific install command).

---

## Phase D: cache/temp cleanup

| action | exact command | est. space saved | risk |
|---|---|---:|---|
| remove backup/temp file | `rm -f opencode.json.backup` | ~577 B | low |
| remove empty placeholder script | `rm -f scripts/run_phase2_confirmatory_coupling_with_patch.py` | ~1 B | low |
| clean pytest cache | `rm -rf .pytest_cache` | ~1.6 KB | low |
| remove empty noncritical directories | `find configs notebooks prompts reports -type d -empty -print -delete` | negligible | low |

---

## Phase E: final validation

Run after each cleanup step block:

| action | exact command | est. space saved | risk |
|---|---|---:|---|
| check tracked changes only | `git status --short --untracked-files=no` | 0 B | low |
| check whitespace/conflict markers | `git diff --check` | 0 B | low |
| inspect remaining untracked/ignored | `git status --short && git status --ignored --short | head -200` | 0 B | low |
| verify phase outputs still present (no rerun) | `find results -maxdepth 2 -type d | sort` | 0 B | low |

---

## Prioritized execution order

1. Phase A (`.gitignore` hardening)
2. Phase B (archive candidates)
3. Phase D (safe tiny deletions)
4. Phase C (environment consolidation)
5. Phase E (final validation)

## Estimated reclaimable disk space

- Conservative (safe tiny cleanup only): ~0.02 MB
- Practical (remove `venv/` + `scripts/analysis/env/`): **~778.9 MB**
- Aggressive (plus `.denario_env/`): **~3.08 GB** additional
- Maximum if also removing `.venv/` (not recommended if canonical): +~1.80 GB
