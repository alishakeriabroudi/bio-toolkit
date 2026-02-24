from __future__ import annotations

from collections.abc import Iterable, Sequence


def print_table(rows: Iterable[Sequence[str]], header: Sequence[str] | None = None) -> None:
    rows = list(rows)
    if header is not None:
        rows = [list(header)] + [list(r) for r in rows]
    widths = [0] * (len(rows[0]) if rows else 0)
    for r in rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(str(c)))
    for idx, r in enumerate(rows):
        line = "  ".join(str(c).ljust(widths[i]) for i, c in enumerate(r))
        print(line)
        if header is not None and idx == 0:
            print("  ".join("-" * w for w in widths))
