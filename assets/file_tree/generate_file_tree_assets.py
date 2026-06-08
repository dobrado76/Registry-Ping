"""Generate file-tree skins and icons at 40×40 (matches editor toolbar).

Run from repo root::

    venv\\Scripts\\python.exe packages/lsm_core/assets/file_tree/generate_file_tree_assets.py
"""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
UI_PATH = HERE / "file_tree_ui.json"
ICON_RGBA = (245, 230, 216, 255)


def _read_ui() -> dict:
    if UI_PATH.is_file():
        raw = json.loads(UI_PATH.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else {}
    return {}


def _size(key: str, default: int) -> int:
    return max(1, int(_read_ui().get(key, default)))


def draw_button_skin(
    size: int,
    *,
    top: tuple[int, int, int, int],
    bottom: tuple[int, int, int, int],
    border: tuple[int, int, int, int],
) -> Image.Image:
    radius = max(4, size // 6)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    body = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(body)
    for y in range(size):
        t = y / max(1, size - 1)
        color = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(4))
        bdraw.line([(0, y), (size - 1, y)], fill=color)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    img = Image.composite(body, img, mask)
    ImageDraw.Draw(img).rounded_rectangle(
        (0, 0, size - 1, size - 1), radius=radius, outline=border, width=1
    )
    return img


def _canvas(size: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def _stroke() -> int:
    return max(3, _size("button_width", 40) // 10)


def icon_plus(size: int) -> Image.Image:
    img, d = _canvas(size)
    m = size // 2
    w = _stroke()
    d.line([(m, size // 5), (m, size - size // 5)], fill=ICON_RGBA, width=w)
    d.line([(size // 5, m), (size - size // 5, m)], fill=ICON_RGBA, width=w)
    return img


def icon_folder_btn(size: int) -> Image.Image:
    img, d = _canvas(size)
    pad = size // 5
    tab_h = size // 6
    d.rounded_rectangle(
        (pad, pad + tab_h, size - pad, size - pad),
        radius=4,
        outline=ICON_RGBA,
        width=_stroke(),
    )
    d.rectangle((pad, pad, pad + size // 2, pad + tab_h + 2), fill=ICON_RGBA)
    return img


def icon_import(size: int) -> Image.Image:
    img, d = _canvas(size)
    w = _stroke()
    cx = size // 2
    d.line([(cx, size // 6), (cx, size // 2)], fill=ICON_RGBA, width=w)
    d.polygon(
        [(cx - size // 5, size // 2 - 2), (cx + size // 5, size // 2 - 2), (cx, size // 2 + size // 6)],
        fill=ICON_RGBA,
    )
    d.line([(size // 5, size - size // 5), (size - size // 5, size - size // 5)], fill=ICON_RGBA, width=w)
    return img


def icon_rename(size: int) -> Image.Image:
    img, d = _canvas(size)
    w = _stroke()
    d.line(
        [(size // 4, size - size // 4), (size - size // 5, size // 5)],
        fill=ICON_RGBA,
        width=w,
    )
    d.polygon(
        [
            (size - size // 5, size // 5),
            (size - size // 8, size // 5 + size // 10),
            (size - size // 5 + size // 10, size // 8),
        ],
        fill=ICON_RGBA,
    )
    return img


def icon_delete(size: int) -> Image.Image:
    img, d = _canvas(size)
    w = _stroke()
    m = size // 2
    r = size // 3
    d.line([(m - r, m - r), (m + r, m + r)], fill=ICON_RGBA, width=w)
    d.line([(m + r, m - r), (m - r, m + r)], fill=ICON_RGBA, width=w)
    return img


def icon_download(size: int) -> Image.Image:
    img, d = _canvas(size)
    w = _stroke()
    cx = size // 2
    d.line([(cx, size // 6), (cx, size // 2)], fill=ICON_RGBA, width=w)
    d.polygon(
        [(cx - size // 5, size // 2), (cx + size // 5, size // 2), (cx, size // 2 + size // 5)],
        fill=ICON_RGBA,
    )
    d.line([(size // 5, size - size // 6), (size - size // 5, size - size // 6)], fill=ICON_RGBA, width=w)
    return img


def icon_zip(size: int) -> Image.Image:
    img, d = _canvas(size)
    pad = size // 5
    d.rounded_rectangle(
        (pad, pad, size - pad, size - pad),
        radius=4,
        outline=ICON_RGBA,
        width=_stroke(),
    )
    mid = size // 2
    for y in (mid - size // 8, mid, mid + size // 8):
        d.line([(mid - size // 10, y), (mid + size // 10, y)], fill=ICON_RGBA, width=2)
    return img


def icon_folder_tree(size: int) -> Image.Image:
    img, d = _canvas(size)
    pad = max(4, size // 8)
    tab = max(5, size // 7)
    body = (200, 160, 100, 255)
    tab_fill = (180, 140, 90, 255)
    d.rounded_rectangle((pad, pad + tab, size - pad, size - pad), radius=4, fill=body)
    d.rectangle((pad, pad, pad + size // 2, pad + tab), fill=tab_fill)
    return img


def icon_file_tree(size: int) -> Image.Image:
    img, d = _canvas(size)
    pad = max(4, size // 8)
    d.rounded_rectangle(
        (pad, pad + 2, size - pad, size - pad),
        radius=3,
        fill=(70, 70, 78, 255),
        outline=(200, 180, 150, 255),
        width=2,
    )
    fold = size // 5
    d.polygon(
        [(size - pad - fold, pad + 2), (size - pad, pad + 2), (size - pad, pad + 2 + fold)],
        fill=(200, 180, 150, 255),
    )
    d.rectangle(
        (pad + 3, pad + size // 3, size - pad - 4, pad + size // 3 + max(3, size // 12)),
        fill=(200, 160, 120, 255),
    )
    return img


def main() -> None:
    btn_size = _size("button_width", 40)
    tree_size = _size("tree_icon_size", 40)

    normal = draw_button_skin(
        btn_size,
        top=(140, 58, 58, 255),
        bottom=(100, 40, 40, 255),
        border=(70, 28, 28, 255),
    )
    hover = draw_button_skin(
        btn_size,
        top=(168, 72, 72, 255),
        bottom=(120, 50, 50, 255),
        border=(85, 35, 35, 255),
    )
    normal.save(HERE / "button_skin.png")
    hover.save(HERE / "button_skin_hover.png")

    toolbar = {
        "btn_new_file.png": icon_plus(btn_size),
        "btn_new_folder.png": icon_folder_btn(btn_size),
        "btn_import.png": icon_import(btn_size),
        "btn_rename.png": icon_rename(btn_size),
        "btn_delete.png": icon_delete(btn_size),
        "btn_download.png": icon_download(btn_size),
        "btn_zip.png": icon_zip(btn_size),
    }
    for name, im in toolbar.items():
        im.save(HERE / name)

    tree = {
        "icon_folder.png": icon_folder_tree(tree_size),
        "icon_file.png": icon_file_tree(tree_size),
    }
    for name, im in tree.items():
        im.save(HERE / name)

    print(f"wrote {btn_size}px toolbar + {tree_size}px tree icons under {HERE}")


if __name__ == "__main__":
    main()
