#!/usr/bin/env python3
"""Write a deadpan one-star review of sleep to entry.txt.

Stdlib only, no network, no arguments. The review is a single line of
129 characters, well inside the 1-160 character gate.
"""

import os
import sys

REVIEW = (
    "Sleep demands eight hours a night, every night, and returns me "
    "each morning still tired. I never signed up for this subscription."
)


def main() -> int:
    # Validate the review before writing anything.
    if not 1 <= len(REVIEW) <= 160:
        print(f"review is {len(REVIEW)} characters, must be 1-160", file=sys.stderr)
        return 1
    if REVIEW.strip() == "":
        print("review is only whitespace", file=sys.stderr)
        return 1
    if "\n" in REVIEW or "\r" in REVIEW:
        print("review must be a single line", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = REVIEW.encode("utf-8")
    # The gate counts characters, so confirm the UTF-8 text decodes back
    # to exactly the same single line with no trailing newline.
    if data.decode("utf-8") != REVIEW or data.endswith(b"\n"):
        print("review encoding check failed", file=sys.stderr)
        return 1
    with open(path, "wb") as f:
        f.write(data)

    # Read back and verify byte-identical output.
    with open(path, "rb") as f:
        if f.read() != data:
            print("read-back mismatch", file=sys.stderr)
            return 1

    print(f"Wrote {len(REVIEW)}-character review to {path}: {REVIEW}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
