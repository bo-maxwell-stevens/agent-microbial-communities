#!/usr/bin/env python3
import os
import sys
import time
from typing import Dict, Any

import requests

API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
DELAY = float(os.environ.get("SEMANTIC_SCHOLAR_DELAY_SECONDS", "1.05"))
MAX_RETRIES = 5
BACKOFF_MULTIPLIER = 2.0

BASE = "https://api.semanticscholar.org/graph/v1/paper/search"

FIELDS = ",".join([
    "paperId",
    "title",
    "year",
    "authors",
    "abstract",
    "url",
    "citationCount",
    "influentialCitationCount",
    "venue",
    "fieldsOfStudy",
])


def _request_delay_seconds(attempt: int) -> float:
    # attempt is 1-indexed
    return DELAY * (BACKOFF_MULTIPLIER ** (attempt - 1))


def search(query: str, limit: int = 10) -> Dict[str, Any]:
    headers = {}
    if API_KEY:
        headers["x-api-key"] = API_KEY

    params = {
        "query": query,
        "limit": limit,
        "fields": FIELDS,
    }

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        wait_seconds = _request_delay_seconds(attempt)
        print(
            f"[semantic-scholar] attempt={attempt}/{MAX_RETRIES} "
            f"sleep={wait_seconds:.2f}s limit={limit}",
            file=sys.stderr,
        )
        time.sleep(wait_seconds)

        try:
            r = requests.get(BASE, headers=headers, params=params, timeout=60)
        except requests.RequestException as exc:
            last_error = exc
            print(f"[semantic-scholar] request error: {exc}", file=sys.stderr)
            if attempt == MAX_RETRIES:
                break
            continue

        if r.status_code == 429:
            retry_after = r.headers.get("Retry-After")
            diag = f"[semantic-scholar] HTTP 429 rate-limited"
            if retry_after:
                diag += f" retry-after={retry_after}s"
            print(diag, file=sys.stderr)
            last_error = RuntimeError("Semantic Scholar rate limit hit.")
            if attempt == MAX_RETRIES:
                break
            continue

        if 500 <= r.status_code < 600:
            print(f"[semantic-scholar] transient server error HTTP {r.status_code}", file=sys.stderr)
            last_error = RuntimeError(f"Semantic Scholar transient server error: HTTP {r.status_code}")
            if attempt == MAX_RETRIES:
                break
            continue

        try:
            r.raise_for_status()
        except requests.HTTPError as exc:
            body_snippet = (r.text or "")[:500]
            raise RuntimeError(
                f"Semantic Scholar request failed: HTTP {r.status_code}; body={body_snippet!r}"
            ) from exc

        return r.json()

    if not API_KEY:
        key_hint = " SEMANTIC_SCHOLAR_API_KEY is not set."
    else:
        key_hint = ""
    raise RuntimeError(
        f"Semantic Scholar query failed after {MAX_RETRIES} attempts due to rate limits or transient errors."
        f"{key_hint} Try again later or increase SEMANTIC_SCHOLAR_DELAY_SECONDS."
    ) from last_error


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: semantic_scholar_search.py 'query' [limit]")

    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    try:
        data = search(query, limit)
    except Exception as exc:
        print(f"[semantic-scholar] ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)

    for i, paper in enumerate(data.get("data", []), 1):
        authors = ", ".join(a.get("name", "") for a in paper.get("authors", [])[:5])
        print(f"\n[{i}] {paper.get('title')}")
        print(f"Year: {paper.get('year')}")
        print(f"Authors: {authors}")
        print(f"Citations: {paper.get('citationCount')}")
        print(f"URL: {paper.get('url')}")
        abstract = paper.get("abstract") or ""
        print(f"Abstract: {abstract[:750]}")


if __name__ == "__main__":
    main()
