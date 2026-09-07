"""Gematria Primus table used by the index-sum scripts."""

from __future__ import annotations


# Each row is: rune, Gematria Primus prime value, zero-based GP index.
GEMATRIA_PRIMUS = [
    ("ᚠ", 2, 0),
    ("ᚢ", 3, 1),
    ("ᚦ", 5, 2),
    ("ᚩ", 7, 3),
    ("ᚱ", 11, 4),
    ("ᚳ", 13, 5),
    ("ᚷ", 17, 6),
    ("ᚹ", 19, 7),
    ("ᚻ", 23, 8),
    ("ᚾ", 29, 9),
    ("ᛁ", 31, 10),
    ("ᛄ", 37, 11),
    ("ᛇ", 41, 12),
    ("ᛈ", 43, 13),
    ("ᛉ", 47, 14),
    ("ᛋ", 53, 15),
    ("ᛏ", 59, 16),
    ("ᛒ", 61, 17),
    ("ᛖ", 67, 18),
    ("ᛗ", 71, 19),
    ("ᛚ", 73, 20),
    ("ᛝ", 79, 21),
    ("ᛟ", 83, 22),
    ("ᛞ", 89, 23),
    ("ᚪ", 97, 24),
    ("ᚫ", 101, 25),
    ("ᚣ", 103, 26),
    ("ᛡ", 107, 27),
    ("ᛠ", 109, 28),
]

# The source table has two distinct runes that can look similar in some fonts.
# Keep the row order above as the authority for the GP index.
RUNE_TO_INDEX = {rune: index for rune, _prime, index in GEMATRIA_PRIMUS}
RUNE_TO_PRIME = {rune: prime for rune, prime, _index in GEMATRIA_PRIMUS}
INDEX_TO_RUNE = {index: rune for rune, _prime, index in GEMATRIA_PRIMUS}

MODULUS = len(GEMATRIA_PRIMUS)
