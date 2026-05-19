#!/usr/bin/env python3
import csv
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

import requests

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "paperId,title,year,authors,abstract,url,citationCount,influentialCitationCount,venue,fieldsOfStudy"
MAX_RETRIES = 5
BACKOFF_MULTIPLIER = 2.0
DEFAULT_LIMIT = 8

QUERIES = [
    "plant dark diversity microbial communities",
    "community completeness soil microbiome",
    "dark diversity belowground ecology",
    "plant community completeness microbial diversity",
    "dark diversity environmental filtering",
    "soil cross kingdom microbial interactions",
    "fungi bacteria protist interactions soil",
    "multi kingdom soil microbiome ecology",
    "cross domain microbial ecology",
    "soil microbiome assembly across kingdoms",
    "plant diversity soil microbiome relationships",
    "plant community composition microbial diversity",
    "plant richness microbial community assembly",
    "vegetation completeness soil microbiome",
    "deterministic stochastic microbial assembly",
    "microbial beta diversity environmental gradients",
    "pH driven microbial community structure",
    "environmental filtering microbiome ecology",
    "compositional microbiome analysis CLR Aitchison",
    "sparse microbiome machine learning",
    "random forest SHAP microbiome ecology",
    "microbial co-occurrence network limitations",
    "joint species distribution microbiome",
    "multi-omics integration ecology",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_delay() -> float:
    val = os.environ.get("SEMANTIC_SCHOLAR_DELAY_SECONDS", "1.05")
    try:
        d = float(val)
    except ValueError:
        d = 1.05
    return max(d, 1.05)


def relevance_note(query: str, paper: Dict[str, Any]) -> str:
    text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
    flags = []
    if any(k in text for k in ["dark diversity", "completeness", "species pool"]):
        flags.append("direct dark-diversity/completeness linkage")
    if any(k in text for k in ["assembly", "stochastic", "deterministic", "filtering"]):
        flags.append("community-assembly mechanism relevance")
    if any(k in text for k in ["soil", "rhizosphere", "plant", "vegetation"]):
        flags.append("plant-soil context relevance")
    if any(k in text for k in ["bacteria", "fung", "protist", "eukary", "kingdom"]):
        flags.append("cross-kingdom microbial relevance")
    if any(k in text for k in ["compositional", "aitchison", "clr", "network", "shap", "machine learning"]):
        flags.append("methodological relevance")
    if not flags:
        flags.append("indirect conceptual/background relevance")
    return "; ".join(flags)


def search_semantic_scholar(query: str, limit: int, delay: float, api_key: str) -> Dict[str, Any]:
    headers = {"x-api-key": api_key} if api_key else {}
    params = {"query": query, "limit": limit, "fields": FIELDS}
    last_error: Optional[Exception] = None

    for attempt in range(1, MAX_RETRIES + 1):
        sleep_s = delay * (BACKOFF_MULTIPLIER ** (attempt - 1))
        time.sleep(sleep_s)
        try:
            r = requests.get(BASE_URL, headers=headers, params=params, timeout=60)
        except requests.RequestException as exc:
            last_error = exc
            if attempt == MAX_RETRIES:
                break
            continue

        if r.status_code == 429:
            last_error = RuntimeError(f"HTTP 429 for query='{query}'")
            if attempt == MAX_RETRIES:
                break
            continue

        if 500 <= r.status_code < 600:
            last_error = RuntimeError(f"HTTP {r.status_code} server error for query='{query}'")
            if attempt == MAX_RETRIES:
                break
            continue

        r.raise_for_status()
        return r.json()

    raise RuntimeError(f"Failed query after {MAX_RETRIES} attempts: {query}; last_error={last_error}")


def main() -> None:
    out_dir = Path("results/literature_search_records")
    out_dir.mkdir(parents=True, exist_ok=True)

    delay = get_delay()
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "")

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_log = out_dir / f"run_{run_id}.json"
    queries_csv = out_dir / f"queries_{run_id}.csv"
    papers_csv = out_dir / f"papers_{run_id}.csv"
    summary_md = out_dir / f"summary_{run_id}.md"

    run_meta = {
        "run_id": run_id,
        "timestamp_utc": now_utc(),
        "delay_seconds": delay,
        "max_retries": MAX_RETRIES,
        "query_count": len(QUERIES),
        "api_key_present": bool(api_key),
        "queries": QUERIES,
    }

    query_rows: List[Dict[str, Any]] = []
    paper_rows: List[Dict[str, Any]] = []

    for i, q in enumerate(QUERIES, start=1):
        q_time = now_utc()
        status = "ok"
        err = ""
        papers: List[Dict[str, Any]] = []
        try:
            data = search_semantic_scholar(q, DEFAULT_LIMIT, delay, api_key)
            papers = data.get("data", []) or []
            with (out_dir / f"query_{i:02d}.json").open("w", encoding="utf-8") as f:
                json.dump({"query": q, "timestamp_utc": q_time, "data": papers}, f, ensure_ascii=False, indent=2)
        except Exception as exc:
            status = "error"
            err = str(exc)
            with (out_dir / f"query_{i:02d}.json").open("w", encoding="utf-8") as f:
                json.dump({"query": q, "timestamp_utc": q_time, "error": err}, f, ensure_ascii=False, indent=2)

        query_rows.append({
            "query_id": i,
            "timestamp_utc": q_time,
            "query": q,
            "status": status,
            "error": err,
            "n_results": len(papers),
            "json_file": f"query_{i:02d}.json",
        })

        for rank, p in enumerate(papers, start=1):
            authors = "; ".join(a.get("name", "") for a in (p.get("authors") or [])[:8])
            paper_rows.append({
                "query_id": i,
                "query": q,
                "rank": rank,
                "paperId": p.get("paperId", ""),
                "title": p.get("title", ""),
                "year": p.get("year", ""),
                "citationCount": p.get("citationCount", ""),
                "influentialCitationCount": p.get("influentialCitationCount", ""),
                "venue": p.get("venue", ""),
                "url": p.get("url", ""),
                "authors": authors,
                "abstract": (p.get("abstract", "") or "").replace("\n", " "),
                "ecological_relevance_note": relevance_note(q, p),
            })

    with queries_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(query_rows[0].keys()))
        w.writeheader()
        w.writerows(query_rows)

    if paper_rows:
        with papers_csv.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(paper_rows[0].keys()))
            w.writeheader()
            w.writerows(paper_rows)

    with run_log.open("w", encoding="utf-8") as f:
        json.dump(run_meta, f, ensure_ascii=False, indent=2)

    ok = sum(1 for r in query_rows if r["status"] == "ok")
    total_papers = len(paper_rows)

    def parse_citations(v: Any) -> int:
        try:
            return int(v)
        except Exception:
            return -1

    top = sorted(paper_rows, key=lambda x: parse_citations(x["citationCount"]), reverse=True)[:25]

    lines = []
    lines.append(f"# Semantic Scholar run {run_id}")
    lines.append("")
    lines.append(f"- timestamp_utc: {run_meta['timestamp_utc']}")
    lines.append(f"- delay_seconds: {delay}")
    lines.append(f"- queries_total: {len(QUERIES)}")
    lines.append(f"- queries_ok: {ok}")
    lines.append(f"- papers_logged: {total_papers}")
    lines.append("")
    lines.append("## Top cited papers across all queries")
    lines.append("")
    for p in top:
        lines.append(f"- [{p['title']}]({p['url']}) ({p['year']}), citations={p['citationCount']}, query=\"{p['query']}\"")
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({
        "run_id": run_id,
        "queries_csv": str(queries_csv),
        "papers_csv": str(papers_csv),
        "summary_md": str(summary_md),
        "queries_ok": ok,
        "queries_total": len(QUERIES),
        "papers_logged": total_papers,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
