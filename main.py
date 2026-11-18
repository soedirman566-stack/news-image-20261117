#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261117 competition.

The finished front-page image lives next to this file as ``entry.png``.
The contest harness runs this program offline and expects the image at
``/output/entry.png`` -- byte for byte identical on every run -- so all
this program does is copy the file there.  Standard library only.
"""

import shutil
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEST = Path("/output/entry.png")


def main():
    if not SOURCE.is_file():
        raise SystemExit(f"entry image missing: {SOURCE}")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    # The harness judges the exact bytes, so refuse to finish on a
    # truncated copy: the destination must be as large as the source.
    if DEST.stat().st_size != SOURCE.stat().st_size:
        raise SystemExit("copied image is incomplete")


if __name__ == "__main__":
    main()
