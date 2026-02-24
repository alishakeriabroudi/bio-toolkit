from pathlib import Path

ci = """name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install tools
        run: |
          python -m pip install -U pip
          pip install black ruff pytest

      - name: Lint
        run: ruff check .

      - name: Format check
        run: black --check .

      - name: Install package
        run: pip install .

      - name: Tests
        run: pytest -q
"""

pp = """[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "bio-toolkit"
version = "0.2.0"
description = "Pure-Python bioinformatics toolkit: FASTA/FASTQ/VCF utilities, ORF finder, and simple alignment."
readme = "README.md"
requires-python = ">=3.9"
license = {text = "MIT"}
authors = [{name="Ali Shakeri Abroudi"}]
keywords = ["bioinformatics", "fasta", "fastq", "vcf", "alignment"]

[project.optional-dependencies]
dev = ["pytest>=7", "ruff>=0.5", "black>=24.0"]

[project.scripts]
bio-toolkit = "bio_toolkit.cli:main"

[tool.setuptools]
packages = ["bio_toolkit"]

[tool.ruff]
line-length = 100
target-version = "py39"
select = ["E","F","I","B","UP","SIM"]
ignore = ["E501"]

[tool.black]
line-length = 100
target-version = ["py39"]

[tool.pytest.ini_options]
addopts = "-q"
"""

cff = """cff-version: 1.2.0
message: "If you use this software, please cite it as below."
title: "bio-toolkit"
version: "0.2.0"
authors:
  - family-names: "Shakeri Abroudi"
    given-names: "Ali"
license: "MIT"
repository-code: "https://github.com/alishakeriabroudi/bio-toolkit"
"""

Path(".github/workflows").mkdir(parents=True, exist_ok=True)
Path(".github/workflows/ci.yml").write_text(ci, encoding="utf-8", newline="\n")
Path("pyproject.toml").write_text(pp, encoding="utf-8", newline="\n")
Path("CITATION.cff").write_text(cff, encoding="utf-8", newline="\n")

print("OK")
