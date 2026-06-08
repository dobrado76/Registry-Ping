"""Generate registry_ping_icon.png (radar ping mark on deep teal)."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent / "registry_ping_icon.png"
SIZE = 96
BG = (22, 52, 60, 255)
PING = (61, 214, 198, 255)
RING = (42, 122, 134, 255)


def main() -> None:
    img = Image.new("RGBA", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2

    for radius, width in ((38, 3), (28, 3), (18, 4)):
        draw.ellipse(
            (cx - radius, cy - radius, cx + radius, cy + radius),
            outline=RING,
            width=width,
        )

    for angle in (330, 0, 30):
        rad = math.radians(angle)
        x1 = cx + int(6 * math.cos(rad))
        y1 = cy + int(6 * math.sin(rad))
        x2 = cx + int(40 * math.cos(rad))
        y2 = cy + int(40 * math.sin(rad))
        draw.line((x1, y1, x2, y2), fill=PING, width=5)

    draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=PING)
    draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=(14, 34, 40, 255))

    img.save(OUT)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
