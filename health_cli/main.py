#!/usr/bin/env python3
"""
API Health Check CLI - Main Entry Point

A command-line tool for batch checking HTTP status codes and response times
of a list of URLs. Supports configurable timeout and JSON output format.

Usage:
    python main.py https://api.example.com https://httpbin.org/status/200
    python main.py --timeout 5 --json https://api.example.com
    python main.py --urls-file urls.txt --timeout 10
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone

from health_checker import HealthChecker, HealthCheckResult


def parse_arguments():
    """Parse command-line arguments using argparse."""
    parser = argparse.ArgumentParser(
        description="Batch API health checker - check HTTP status codes and response times.",
        epilog="Example: %(prog)s --timeout 5 --json https://api.example.com https://httpbin.org",
    )
    parser.add_argument(
        "urls",
        nargs="*",
        help="One or more URLs to check (mutually exclusive with --urls-file)",
    )
    parser.add_argument(
        "--urls-file",
        type=str,
        help="Path to a file containing URLs (one per line)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="Request timeout in seconds (default: 10)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output results in JSON format",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=0,
        help="Number of retries on failure (default: 0)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Max concurrent requests (default: 5)",
    )
    return parser.parse_args()


def load_urls_from_file(file_path):
    """Load URLs from a text file, one per line."""
    try:
        with open(file_path, "r") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        return urls
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading '{file_path}'.", file=sys.stderr)
        sys.exit(1)


def format_text_output(results):
    """Format results as human-readable text."""
    lines = []
    lines.append("=" * 70)
    lines.append(
        f"  API Health Check Report  ({datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')})"
    )
    lines.append("=" * 70)
    lines.append("")

    for r in results:
        status_icon = "OK" if r.is_healthy else "FAIL"
        lines.append(f"  [{status_icon}] {r.url}")
        lines.append(f"       Status: {r.status_code}  Response Time: {r.response_time_ms:.0f}ms")
        if r.error:
            lines.append(f"       Error: {r.error}")
        lines.append("")

    # Summary
    total = len(results)
    healthy = sum(1 for r in results if r.is_healthy)
    failed = total - healthy
    lines.append("-" * 70)
    lines.append(f"  Summary: {healthy}/{total} healthy, {failed} failed")
    lines.append("-" * 70)

    return "\n".join(lines)


def format_json_output(results):
    """Format results as JSON."""
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "healthy": sum(1 for r in results if r.is_healthy),
        "failed": sum(1 for r in results if not r.is_healthy),
        "results": [r.to_dict() for r in results],
    }
    return json.dumps(output, indent=2)


def main():
    """Main entry point for the CLI."""
    args = parse_arguments()

    # Validate URL sources
    if not args.urls and not args.urls_file:
        print("Error: Provide at least one URL or use --urls-file.", file=sys.stderr)
        print("Usage: %(prog)s URL1 URL2 ...", file=sys.stderr)
        sys.exit(1)

    # Collect URLs
    urls = list(args.urls) if args.urls else []
    if args.urls_file:
        urls.extend(load_urls_from_file(args.urls_file))

    if not urls:
        print("Error: No valid URLs to check.", file=sys.stderr)
        sys.exit(1)

    # Validate timeout
    if args.timeout <= 0:
        print("Error: Timeout must be a positive number.", file=sys.stderr)
        sys.exit(1)

    # Run health checks
    checker = HealthChecker(
        timeout=args.timeout,
        retries=args.retries,
        max_concurrency=args.concurrency,
    )

    try:
        results = checker.check_urls(urls)
    except Exception as e:
        print(f"Error during health check: {e}", file=sys.stderr)
        sys.exit(1)

    # Output results
    if args.json_output:
        print(format_json_output(results))
    else:
        print(format_text_output(results))

    # Exit with non-zero if any check failed
    if any(not r.is_healthy for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
