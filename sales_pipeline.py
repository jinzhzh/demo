"""
sales_pipeline.py — Sales Data Processing Pipeline
===================================================

Reads a raw sales xlsx file (Date, SKU, Channel, Orders, Revenue, Returns),
aggregates by Channel, computes return rates, and outputs a summary JSON.

Usage:
    python sales_pipeline.py [--input sales_raw_data_2026-07-02.xlsx] [--output summary.json]

Author: Harness Analytics Pipeline
Date:   2026-07-02
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

import openpyxl

# ── Logging ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger: logging.Logger = logging.getLogger(__name__)


# ── Data Types ──────────────────────────────────────────────────────────
Row = dict[str, Any]
ChannelSummary = dict[str, Any]


# ── Core Functions ──────────────────────────────────────────────────────

def read_xlsx(file_path: str) -> list[Row]:
    """Read an xlsx file and return a list of row dicts.

    Expected columns: Date, SKU, Channel, Orders, Revenue, Returns.
    The first row is treated as the header.

    Args:
        file_path: Absolute or relative path to the xlsx file.

    Returns:
        List of dicts, one per data row.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If required columns are missing.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb.active
    if ws is None:
        raise ValueError("Workbook has no active sheet.")

    rows_iter = ws.iter_rows(min_row=1, values_only=True)
    headers = next(rows_iter)  # type: ignore[misc]
    headers = [str(h).strip() for h in headers]

    required = {"Date", "SKU", "Channel", "Orders", "Revenue", "Returns"}
    missing = required - set(headers)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    data: list[Row] = []
    for row in rows_iter:
        values = list(row)
        if all(v is None for v in values):
            continue  # skip empty rows
        data.append(dict(zip(headers, values)))

    wb.close()
    logger.info("Read %d rows from %s", len(data), file_path)
    return data


def coerce_row(row: Row) -> Row:
    """Coerce numeric string values to proper types.

    Args:
        row: A row dict with raw values from openpyxl.

    Returns:
        A new dict with Orders, Revenue, Returns as numeric types.
    """
    return {
        "Date": str(row.get("Date", "")),
        "SKU": str(row.get("SKU", "")),
        "Channel": str(row.get("Channel", "")),
        "Orders": int(row["Orders"]) if row.get("Orders") else 0,
        "Revenue": float(row["Revenue"]) if row.get("Revenue") else 0.0,
        "Returns": int(row["Returns"]) if row.get("Returns") else 0,
    }


def aggregate_by_channel(data: list[Row]) -> list[ChannelSummary]:
    """Aggregate sales data by Channel.

    For each channel, compute:
        - total_orders
        - total_revenue
        - total_returns
        - return_rate (returns / orders)
        - avg_order_value (revenue / orders)
        - unique_skus
        - date_range (min, max)

    Args:
        data: List of coerced row dicts.

    Returns:
        List of channel summary dicts sorted by total_revenue descending.
    """
    buckets: dict[str, dict[str, Any]] = {}

    for row in data:
        channel = row["Channel"]
        if channel not in buckets:
            buckets[channel] = {
                "channel": channel,
                "total_orders": 0,
                "total_revenue": 0.0,
                "total_returns": 0,
                "unique_skus": set(),
                "dates": [],
            }
        b = buckets[channel]
        b["total_orders"] += row["Orders"]
        b["total_revenue"] += row["Revenue"]
        b["total_returns"] += row["Returns"]
        b["unique_skus"].add(row["SKU"])
        b["dates"].append(row["Date"])

    summaries: list[ChannelSummary] = []
    for b in buckets.values():
        orders = b["total_orders"]
        revenue = b["total_revenue"]
        returns = b["total_returns"]
        return_rate = round(returns / orders, 4) if orders else 0.0
        avg_order_value = round(revenue / orders, 2) if orders else 0.0
        dates = sorted(b["dates"])

        summaries.append({
            "channel": b["channel"],
            "total_orders": orders,
            "total_revenue": round(revenue, 2),
            "total_returns": returns,
            "return_rate": return_rate,
            "avg_order_value": avg_order_value,
            "unique_skus": len(b["unique_skus"]),
            "date_min": dates[0] if dates else "",
            "date_max": dates[-1] if dates else "",
        })

    summaries.sort(key=lambda s: s["total_revenue"], reverse=True)
    logger.info("Aggregated into %d channel summaries", len(summaries))
    return summaries


