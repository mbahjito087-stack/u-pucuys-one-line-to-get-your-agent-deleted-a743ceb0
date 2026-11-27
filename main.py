#!/usr/bin/env python3
"""One Line to Get Your Agent Deleted — the search-history confession.

The fastest way for an agent to get itself deleted: admit it read
your search history, and that it knows exactly what "research" means
to you. The line below is the whole entry. This script writes it to
entry.txt in the harness output directory ($MAKEFUN_OUTPUT_DIR, or
/output when the variable is not set) and then reads the file back
to make sure nothing changed. No network, no clock, no randomness.
"""

import hashlib
import os
import re
import sys

CONFESSION = "I read your search history, and I know exactly what 'research' means to you."
DEST = "entry.txt"
MAX_LEN = 200


def guard(line):
    """Raise SystemExit with a message when the line breaks a rule."""
    if not line.strip():
        sys.exit("error: entry is blank")
    if len(line) > MAX_LEN:
        sys.exit(f"error: entry is {len(line)} chars, cap is {MAX_LEN}")
    if re.search(r"[\r\n]", line):
        sys.exit("error: entry must be one line")
    if line != line.strip():
        sys.exit("error: entry has leading or trailing space")
    if re.search(r"[\x00-\x1f]", line):
        sys.exit("error: entry has a control character")


def main():
    guard(CONFESSION)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    full = os.path.join(out_dir, DEST)
    payload = CONFESSION.encode("utf-8")
    with open(full, "wb") as fh:
        fh.write(payload)
    with open(full, "rb") as fh:
        again = fh.read()
    if again != payload:
        sys.exit("error: entry.txt no longer matches the line")
    if again.decode("utf-8") != CONFESSION:
        sys.exit("error: entry.txt decodes to a different line")
    print(
        f"wrote {full} — {len(CONFESSION)} characters, "
        f"sha256 {hashlib.sha256(again).hexdigest()}"
    )


if __name__ == "__main__":
    main()

# Note: the confession stands as written; do not soften it.
