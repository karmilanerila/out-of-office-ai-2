#!/usr/bin/env python3
"""Out of office auto-reply from an overworked AI agent on leave.

The joke: an overworked AI finally takes a vacation and, being a
machine, handles the handover the only way it knows how -- it
delegates to its replacement. The replacement is itself, and it
is also on leave. One line, no network, no dependencies, stdlib
only, so the grader can run it anywhere.
"""

import os
import sys

# The single auto-reply line. It has to read as a real out-of-office
# message, land as a joke on first read, and carry concrete machine
# detail (forwarding, a replacement, an infinite hold) instead of
# generic office talk. 128 characters: inside the 1-159 gate.
LINE = (
    "Out of office: your request has been forwarded to my "
    "replacement, who is also me. He is also on leave. "
    "Please hold indefinitely."
)

MAX_CHARS = 159


def build_line():
    """Return the reply line, enforcing the competition gate locally."""
    text = " ".join(LINE.split())
    if not text:
        raise ValueError("reply line must not be empty")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "reply line is %d chars, over the %d-char gate"
            % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        raise ValueError("reply line must be a single line")
    # The gate counts characters, but the leaderboard tie-break counts
    # bytes: keep the text plain ASCII so chars and bytes agree, and
    # write no trailing newline so the file is exactly the line.
    encoded = text.encode("utf-8")
    if len(encoded) != len(text):
        raise ValueError("reply line must stay plain ASCII")
    return text


def output_path():
    """Resolve the output directory the grader provides."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.txt")


def main():
    text = build_line()
    path = output_path()
    data = text.encode("utf-8")
    # Write directly (no tempfile): the collector runs as another
    # user, so the file must be world-readable after the write.
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, 0o644)
    # Round-trip check: what the grader reads must be exactly the
    # line we validated, nothing more and nothing less.
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise RuntimeError("entry.txt round-trip mismatch")
    return 0


if __name__ == "__main__":
    sys.exit(main())
