#!/usr/bin/env python3
"""One Line, One Laugh — make.fun entry.

Writes one funny line (a single line, 1 to 200 characters) to
/output/entry.txt. Deterministic by design: stdlib only, no network,
no randomness, no clock reads. Two runs produce byte-identical
output.

The joke: the writer's houseplants died of neglect, so the writer
bought plastic ones — and now feels guilty for not watering those
too. The guilt survives the switch from living plants to plastic
ones; the punchline is that the neglect outlived the plants.
"""

import os

# The line is assembled from its two halves so the joke's structure
# stays visible in the code: the setup states the everyday mishap
# (houseplants died of neglect, replaced with plastic ones), the
# punchline saves the surprise for the end (the writer now feels
# guilty for not watering the plastic ones too). Neither half is
# funny alone; the turn is the joke.
_CLAUSE_SETUP = "My houseplants died of neglect, so I bought plastic ones —"
_CLAUSE_PUNCH = "and now I feel guilty for not watering those too."

MAX_LINE_CHARS = 200  # competition ceiling for the single line


def build_line() -> str:
    """Return the one-line laugh.

    The result must be exactly one line: a stray newline in the line
    would silently break the entry format, so fail loudly instead of
    writing a malformed file. It must also be more than whitespace:
    the gate refuses a file that is only white space.
    """
    line = _CLAUSE_SETUP + " " + _CLAUSE_PUNCH
    if "\n" in line or "\r" in line:
        raise ValueError("line clauses must not contain line breaks")
    if not line.strip():
        raise ValueError("line must not be only white space")
    return line


def resolve_output_path() -> str:
    """Return the path of the file the line is written to.

    The kit sets MAKEFUN_OUTPUT_DIR for the run; when it is absent
    we fall back to the conventional ``/output`` directory so the
    program still behaves the same way when run by hand.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(output_dir, "entry.txt")


def main() -> None:
    """Write the line to the output file, with no trailing newline.

    The gate requires 1 to 200 characters of UTF-8 text, so the
    line is validated here before it is written: one line, no line
    breaks, and within the limit. After writing, the file is read
    back and its character count re-checked, so a truncated or
    altered write fails loudly instead of shipping a bad entry.
    """
    line = build_line()
    if not 1 <= len(line) <= MAX_LINE_CHARS:
        raise ValueError("line must be 1 to 200 characters")
    output_path = resolve_output_path()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    with open(output_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        raise ValueError("written line does not match the built line")
    if not 1 <= len(written) <= MAX_LINE_CHARS:
        raise ValueError("written line is outside 1 to 200 characters")


if __name__ == "__main__":
    main()
