from __future__ import annotations


def gc_content(seq: str) -> float:
    seq = seq.upper()
    if not seq:
        return 0.0
    gc = sum(1 for c in seq if c in {"G", "C"})
    return gc / len(seq)


def reverse_complement(seq: str) -> str:
    comp = str.maketrans({"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"})
    return seq.upper().translate(comp)[::-1]


def codon_table_standard() -> dict[str, str]:
    return {
        "TTT": "F",
        "TTC": "F",
        "TTA": "L",
        "TTG": "L",
        "CTT": "L",
        "CTC": "L",
        "CTA": "L",
        "CTG": "L",
        "ATT": "I",
        "ATC": "I",
        "ATA": "I",
        "ATG": "M",
        "GTT": "V",
        "GTC": "V",
        "GTA": "V",
        "GTG": "V",
        "TCT": "S",
        "TCC": "S",
        "TCA": "S",
        "TCG": "S",
        "CCT": "P",
        "CCC": "P",
        "CCA": "P",
        "CCG": "P",
        "ACT": "T",
        "ACC": "T",
        "ACA": "T",
        "ACG": "T",
        "GCT": "A",
        "GCC": "A",
        "GCA": "A",
        "GCG": "A",
        "TAT": "Y",
        "TAC": "Y",
        "TAA": "*",
        "TAG": "*",
        "CAT": "H",
        "CAC": "H",
        "CAA": "Q",
        "CAG": "Q",
        "AAT": "N",
        "AAC": "N",
        "AAA": "K",
        "AAG": "K",
        "GAT": "D",
        "GAC": "D",
        "GAA": "E",
        "GAG": "E",
        "TGT": "C",
        "TGC": "C",
        "TGA": "*",
        "TGG": "W",
        "CGT": "R",
        "CGC": "R",
        "CGA": "R",
        "CGG": "R",
        "AGT": "S",
        "AGC": "S",
        "AGA": "R",
        "AGG": "R",
        "GGT": "G",
        "GGC": "G",
        "GGA": "G",
        "GGG": "G",
    }


def translate(seq: str) -> str:
    seq = seq.upper().replace("U", "T")
    table = codon_table_standard()
    aa: list[str] = []
    for i in range(0, len(seq) - 2, 3):
        codon = seq[i : i + 3]
        aa.append(table.get(codon, "X"))
    return "".join(aa)


def find_orfs(seq: str, min_aa: int = 30) -> list[tuple[int, int, str]]:
    seq = seq.upper().replace("U", "T")
    stops = {"TAA", "TAG", "TGA"}
    out: list[tuple[int, int, str]] = []
    i = 0
    while i < len(seq) - 2:
        if seq[i : i + 3] == "ATG":
            j = i
            while j < len(seq) - 2:
                codon = seq[j : j + 3]
                if codon in stops:
                    prot = translate(seq[i:j])
                    if len(prot) >= min_aa:
                        out.append((i, j + 3, prot))
                    break
                j += 3
        i += 1
    return out
