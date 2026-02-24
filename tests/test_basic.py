from bio_toolkit.alignment import smith_waterman
from bio_toolkit.analysis import gc_content, reverse_complement


def test_gc_content():
    assert gc_content("GC") == 1.0
    assert gc_content("AT") == 0.0


def test_reverse_complement():
    assert reverse_complement("ATGC") == "GCAT"


def test_smith_waterman_smoke():
    res = smith_waterman("ACACACTA", "AGCACACA")
    assert res.score > 0
    assert len(res.aligned_a) == len(res.aligned_b)
