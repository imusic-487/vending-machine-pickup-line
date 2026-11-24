#!/usr/bin/env python3
"""Write the vending machine pickup line to /output/entry.txt.

The line lives in line.txt beside this file. This program reads it,
checks it against the competition gate (UTF-8 text, 1-200
characters, a single line, not only white space), writes it byte
for byte to /output/entry.txt and reads the output back to prove
the copy is exact.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LINE_FILE = HERE / "line.txt"
OUTPUT_FILE = Path("/output/entry.txt")

MIN_CHARS = 1
MAX_CHARS = 200


def read_entry():
    raw = LINE_FILE.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("line.txt must not start with a UTF-8 BOM")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("line.txt is not valid UTF-8") from error


def validate(text):
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, "
            f"got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def first_difference(expected, actual):
    for index, (left, right) in enumerate(zip(expected, actual)):
        if left != right:
            return index
    if len(expected) != len(actual):
        return min(len(expected), len(actual))
    return None


def write_and_verify(text):
    data = text.encode("utf-8")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_bytes(data)
    back = OUTPUT_FILE.read_bytes()
    diff = first_difference(data, back)
    if diff is not None:
        raise ValueError(
            f"output differs from line.txt at byte {diff}: "
            f"wrote {data[diff:diff + 1]!r}, read back {back[diff:diff + 1]!r}"
        )
    return len(data)


def main():
    try:
        size = write_and_verify(validate(read_entry()))
    except (ValueError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"wrote {size} bytes to {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
