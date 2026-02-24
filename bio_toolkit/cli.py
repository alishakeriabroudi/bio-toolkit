from __future__ import annotations

import argparse

from .alignment import smith_waterman
from .analysis import gc_content, reverse_complement
from .fastq import fastq_cycle_stats
from .io import read_fasta
from .utils import print_table
from .vcf import vcf_stats


def cmd_gc(args: argparse.Namespace) -> int:
    for header, seq in read_fasta(args.fasta):
        gc = gc_content(seq) * 100
        print(f"{header}\t{gc:.2f}")
    return 0


def cmd_revcomp(args: argparse.Namespace) -> int:
    print(reverse_complement(args.sequence))
    return 0


def cmd_sw(args: argparse.Namespace) -> int:
    res = smith_waterman(args.a, args.b, match=args.match, mismatch=args.mismatch, gap=args.gap)
    print(f"score\t{res.score}")
    print(res.aligned_a)
    print(res.aligned_b)
    return 0


def cmd_fastq_stats(args: argparse.Namespace) -> int:
    mean_q, frac_n = fastq_cycle_stats(args.fastq, max_reads=args.max_reads)
    rows = []
    for i, (mq, fn) in enumerate(zip(mean_q, frac_n), start=1):
        rows.append([str(i), f"{mq:.2f}", f"{100 * fn:.2f}%"])
    print_table(rows, header=["Cycle", "MeanQ", "FracN"])
    return 0


def cmd_vcf_stats(args: argparse.Namespace) -> int:
    stats = vcf_stats(args.vcf)
    rows = [[k, f"{v:.4f}"] for k, v in stats.items()]
    print_table(rows, header=["Metric", "Value"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bio-toolkit", description="bio-toolkit CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_gc = sub.add_parser("gc", help="Compute GC%% for sequences in a FASTA file")
    p_gc.add_argument("fasta", type=str, help="Path to FASTA")
    p_gc.set_defaults(func=cmd_gc)

    p_rc = sub.add_parser("revcomp", help="Reverse complement a DNA sequence")
    p_rc.add_argument("sequence", type=str)
    p_rc.set_defaults(func=cmd_revcomp)

    p_sw = sub.add_parser("sw", help="Smith-Waterman local alignment (simple)")
    p_sw.add_argument("a", type=str)
    p_sw.add_argument("b", type=str)
    p_sw.add_argument("--match", type=int, default=2)
    p_sw.add_argument("--mismatch", type=int, default=-1)
    p_sw.add_argument("--gap", type=int, default=-2)
    p_sw.set_defaults(func=cmd_sw)

    p_fq = sub.add_parser("fastq-stats", help="Per-cycle FASTQ stats (mean Q and N fraction)")
    p_fq.add_argument("fastq", type=str)
    p_fq.add_argument("--max-reads", type=int, default=10_000)
    p_fq.set_defaults(func=cmd_fastq_stats)

    p_vcf = sub.add_parser("vcf-stats", help="VCF quick stats (SNP/INDEL + Ti/Tv)")
    p_vcf.add_argument("vcf", type=str)
    p_vcf.set_defaults(func=cmd_vcf_stats)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
