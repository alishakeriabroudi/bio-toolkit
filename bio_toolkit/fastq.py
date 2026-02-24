from __future__ import annotations

from .io import read_fastq


def fastq_cycle_stats(path: str, max_reads: int = 10_000) -> tuple[list[float], list[float]]:
    """Return per-cycle mean quality and fraction of N bases."""
    counts: list[int] = []
    q_sums: list[int] = []
    n_counts: list[int] = []

    for reads, rec in enumerate(read_fastq(path), start=1):
        if reads > max_reads:
            break

        seq = rec.sequence
        qual = rec.quality
        L = len(seq)

        while len(counts) < L:
            counts.append(0)
            q_sums.append(0)
            n_counts.append(0)

        for i, (b, qch) in enumerate(zip(seq, qual)):
            counts[i] += 1
            q_sums[i] += max(0, ord(qch) - 33)
            if b.upper() == "N":
                n_counts[i] += 1

    mean_q = [(q_sums[i] / counts[i]) if counts[i] else 0.0 for i in range(len(counts))]
    frac_n = [(n_counts[i] / counts[i]) if counts[i] else 0.0 for i in range(len(counts))]
    return mean_q, frac_n
