#!/usr/bin/env python3
"""
batch_rename.py — Batch file rename CLI tool.

Reads a manifest CSV (old_name,new_name) and renames files in the current
directory. Supports --dry-run (preview) and --execute (apply) modes.

Usage:
    python batch_rename.py --manifest manifest.csv --dry-run
    python batch_rename.py --manifest manifest.csv --execute
"""

import argparse
import csv
import os
import re
import sys
from datetime import datetime


# Characters that are illegal on common filesystems
ILLEGAL_CHARS = re.compile(r'[<>:"/\\|?*]')


def load_manifest(manifest_path):
    """Load and parse the manifest CSV file.

    Returns a list of (old_name, new_name) tuples.
    Raises ValueError on empty manifest or malformed rows.
    """
    if not os.path.isfile(manifest_path):
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    entries = []
    with open(manifest_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        required = {"old_name", "new_name"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(
                f"Manifest must contain columns: {required}. "
                f"Found: {reader.fieldnames}"
            )
        for row_num, row in enumerate(reader, start=2):
            old_name = row["old_name"].strip()
            new_name = row["new_name"].strip()
            if not old_name or not new_name:
                raise ValueError(f"Row {row_num}: old_name and new_name must not be empty")
            entries.append((old_name, new_name))

    if not entries:
        raise ValueError("Manifest is empty — no rename entries found")

    return entries


def validate_name(name):
    """Return an error string if *name* contains illegal characters, else None."""
    if ILLEGAL_CHARS.search(name):
        return f"Name '{name}' contains illegal filesystem characters"
    return None


def build_plan(entries, root="."):
    """Validate entries and build an actionable rename plan.

    Returns (plan, warnings) where *plan* is a list of dicts with keys
    old_name, new_name, old_path, new_path, status.
    """
    plan = []
    warnings = []

    for old_name, new_name in entries:
        old_path = os.path.join(root, old_name)
        new_path = os.path.join(root, new_name)

        # Check for illegal characters
        err = validate_name(old_name) or validate_name(new_name)
        if err:
            warnings.append(err)
            plan.append({
                "old_name": old_name,
                "new_name": new_name,
                "old_path": old_path,
                "new_path": new_path,
                "status": "skipped",
                "reason": err,
            })
            continue

        if not os.path.exists(old_path):
            warnings.append(f"Source file not found: {old_path}")
            plan.append({
                "old_name": old_name,
                "new_name": new_name,
                "old_path": old_path,
                "new_path": new_path,
                "status": "skipped",
                "reason": "source not found",
            })
            continue

        plan.append({
            "old_name": old_name,
            "new_name": new_name,
            "old_path": old_path,
            "new_path": new_path,
            "status": "ready",
            "reason": None,
        })

    return plan, warnings


def execute_plan(plan):
    """Execute the rename plan. Returns list of results."""
    results = []
    for entry in plan:
        if entry["status"] != "ready":
            results.append(entry)
            continue

        try:
            os.rename(entry["old_path"], entry["new_path"])
            entry["status"] = "renamed"
            results.append(entry)
        except OSError as exc:
            entry["status"] = "error"
            entry["reason"] = str(exc)
            results.append(entry)
    return results


def format_log(results):
    """Format rename results as a human-readable log."""
    lines = []
    lines.append(f"Batch Rename Log — {datetime.now().isoformat(timespec='seconds')}")
    lines.append("=" * 60)

    for r in results:
        status = r["status"].upper()
        old = r["old_name"]
        new = r["new_name"]
        if status == "RENAMED":
            lines.append(f"  [RENAMED] {old} → {new}")
        elif status == "SKIPPED":
            lines.append(f"  [SKIPPED] {old} → {new}  ({r['reason']})")
        elif status == "ERROR":
            lines.append(f"  [ERROR]   {old} → {new}  ({r['reason']})")

    renamed = sum(1 for r in results if r["status"] == "renamed")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    errors = sum(1 for r in results if r["status"] == "error")
    lines.append("-" * 60)
    lines.append(f"Summary: {renamed} renamed, {skipped} skipped, {errors} errors")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Batch rename files based on a manifest CSV."
    )
    parser.add_argument(
        "--manifest", "-m",
        required=True,
        help="Path to manifest CSV (columns: old_name,new_name)",
    )
    parser.add_argument(
        "--root", "-r",
        default=".",
        help="Root directory where files reside (default: current dir)",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true", help="Preview changes without renaming")
    group.add_argument("--execute", action="store_true", help="Apply renames")

    args = parser.parse_args()

    # Load manifest
    try:
        entries = load_manifest(args.manifest)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    # Build plan
    plan, warnings = build_plan(entries, root=args.root)
    for w in warnings:
        print(f"Warning: {w}", file=sys.stderr)

    if args.dry_run:
        results = plan
        print("DRY-RUN mode — no files were modified.")
    else:
        results = execute_plan(plan)

    log = format_log(results)
    print(log)

    # Exit with error code if any renames failed
    if any(r["status"] == "error" for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