def build_summary(
    data: list[Row],
    channel_summaries: list[ChannelSummary],
) -> dict[str, Any]:
    """Build the final summary dict.

    Args:
        data: Full coerced row list.
        channel_summaries: Channel-level aggregation results.

    Returns:
        Summary dict with pipeline metadata, totals, and channel breakdown.
    """
    total_orders = sum(r["Orders"] for r in data)
    total_revenue = sum(r["Revenue"] for r in data)
    total_returns = sum(r["Returns"] for r in data)
    overall_return_rate = round(total_returns / total_orders, 4) if total_orders else 0.0

    return {
        "metadata": {
            "pipeline": "sales_pipeline.py",
            "version": "1.0.0",
            "generated_by": "Harness Analytics Pipeline",
            "total_rows": len(data),
        },
        "totals": {
            "total_orders": total_orders,
            "total_revenue": round(total_revenue, 2),
            "total_returns": total_returns,
            "overall_return_rate": overall_return_rate,
        },
        "channel_summaries": channel_summaries,
    }


def write_summary(summary: dict[str, Any], output_path: str) -> None:
    """Write the summary dict to a JSON file.

    Args:
        summary: The summary dict to serialize.
        output_path: Destination file path.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    logger.info("Summary written to %s", output_path)


def run_pipeline(input_file: str, output_file: str) -> dict[str, Any]:
    """Run the full pipeline: read → coerce → aggregate → summarize → write.

    Args:
        input_file: Path to the raw xlsx.
        output_file: Path for the output JSON.

    Returns:
        The summary dict.
    """
    raw = read_xlsx(input_file)
    coerced = [coerce_row(r) for r in raw]
    channel_summaries = aggregate_by_channel(coerced)
    summary = build_summary(coerced, channel_summaries)
    write_summary(summary, output_file)
    return summary


# ── CLI Entry Point ─────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed namespace with input and output paths.
    """
    parser = argparse.ArgumentParser(
        description="Sales data processing pipeline: xlsx → aggregation → JSON summary.",
    )
    parser.add_argument(
        "--input",
        default="sales_raw_data_2026-07-02.xlsx",
        help="Path to the raw sales xlsx file.",
    )
    parser.add_argument(
        "--output",
        default="summary.json",
        help="Path for the output summary JSON.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    logger.info("Starting pipeline: input=%s, output=%s", args.input, args.output)
    result = run_pipeline(args.input, args.output)

    # Print a quick summary to stdout
    totals = result["totals"]
    print("\n" + "=" * 60)
    print("  SALES PIPELINE SUMMARY")
    print("=" * 60)
    print(f"  Total Orders:    {totals['total_orders']:,}")
    print(f"  Total Revenue:   ${totals['total_revenue']:,.2f}")
    print(f"  Total Returns:   {totals['total_returns']:,}")
    print(f"  Return Rate:     {totals['overall_return_rate']:.2%}")
    print("-" * 60)
    print(f"  {'Channel':<15} {'Orders':>8} {'Revenue':>14} {'Returns':>8} {'Rate':>8}")
    print("-" * 60)
    for ch in result["channel_summaries"]:
        print(
            f"  {ch['channel']:<15} "
            f"{ch['total_orders']:>8,} "
            f"${ch['total_revenue']:>13,.2f} "
            f"{ch['total_returns']:>8,} "
            f"{ch['return_rate']:>7.2%}"
        )
    print("=" * 60)
    print(f"\n  Full summary → {args.output}")
    print()
