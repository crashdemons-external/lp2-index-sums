"""Compare A=0 counts in the real and randomized LP2-shaped bodies."""

from __future__ import annotations

from pathlib import Path

from lp_checksum import a_zero_words, all_words
from lp_format import read_transcription
from lp_genrandom import DEFAULT_INPUT, DEFAULT_OUTPUT, main as generate_random

# Change this one number to adjust the length cutoff for the second table.
MINIMUM_LENGTH = 5


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 1
    return True


def summary(path: Path, minimum_length: int = 1) -> dict[str, int | str]:
    pages = read_transcription(path)
    words = a_zero_words(pages, minimum_length)
    body_words = [word for word in all_words(pages) if len(word) >= minimum_length]
    lengths = [len(word) for word in words]
    return {
        "body": path.name,
        "total_words": len(body_words),
        "a_zero": len(words),
        "odd_length": sum(length % 2 == 1 for length in lengths),
        "even_length": sum(length % 2 == 0 for length in lengths),
        "prime_length": sum(is_prime(length) for length in lengths),
    }


def main() -> None:
    if not DEFAULT_OUTPUT.exists():
        # Keep the usual one-command workflow convenient.
        generate_random()

    scopes = [(1, "all lengths")]
    if MINIMUM_LENGTH != 1:
        scopes.append((MINIMUM_LENGTH, f"length >= {MINIMUM_LENGTH}"))

    for minimum_length, label in scopes:
        print(f"{label}")
        rows = [summary(DEFAULT_INPUT, minimum_length),
                summary(DEFAULT_OUTPUT, minimum_length)]
        print("body                 words   A=0   odd   even   prime")
        for row in rows:
            print(
                f"{row['body']:<20} {row['total_words']:>5} {row['a_zero']:>5}"
                f" {row['odd_length']:>5} {row['even_length']:>6}"
                f" {row['prime_length']:>7}"
            )


if __name__ == "__main__":
    main()
