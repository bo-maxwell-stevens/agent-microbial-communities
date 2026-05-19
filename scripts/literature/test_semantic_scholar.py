#!/usr/bin/env python3
"""Lightweight connectivity test for Semantic Scholar search."""

import sys

from semantic_scholar_search import search, DELAY


def main() -> None:
    query = sys.argv[1] if len(sys.argv) > 1 else "soil microbiome"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    print(f"[test] query={query!r} limit={limit} base_delay={DELAY}")
    try:
        data = search(query=query, limit=limit)
    except Exception as exc:
        print(f"[test] FAIL: {exc}")
        raise SystemExit(1)

    papers = data.get("data", [])
    print(f"[test] PASS: received {len(papers)} paper(s)")
    if papers:
        first = papers[0]
        print(f"[test] first_title={first.get('title')}")
        print(f"[test] first_year={first.get('year')}")


if __name__ == "__main__":
    main()
