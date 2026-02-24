# bio-toolkit

A small, dependency-free bioinformatics toolkit in **pure Python**.

## Install
```bash
python -m pip install .
```

## CLI quickstart
```bash
bio-toolkit --help

# GC% per FASTA record
bio-toolkit gc tests/data/example.fa

# Reverse-complement a sequence
bio-toolkit revcomp ATGC

# Simple Smith–Waterman local alignment
bio-toolkit sw ACACACTA AGCACACA

# FASTQ cycle stats (mean Q and N fraction)
bio-toolkit fastq-stats tests/data/example.fq

# VCF quick stats (SNP/INDEL + Ti/Tv)
bio-toolkit vcf-stats tests/data/example.vcf
```

## Development
```bash
python -m pip install -U pip
pip install -e ".[dev]"
ruff check .
black --check .
pytest
```

## License
MIT.
