from __future__ import annotations

from .io import read_vcf


def vcf_stats(path: str) -> dict[str, float]:
    """Quick VCF stats: SNP, INDEL counts and Ti/Tv."""
    snp = 0
    indel = 0
    ti = 0
    tv = 0

    transitions = {("A", "G"), ("G", "A"), ("C", "T"), ("T", "C")}

    for _chrom, _pos, ref, alt in read_vcf(path):
        ref = ref.upper()
        for a in alt.split(","):
            a = a.upper()
            if len(ref) == 1 and len(a) == 1:
                snp += 1
                if (ref, a) in transitions:
                    ti += 1
                else:
                    tv += 1
            else:
                indel += 1

    titv = (ti / tv) if tv else 0.0
    return {
        "snp": float(snp),
        "indel": float(indel),
        "ti": float(ti),
        "tv": float(tv),
        "titv": float(titv),
    }
