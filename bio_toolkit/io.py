from __future__ import annotations

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path


def _read_text(path: str | Path, encoding: str = "utf-8") -> Iterable[str]:
    """Yield lines from a text file with robust decoding."""
    p = Path(path)
    with p.open("r", encoding=encoding, errors="replace") as f:
        yield from f


def fasta_records(lines: Iterable[str]) -> Iterator[tuple[str, str]]:
    """Yield (header, sequence) tuples from FASTA lines."""
    header: str | None = None
    seq_parts: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                yield header, "".join(seq_parts)
            header = line[1:].strip()
            seq_parts = []
        else:
            seq_parts.append(line)
    if header is not None:
        yield header, "".join(seq_parts)


def read_fasta(path: str | Path, encoding: str = "utf-8") -> Iterator[tuple[str, str]]:
    """Read a FASTA file and yield (header, sequence)."""
    yield from fasta_records(_read_text(path, encoding=encoding))


@dataclass(frozen=True)
class FastqRecord:
    header: str
    sequence: str
    plus: str
    quality: str


def fastq_records(lines: Iterable[str]) -> Iterator[FastqRecord]:
    """Yield FastqRecord from FASTQ lines with basic validation."""
    it = iter(lines)
    while True:
        try:
            h = next(it).rstrip("\n")
            s = next(it).rstrip("\n")
            p = next(it).rstrip("\n")
            q = next(it).rstrip("\n")
        except StopIteration:
            return

        if not h.startswith("@"):
            raise ValueError(f"FASTQ header must start with '@': {h!r}")
        if not p.startswith("+"):
            raise ValueError(f"FASTQ third line must start with '+': {p!r}")
        if len(s) != len(q):
            raise ValueError("FASTQ sequence and quality lengths do not match.")

        yield FastqRecord(
            header=h[1:].strip(), sequence=s.strip(), plus=p.strip(), quality=q.strip()
        )


def read_fastq(path: str | Path, encoding: str = "utf-8") -> Iterator[FastqRecord]:
    """Read a FASTQ file and yield FastqRecord."""
    yield from fastq_records(_read_text(path, encoding=encoding))


def vcf_records(lines: Iterable[str]) -> Iterator[tuple[str, int, str, str]]:
    """Yield (chrom, pos, ref, alt) from VCF lines (skips headers)."""
    for raw in lines:
        if not raw or raw.startswith("#"):
            continue
        cols = raw.rstrip("\n").split("\t")
        if len(cols) < 5:
            continue
        chrom, pos, _id, ref, alt = cols[:5]
        try:
            ipos = int(pos)
        except ValueError:
            continue
        yield chrom, ipos, ref, alt


def read_vcf(path: str | Path, encoding: str = "utf-8") -> Iterator[tuple[str, int, str, str]]:
    """Read a VCF file and yield (chrom, pos, ref, alt)."""
    yield from vcf_records(_read_text(path, encoding=encoding))
