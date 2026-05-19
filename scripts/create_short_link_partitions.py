#!/usr/bin/env python3
"""Call PostgreSQL ``create_short_link_partition`` for UTC months (needs DATABASE_URL + migration that defines the function)."""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import create_async_engine


def _parse_month(s: str) -> tuple[int, int]:
    parts = s.strip().split("-")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("expected YYYY-MM")
    y, m = int(parts[0]), int(parts[1])
    if not 1 <= m <= 12:
        raise argparse.ArgumentTypeError("month must be 01-12")
    return y, m


def _utc_months_from_now(count: int) -> list[tuple[int, int]]:
    t = datetime.now(timezone.utc)
    y, m, out = t.year, t.month, []
    for _ in range(count):
        out.append((y, m))
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return out


async def _run(url: str, months: list[tuple[int, int]]) -> None:
    engine = create_async_engine(url)
    try:
        async with engine.begin() as conn:
            for y, mo in months:
                start = datetime(y, mo, 1, tzinfo=timezone.utc)
                await conn.execute(select(func.create_short_link_partition(start)))
    finally:
        await engine.dispose()


def main() -> None:
    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
    p = argparse.ArgumentParser(
        description="Create short_link monthly partitions via create_short_link_partition()."
    )
    p.add_argument(
        "--ahead",
        type=int,
        default=2,
        metavar="N",
        help="This UTC month plus the next N-1 (default: 2). Ignored if --month is set.",
    )
    p.add_argument(
        "--month",
        action="append",
        dest="months",
        type=_parse_month,
        metavar="YYYY-MM",
        help="Explicit month (repeatable).",
    )
    args = p.parse_args()
    url = os.environ.get("DATABASE_URL")
    if not url:
        print("DATABASE_URL is not set.", file=sys.stderr)
        sys.exit(1)
    if args.months:
        months = args.months
    elif args.ahead < 1:
        print("--ahead must be at least 1.", file=sys.stderr)
        sys.exit(1)
    else:
        months = _utc_months_from_now(args.ahead)
    asyncio.run(_run(url, months))


if __name__ == "__main__":
    main()
