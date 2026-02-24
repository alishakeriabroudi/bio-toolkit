import subprocess
import sys
from pathlib import Path


def run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "bio_toolkit", *args],
        check=True,
        capture_output=True,
        text=True,
    )


def test_cli_help():
    p = run_cli("--help")
    assert "bio-toolkit" in p.stdout.lower() or "bio-toolkit" in p.stderr.lower()


def test_cli_gc():
    fasta = Path(__file__).parent / "data" / "example.fa"
    p = run_cli("gc", str(fasta))
    assert "seq1" in p.stdout
