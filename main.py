#!/usr/bin/env python3
"""news-image-20261117 entrypoint.

Copies the front-page image bundled in this repository (entry.png, the
whole of Tuesday 17 November 2026 in one picture) to /output/entry.png,
where the competition runner expects to find it.  Standard library only,
no network, fully deterministic.
"""

import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEST = Path("/output/entry.png")


def main() -> int:
    if not SOURCE.is_file():
        print(f"error: bundled image not found at {SOURCE}", file=sys.stderr)
        return 1
    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    if DEST.read_bytes() != SOURCE.read_bytes():
        print(f"error: copy at {DEST} does not match {SOURCE}", file=sys.stderr)
        return 1
    print(f"wrote {DEST} ({DEST.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
