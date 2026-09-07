# LP2 index-sum checks

These small Python scripts test numerical patterns in Liber Primus 2 (LP2)
words. They use the Gematria Primus zero-based index of each rune and count
words whose alternating checksum is zero.

## Checksum

For a word with GP indices `x0, x1, x2, ...`:

```text
A(word) = (x0 - x1 + x2 - x3 + ...) mod 29
```

An `A=0` occurrence is a word where this result is zero. The script also
reports whether those words have odd, even, or prime lengths.

## Transcription format

- `-` separates words
- `/` ends a line
- `%` ends a page

## Files

- `gematria.py` — Gematria Primus rune, prime-value, and GP-index table.
- `lp_format.py` — reads, writes, and parses the compact transcription format.
- `lp_checksum.py` — calculates checksums and finds `A=0` words.
- `lp_genrandom.py` — creates a randomized LP-shaped transcription while
  preserving the word, line, and page boundaries.
- `run_tests.py` — compares the real and randomized bodies. Set
  `MINIMUM_LENGTH` near the top to adjust the filtered length cutoff.
- `lp2.txt` — normalized LP2 transcription used by the tests.
- `lp2-randomized.txt` — generated randomized comparison body.

## Run

```text
python lp_genrandom.py
python run_tests.py
```
