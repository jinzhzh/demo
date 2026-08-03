"""Small utilities for text metrics."""

from collections import Counter
import re


def summarize_text_metrics(text: str) -> dict[str, int]:
    """Return character, word, line, and unique-word counts for *text*."""
    words = re.findall(r"\b[\w'-]+\b", text.lower())
    return {
        "characters": len(text),
        "words": len(words),
        "lines": len(text.splitlines()),
        "unique_words": len(Counter(words)),
    }
