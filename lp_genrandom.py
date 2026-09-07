"""Make a random LP-shaped transcription while keeping its boundaries."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

from gematria import INDEX_TO_RUNE, MODULUS
from lp_format import format_transcription, read_transcription

HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE / "lp2.txt"
DEFAULT_OUTPUT = HERE / "lp2-randomized.txt"


def randomize_pages(pages, seed: int = 20260906):
    """Replace every rune with a uniform random GP rune, preserving stops."""
    rng = random.Random(seed)
    return [
        [
            [
                [INDEX_TO_RUNE[rng.randrange(MODULUS)] for _rune in word]
                for word in line
            ]
            for line in page
        ]
        for page in pages
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate randomized LP2 text")
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--seed", type=int, default=20260906)
    args = parser.parse_args()

    pages = read_transcription(args.input)
    Path(args.output).write_text(
        format_transcription(randomize_pages(pages, args.seed)),
        encoding="utf-8",
    )
    print(f"wrote {args.output} (seed {args.seed})")


if __name__ == "__main__":
    main()
