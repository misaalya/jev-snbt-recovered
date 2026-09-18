#!/usr/bin/env python3
"""Crop a figure out of a PDF page into data/figures/.

Usage: crop.py <page> <x0> <y0> <x1> <y1> <name>
Coordinates are in pixels of the 110-dpi review render (data/pages/p-NNN.png);
the crop itself is taken from a 200-dpi render for legibility.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "dataset" / "MMASNBT2025.pdf"
OUT = ROOT / "data" / "figures"
REVIEW_DPI, CROP_DPI = 110, 200


def main():
    page, x0, y0, x1, y1 = (int(v) for v in sys.argv[1:6])
    name = sys.argv[6]
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(
            ["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(CROP_DPI), "-png", "-singlefile", str(PDF), f"{td}/p"],
            check=True,
        )
        img = Image.open(f"{td}/p.png")
        k = CROP_DPI / REVIEW_DPI
        box = tuple(int(round(v * k)) for v in (x0, y0, x1, y1))
        OUT.mkdir(parents=True, exist_ok=True)
        dest = OUT / f"{name}.png"
        img.crop(box).save(dest)
        print(f"{dest.relative_to(ROOT)} {img.crop(box).size}")


if __name__ == "__main__":
    main()
