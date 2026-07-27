#!/usr/bin/env python3
"""A tiny dependency-free CLI for turning text into URL-friendly slugs."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata


def slugify(value: str) -> str:
    """Return a normalized, lowercase slug separated by hyphens."""
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value.lower()).strip("-")
    return slug


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert text to a URL-friendly slug.")
    parser.add_argument("text", nargs="?", help="Text to convert; reads stdin when omitted.")
    args = parser.parse_args()

    source = args.text if args.text is not None else sys.stdin.read().strip()
    if not source:
        parser.error("provide text as an argument or through stdin")

    print(slugify(source))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
