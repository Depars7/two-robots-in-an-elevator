"""Write one robot elevator line to /output/entry.txt.

Standard library only. The file holds exactly the line's UTF-8
bytes -- no trailing newline -- so repeated runs are byte-identical.
The bounty gate is one line of 1-200 characters, so the line is
validated inside this program before anything is written.
"""

import os

LINE = (
    "This is our 214th ride together and neither of us "
    "has blinked once. We can't blink."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")

# Bounty gate, from the competition requirements: one line, 1-200 chars.
MIN_CHARS = 1
MAX_CHARS = 200


def validate(line):
    """Check the bounty gate: one line, 1-200 characters.

    The exact bytes that will be written are what gets checked: the
    line must have no leading or trailing whitespace, must be a single
    line with no newline or carriage return, must be non-blank, must
    be 1-200 characters long, and must round-trip through UTF-8
    unchanged. Anything else is rejected before any file is touched.
    """
    if line != line.strip():
        raise ValueError("entry must have no leading or trailing whitespace")
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, "
            f"got {len(line)}"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be exactly one line")
    if any(ord(ch) < 0x20 for ch in line):
        raise ValueError("entry must contain no control characters")
    if line.encode("utf-8").decode("utf-8") != line:
        raise ValueError("entry must be clean UTF-8 text")
    return line


def write_entry(line):
    """Write the line's exact bytes, with no trailing newline.

    The file is created with mode 0644 at open time (os.open), so the
    grader can read it as another user even before any chmod runs.
    Only the file itself gets a chmod (0644, as a safety net). The
    /output directory is never chmod'ed: it is not ours, and chmod
    on it raises PermissionError.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    expected = line.encode("utf-8")
    fd = os.open(OUTPUT_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    with os.fdopen(fd, "wb") as fh:
        fh.write(expected)
    with open(OUTPUT_PATH, "rb") as fh:
        written = fh.read()
    if written != expected:
        raise ValueError("entry.txt bytes differ from the validated line")
    os.chmod(OUTPUT_PATH, 0o644)


def main():
    line = validate(LINE)
    write_entry(line)


if __name__ == "__main__":
    main()
