"""Read and write the small LP transcription format used here.

Format:
  - separates words
  / ends a line
  % ends a page

Whitespace is ignored. Other characters are ignored when parsing this compact
format, which makes the parser tolerant of a final newline or comments.
"""

from __future__ import annotations

from pathlib import Path

from gematria import RUNE_TO_INDEX

WORD_STOP = "-"
LINE_STOP = "/"
PAGE_STOP = "%"


def _finish_word(line: list[list[str]], word: list[str]) -> None:
    if word:
        line.append(word[:])
        word.clear()


def _finish_line(page: list[list[list[str]]], line: list[list[str]], word: list[str]) -> None:
    _finish_word(line, word)
    if line:
        page.append(line[:])
        line.clear()


def parse_transcription(text: str) -> list[list[list[list[str]]]]:
    """Return pages containing lines containing words containing runes."""
    pages: list[list[list[list[str]]]] = []
    page: list[list[list[str]]] = []
    line: list[list[str]] = []
    word: list[str] = []

    for char in text:
        if char in RUNE_TO_INDEX:
            word.append(char)
        elif char == WORD_STOP:
            _finish_word(line, word)
        elif char == LINE_STOP:
            _finish_line(page, line, word)
        elif char == PAGE_STOP:
            _finish_line(page, line, word)
            # Append even an empty page: consecutive % markers represent an
            # empty page slot in the source transcription.
            pages.append(page[:])
            page.clear()

    _finish_line(page, line, word)
    if page:
        pages.append(page)
    return pages


def format_transcription(pages: list[list[list[list[str]]]]) -> str:
    """Return a parsed transcription in the compact text format."""
    output: list[str] = []
    for page in pages:
        for line in page:
            words = ["".join(word) for word in line]
            output.append(WORD_STOP.join(words) + LINE_STOP)
        output.append(PAGE_STOP)
    return "\n".join(output) + ("\n" if output else "")


def read_transcription(path: str | Path) -> list[list[list[list[str]]]]:
    return parse_transcription(Path(path).read_text(encoding="utf-8"))


def write_transcription(path: str | Path, pages: list[list[list[list[str]]]]) -> None:
    Path(path).write_text(format_transcription(pages), encoding="utf-8")


def parse_master_transcription(text: str, page_start: int, page_end: int):
    """Convert the archive master format to this format's page structure.

    The master has punctuation beyond the three compact stops. Those marks
    end the current word, matching the earlier LP2 word parser. The page range
    is zero-based on the master's percent-separated pages.
    """
    raw_pages = text.split(PAGE_STOP)[page_start:page_end]
    pages: list[list[list[list[str]]]] = []

    for raw_page in raw_pages:
        page: list[list[list[str]]] = []
        line: list[list[str]] = []
        word: list[str] = []
        for char in raw_page:
            if char in RUNE_TO_INDEX:
                word.append(char)
            elif char == LINE_STOP:
                _finish_line(page, line, word)
            else:
                # Master punctuation, spaces, and line wrapping all end a
                # word; repeated stops do not create empty words.
                _finish_word(line, word)
        _finish_line(page, line, word)
        pages.append(page)
    return pages


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Normalize an LP transcription")
    parser.add_argument("source", help="input transcription")
    parser.add_argument("output", help="output compact transcription")
    parser.add_argument("--master-pages", action="store_true",
                        help="read the archive master and select pages 16 through 71")
    args = parser.parse_args()

    source_text = Path(args.source).read_text(encoding="utf-8-sig")
    if args.master_pages:
        pages = parse_master_transcription(source_text, 16, 72)
    else:
        pages = parse_transcription(source_text)
    write_transcription(args.output, pages)
