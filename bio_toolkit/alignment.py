from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AlignmentResult:
    score: int
    aligned_a: str
    aligned_b: str


def smith_waterman(
    a: str, b: str, match: int = 2, mismatch: int = -1, gap: int = -2
) -> AlignmentResult:
    """Simple Smith–Waterman local alignment (no affine gaps)."""
    a = a.upper()
    b = b.upper()
    m, n = len(a), len(b)

    H = [[0] * (n + 1) for _ in range(m + 1)]
    tb = [[0] * (n + 1) for _ in range(m + 1)]  # 0 stop, 1 diag, 2 up, 3 left

    best = 0
    best_pos = (0, 0)

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diag = H[i - 1][j - 1] + (match if a[i - 1] == b[j - 1] else mismatch)
            up = H[i - 1][j] + gap
            left = H[i][j - 1] + gap
            score = max(0, diag, up, left)

            H[i][j] = score
            if score == 0:
                tb[i][j] = 0
            elif score == diag:
                tb[i][j] = 1
            elif score == up:
                tb[i][j] = 2
            else:
                tb[i][j] = 3

            if score > best:
                best = score
                best_pos = (i, j)

    i, j = best_pos
    aa: list[str] = []
    bb: list[str] = []
    while i > 0 and j > 0 and tb[i][j] != 0:
        if tb[i][j] == 1:
            aa.append(a[i - 1])
            bb.append(b[j - 1])
            i -= 1
            j -= 1
        elif tb[i][j] == 2:
            aa.append(a[i - 1])
            bb.append("-")
            i -= 1
        else:
            aa.append("-")
            bb.append(b[j - 1])
            j -= 1

    return AlignmentResult(
        score=best, aligned_a="".join(reversed(aa)), aligned_b="".join(reversed(bb))
    )
