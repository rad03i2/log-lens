from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Iterable, Iterator

LEVELS = ("TRACE", "DEBUG", "INFO", "WARN", "WARNING", "ERROR", "CRITICAL", "FATAL")
LEVEL_RE = re.compile(r"(?<![A-Z])(" + "|".join(LEVELS) + r")(?![A-Z])", re.I)
ISO_TS_RE = re.compile(r"^\s*(\d{4}-\d{2}-\d{2}[T ][0-9:.+-]+Z?)")


class LogLensError(ValueError):
    pass


@dataclass(frozen=True)
class LogRecord:
    number: int
    text: str
    level: str | None
    timestamp: str | None

    def as_dict(self) -> dict[str, object]:
        return {"line": self.number, "level": self.level, "timestamp": self.timestamp, "text": self.text}


def normalize_level(level: str | None) -> str | None:
    if level is None:
        return None
    value = level.upper()
    if value == "WARNING":
        return "WARN"
    if value == "FATAL":
        return "CRITICAL"
    if value not in {"TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"}:
        raise LogLensError(f"Unsupported level: {level}")
    return value


def parse_line(number: int, text: str) -> LogRecord:
    match = LEVEL_RE.search(text)
    ts = ISO_TS_RE.search(text)
    return LogRecord(number, text.rstrip("\r\n"), normalize_level(match.group(1)) if match else None, ts.group(1) if ts else None)


def iter_records(lines: Iterable[str]) -> Iterator[LogRecord]:
    for number, line in enumerate(lines, 1):
        yield parse_line(number, line)


def filter_records(records: Iterable[LogRecord], *, level: str | None = None, contains: str | None = None,
                   regex: str | None = None, ignore_case: bool = False, invert: bool = False) -> Iterator[LogRecord]:
    wanted = normalize_level(level)
    compiled = None
    if regex:
        if len(regex) > 1000:
            raise LogLensError("Regex is limited to 1000 characters")
        try:
            compiled = re.compile(regex, re.I if ignore_case else 0)
        except re.error as exc:
            raise LogLensError(f"Invalid regex: {exc}") from exc
    needle = contains.casefold() if contains and ignore_case else contains
    for record in records:
        matched = wanted is None or record.level == wanted
        haystack = record.text.casefold() if ignore_case else record.text
        if needle is not None:
            matched = matched and needle in haystack
        if compiled is not None:
            matched = matched and compiled.search(record.text) is not None
        if matched != invert:
            yield record


def summarize(records: Iterable[LogRecord]) -> dict[str, object]:
    items = list(records)
    levels = Counter(r.level or "UNCLASSIFIED" for r in items)
    return {
        "total_lines": len(items),
        "levels": dict(sorted(levels.items())),
        "first_timestamp": next((r.timestamp for r in items if r.timestamp), None),
        "last_timestamp": next((r.timestamp for r in reversed(items) if r.timestamp), None),
    }


def read_records(path: Path, *, encoding: str = "utf-8", max_bytes: int = 100 * 1024 * 1024) -> Iterator[LogRecord]:
    if not path.is_file():
        raise LogLensError(f"Not a readable file: {path}")
    if path.stat().st_size > max_bytes:
        raise LogLensError(f"File exceeds {max_bytes} byte safety limit")
    try:
        with path.open("r", encoding=encoding, errors="replace") as handle:
            yield from iter_records(handle)
    except OSError as exc:
        raise LogLensError(f"Could not read {path}: {exc}") from exc
