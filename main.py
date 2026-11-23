#!/usr/bin/env python3
"""Entry for make.fun bounty news-image-20261123.

Writes /output/entry.png by copying the committed entry.png bytes.
Pure standard library: no third-party imports, so it runs under `python3 -S`.
"""
import os
import shutil
import sys


def main():
    # The image is committed in this repo; the program only relays its bytes
    # so both runs produce byte-identical output with no network and no
    # third-party dependencies.
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as fin, open(dst, "wb") as fout:
        shutil.copyfileobj(fin, fout, length=1024 * 1024)
    return 0


if __name__ == "__main__":
    sys.exit(main())
