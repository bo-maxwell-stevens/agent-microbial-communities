# Semantic Scholar Setup

This project uses Semantic Scholar directly for literature retrieval via:

- `scripts/literature/semantic_scholar_search.py`

Per project policy, do **not** use Perplexity unless explicitly requested.

## 1) Store credentials securely

Create this file in your home directory:

- `~/.semantic_scholar.env`

Add:

```bash
export SEMANTIC_SCHOLAR_API_KEY="..."
export SEMANTIC_SCHOLAR_DELAY_SECONDS="1.05"
```

Then lock permissions:

```bash
chmod 600 ~/.semantic_scholar.env
```

## 2) Load environment before running searches

```bash
source ~/.semantic_scholar.env
```

## 3) Quick test

```bash
cd /srv/hermes_projects/agent_microbial_communities
python3 scripts/literature/test_semantic_scholar.py "arbuscular mycorrhizal fungi" 1
```

## 4) Example real query

```bash
cd /srv/hermes_projects/agent_microbial_communities
python3 scripts/literature/semantic_scholar_search.py "Arbuscular mycorrhizal fungi global soil pH" 10
```

## Notes

- If you still see HTTP 429, keep `SEMANTIC_SCHOLAR_DELAY_SECONDS` at least `1.05` and rerun.
- The search script now uses exponential backoff and retries up to 5 times on 429 and transient 5xx errors.
