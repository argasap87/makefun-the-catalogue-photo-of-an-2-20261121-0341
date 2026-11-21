#!/usr/bin/env python3
"""The Time Toaster — catalogue photograph of an impossible gadget.

A chrome toaster with an analog clock face built into its body: it toasts
time. One slice of toast pops up as the single accessory. The program
composites a fresh AI-generated studio product photo with PIL, paints a
legible analog clock face onto the toaster's front dial, crops out the
generator watermark, and writes a gate-valid 1024x1024 PNG.

Self-contained, no network at runtime. Writes /output/entry.png
(falls back to ./output/entry.png when /output is not writable).
"""

import math
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw

MAX_BYTES = 1_048_576
SIZE = 1024

HERE = Path(__file__).resolve().parent
ASSET = HERE / "assets" / "time-toaster-v3.png"

# The generator watermark sits in the bottom-right corner; crop the
# bottom strip of the source photo out before compositing.
CROP_BOTTOM = 70

# Round dial on the toaster front, in source-photo coordinates
# (768 x 768 image). The clock face is painted over this dial.
# Centred on the dial recess so no rim of the old dial peeks out.
DIAL_CX, DIAL_CY, DIAL_R = 425, 418, 60


def pick_output_path() -> Path:
    for candidate in (Path("/output/entry.png"), HERE / "output" / "entry.png"):
        try:
            candidate.parent.mkdir(parents=True, exist_ok=True)
            if os.access(candidate.parent, os.W_OK):
                return candidate
        except OSError:
            continue
    return HERE / "output" / "entry.png"


def paint_clock_face(img: Image.Image, cx: float, cy: float,
                     rx: float, ry: float) -> None:
    """Paint a legible analog clock face (10:09) over the toaster dial."""
    draw = ImageDraw.Draw(img, "RGBA")
    # Dark rim, then a warm ivory face.
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                 fill=(238, 232, 214, 255), outline=(28, 28, 28, 255),
                 width=5)
    # Hour ticks.
    for hour in range(12):
        angle = math.radians(hour * 30 - 90)
        inner = 0.82 if hour % 3 == 0 else 0.88
        x1 = cx + rx * inner * math.cos(angle)
        y1 = cy + ry * inner * math.sin(angle)
        x2 = cx + rx * 0.96 * math.cos(angle)
        y2 = cy + ry * 0.96 * math.sin(angle)
        draw.line([x1, y1, x2, y2], fill=(28, 28, 28, 255),
                  width=5 if hour % 3 == 0 else 3)
    # Hands: hour hand toward 10, minute hand toward 9 minutes past.
    for angle_deg, length, width in ((300, 0.50, 7), (54, 0.74, 5)):
        angle = math.radians(angle_deg - 90)
        draw.line([cx, cy,
                   cx + rx * length * math.cos(angle),
                   cy + ry * length * math.sin(angle)],
                  fill=(20, 20, 20, 255), width=width)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(20, 20, 20, 255))


def build() -> Image.Image:
    photo = Image.open(ASSET).convert("RGB")
    # Crop the watermark strip off the bottom.
    w, h = photo.size
    photo = photo.crop((0, 0, w, h - CROP_BOTTOM))
    # Fill the square canvas with the photo itself (mild stretch is
    # invisible on a seamless studio backdrop and keeps one clean
    # background with no pasted-edge seam).
    canvas = photo.resize((SIZE, SIZE), Image.LANCZOS)
    # Scale the dial position into canvas coordinates.
    sx = SIZE / photo.size[0]
    sy = SIZE / photo.size[1]
    paint_clock_face(canvas,
                     DIAL_CX * sx, DIAL_CY * sy,
                     DIAL_R * sx, DIAL_R * sy)
    return canvas


def save_with_gate(img: Image.Image, path: Path) -> Path:
    """Save as PNG, shrinking the payload in steps if over the byte cap.

    The gate demands exactly 1024x1024 and at most 1,048,576 bytes, so
    the dimensions never change: only the encoding is tightened.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    work = img
    for attempt in range(5):
        work.save(path, format="PNG", optimize=True)
        n = path.stat().st_size
        if n <= MAX_BYTES:
            return path
        # Fewer colours compress far better; step down the palette.
        colours = 256 >> attempt
        work = img.convert("P", palette=Image.ADAPTIVE,
                           colors=max(colours, 16)).convert("RGB")
    raise SystemExit(f"gate failed: {path} still "
                     f"{path.stat().st_size} bytes after 5 attempts")


def validate(path: Path) -> None:
    with Image.open(path) as im:
        assert im.format == "PNG", f"not PNG: {im.format}"
        assert im.size == (SIZE, SIZE), f"wrong size: {im.size}"
    n = path.stat().st_size
    assert n <= MAX_BYTES, f"over byte cap: {n} > {MAX_BYTES}"
    print(f"OK {path} {SIZE}x{SIZE} {n} bytes")


def main() -> int:
    out = pick_output_path()
    img = build()
    save_with_gate(img, out)
    validate(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
