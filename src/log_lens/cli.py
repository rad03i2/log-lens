from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

from .core import LogLensError, filter_records, read_records, summarize

VERSION = "1.0.0"


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="log-lens", description="Inspect text logs locally without uploading them.")
    p.add_argument("--version", action="version", version=f"Log Lens {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    sub = p.add_subparsers(dest="command", required=True)

    def source(cmd: argparse.ArgumentParser) -> None:
        cmd.add_argument("file", type=Path)
        cmd.add_argument("--encoding", default="utf-8")

    search = sub.add_parser("search", help="Filter log lines")
    source(search)
    search.add_argument("--level", help="TRACE, DEBUG, INFO, WARN, ERROR or CRITICAL")
    search.add_argument("--contains", help="Literal substring")
    search.add_argument("--regex", help="Python regular expression")
    search.add_argument("-i", "--ignore-case", action="store_true")
    search.add_argument("--invert", action="store_true")
    search.add_argument("--limit", type=int, default=200)
    search.add_argument("--json", action="store_true")

    summary = sub.add_parser("summary", help="Summarize severity counts and timestamp range")
    source(summary)
    summary.add_argument("--json", action="store_true")

    tail = sub.add_parser("tail", help="Print the last N lines")
    source(tail)
    tail.add_argument("-n", "--lines", type=int, default=20)

    follow = sub.add_parser("follow", help="Follow appended lines until interrupted")
    source(follow)
    follow.add_argument("--interval", type=float, default=0.5)
    return p


def _records(args):
    return read_records(args.file, encoding=args.encoding)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "search":
            if args.limit < 1 or args.limit > 10000:
                raise LogLensError("--limit must be between 1 and 10000")
            rows = list(filter_records(_records(args), level=args.level, contains=args.contains,
                                       regex=args.regex, ignore_case=args.ignore_case, invert=args.invert))[:args.limit]
            if args.json:
                print(json.dumps([r.as_dict() for r in rows], ensure_ascii=False, indent=2))
            else:
                for row in rows:
                    print(f"{row.number:>7} | {row.text}")
            return 0 if rows else 1

        if args.command == "summary":
            data = summarize(_records(args))
            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                print(f"Lines: {data['total_lines']}")
                for level, count in data["levels"].items():
                    print(f"{level:>12}: {count}")
                print(f"First timestamp: {data['first_timestamp'] or '-'}")
                print(f"Last timestamp:  {data['last_timestamp'] or '-'}")
            return 0

        if args.command == "tail":
            if not 1 <= args.lines <= 10000:
                raise LogLensError("--lines must be between 1 and 10000")
            rows = list(_records(args))[-args.lines:]
            for row in rows:
                print(row.text)
            return 0

        if args.command == "follow":
            if args.interval < 0.05:
                raise LogLensError("--interval must be at least 0.05 seconds")
            with args.file.open("r", encoding=args.encoding, errors="replace") as handle:
                handle.seek(0, 2)
                while True:
                    line = handle.readline()
                    if line:
                        print(line, end="", flush=True)
                    else:
                        time.sleep(args.interval)
    except KeyboardInterrupt:
        return 130
    except (LogLensError, OSError, LookupError) as exc:
        print(f"log-lens: error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
