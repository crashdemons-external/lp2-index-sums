"""Checksums and simple A=0 counts for parsed LP transcription text."""

from __future__ import annotations

from collections.abc import Iterable

from gematria import MODULUS, RUNE_TO_INDEX


def checksum(word: Iterable[str]) -> int:
    """Return A: alternating zero-based GP indices, reduced modulo 29."""
    total = 0
    for position, rune in enumerate(word):
        sign = 1 if position % 2 == 0 else -1
        total += sign * RUNE_TO_INDEX[rune]
    return total % MODULUS


def all_words(pages) -> list[list[str]]:
    """Flatten pages/lines into a simple list of words."""
    return [word for page in pages for line in page for word in line]


def a_zero_words(pages, minimum_length: int = 1) -> list[list[str]]:
    """Return words whose alternating checksum is zero."""
    return [
        word
        for word in all_words(pages)
        if len(word) >= minimum_length and checksum(word) == 0
    ]


def count_a_zero(pages, minimum_length: int = 1) -> int:
    return len(a_zero_words(pages, minimum_length))
