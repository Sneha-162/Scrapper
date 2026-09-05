#!/usr/bin/env python3
"""
scraper.py

Convert web_scraper.ipynb to a runnable script with a small CLI.

Features:
- Accept a URL or a local HTML file as input
- Parse the GitHub Topics page (same selectors used in the notebook)
- Export results to CSV or JSON

Usage examples:
  python scraper.py --input https://github.com/topics --output topics.csv --format csv
  python scraper.py --input webpage.html --output topics.json --format json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import List
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup


DEFAULT_BASE_URL = "https://github.com/"

# CSS classes used in the notebook
TITLE_CLASS = "f3 lh-condensed mb-0 mt-1 Link--primary"
DESC_CLASS = "f5 color-fg-muted mb-0 mt-1"
URL_CLASS = "no-underline flex-grow-0"


def fetch_content(source: str) -> str:
    """Fetch HTML content from a URL or read from a local file.

    Args:
        source: HTTP(S) URL or local file path.
    Returns:
        HTML content as a string.
    Raises:
        RuntimeError on network or I/O errors.
    """
    # Local file
    if os.path.exists(source):
        try:
            with open(source, "r", encoding="utf-8") as fh:
                return fh.read()
        except Exception as e:
            raise RuntimeError(f"Failed to read local file {source}: {e}")

    # URL
    if source.startswith("http://") or source.startswith("https://"):
        try:
            resp = requests.get(source, timeout=15)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            raise RuntimeError(f"Failed to fetch URL {source}: {e}")

    raise RuntimeError("Input must be an existing file path or an http(s) URL")


def parse_topics(html: str, base_url: str = DEFAULT_BASE_URL) -> pd.DataFrame:
    """Parse topic titles, descriptions, and URLs from a GitHub Topics page HTML.

    This follows the approach used in web_scraper.ipynb but extracts cleaned text and
    normalizes URLs.
    """
    soup = BeautifulSoup(html, "html.parser")

    titles: List[str] = [t.get_text(strip=True) for t in soup.find_all("p", class_=TITLE_CLASS)]
    descs: List[str] = [d.get_text(strip=True) for d in soup.find_all("p", class_=DESC_CLASS)]

    # Build absolute URLs from hrefs found on anchor tags with the URL class
    links: List[str] = []
    for a in soup.find_all("a", class_=URL_CLASS):
        href = a.get("href")
        if not href:
            continue
        links.append(urljoin(base_url, href))

    # Align lengths (notebook used separate lists; use the minimum length to avoid mismatches)
    n = min(len(titles), len(descs), len(links))
    titles = titles[:n]
    descs = descs[:n]
    links = links[:n]

    df = pd.DataFrame({"title": titles, "description": descs, "url": links})
    return df


def save_output(df: pd.DataFrame, path: str, fmt: str = "csv") -> None:
    fmt = fmt.lower()
    if fmt == "csv":
        df.to_csv(path, index=False)
    elif fmt == "json":
        df.to_json(path, orient="records", indent=2)
    else:
        raise ValueError("Unsupported format: %s" % fmt)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Simple scraper for GitHub Topics (converted from notebook)")
    parser.add_argument("--input", "-i", default="https://github.com/topics",
                        help="Input URL or local HTML file (default: https://github.com/topics)")
    parser.add_argument("--output", "-o", default="topics.csv", help="Output file path")
    parser.add_argument("--format", "-f", default="csv", choices=["csv", "json"], help="Output format")
    parser.add_argument("--save-html", action="store_true", help="Save fetched page to webpage.html (useful for debugging)")

    args = parser.parse_args(argv)

    try:
        html = fetch_content(args.input)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.save_html:
        try:
            with open("webpage.html", "w", encoding="utf-8") as fh:
                fh.write(html)
            print("Saved fetched HTML to webpage.html")
        except Exception as exc:
            print(f"Warning: failed to save webpage.html: {exc}", file=sys.stderr)

    df = parse_topics(html)

    if df.empty:
        print("No topics found. The page structure may have changed or the selectors need updating.")
        return 1

    try:
        save_output(df, args.output, args.format)
    except Exception as exc:
        print(f"Failed to write output: {exc}", file=sys.stderr)
        return 3

    print(f"Wrote {len(df)} topics to {args.output} ({args.format})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
