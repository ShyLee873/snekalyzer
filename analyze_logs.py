#!/usr/bin/env python3
"""
Snekalyzer – A Python tool for analyzing Rails logs
Find slow endpoints, DB-heavy actions, and request stats.
"""

import re
import argparse
from pathlib import Path
from collections import defaultdict

# Regex pattern for Rails "Completed ..." lines
COMPLETED_RE = re.compile(
    r"Completed\s+(?P<status>\d+).+in\s+(?P<total_ms>\d+)ms.*ActiveRecord:\s*(?P<db_ms>[\d\.]+)ms",
)

def parse_log(path):
    """Parse a Rails log file and extract stats for each request path."""
    stats = defaultdict(list)
    current_path = None

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for raw_line in f:
            line = raw_line.strip()

            # Extract path from "Started ..." lines
            if line.startswith("Started "):
                parts = line.split()
                if len(parts) >= 3:
                    current_path = parts[2]

            # Match the "Completed 200 OK in XYZms ..." line
            m = COMPLETED_RE.match(line)
            if m and current_path:
                entry = {
                    "status": int(m.group("status")),
                    "total": int(m.group("total_ms")),
                    "db": float(m.group("db_ms")),
                }
                stats[current_path].append(entry)
                current_path = None  # Reset after completing a request

    return stats


def summarize(stats, top_n=10):
    """Return a list of (path, count, avg_total, avg_db) sorted by avg_total desc."""
    summary = []
    for path, entries in stats.items():
        count = len(entries)
        avg_total = sum(e["total"] for e in entries) / count
        avg_db = sum(e["db"] for e in entries) / count
        summary.append((path, count, avg_total, avg_db))

    summary.sort(key=lambda x: x[2], reverse=True)
    return summary[:top_n]


def main():
    parser = argparse.ArgumentParser(description="Snekalyzer – Rails log analyzer")
    parser.add_argument("logfile", help="Path to a Rails log file")
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Show the top N slowest endpoints (default: 10)",
    )
    args = parser.parse_args()

    log_path = Path(args.logfile)
    if not log_path.exists():
        print(f"Error: File not found: {log_path}")
        return

    stats = parse_log(log_path)
    if not stats:
        print("No valid Rails request entries found in log.")
        return

    results = summarize(stats, top_n=args.top)

    print(f"\n🐍 Snekalyzer Report for {log_path}")
    print(f"{'Path':40} {'Count':>5} {'Avg (ms)':>10} {'Avg DB (ms)':>12}")
    print("-" * 70)
    for path, count, avg_total, avg_db in results:
        print(f"{path:40} {count:5d} {avg_total:10.1f} {avg_db:12.1f}")
    print()


if __name__ == "__main__":
    main()