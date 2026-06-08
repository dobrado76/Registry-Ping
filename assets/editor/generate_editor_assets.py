"""Generate TEST-Debug Shell toolbar assets (40×40 skins, transparent icons).

Run from repo root::

    venv\\Scripts\\python.exe apps_testing/TEST-debug-shell/assets/editor/generate_editor_assets.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[3]
CORE_EDITOR = REPO_ROOT / "packages" / "lsm_core" / "assets" / "editor"
GENERATE_SKINS = CORE_EDITOR / "generate_button_skins.py"

ICON_TINT = (255, 232, 200, 255)  # #FFE8C8


def _load_skin_drawer():
    import importlib.util

    spec = importlib.util.spec_from_file_location("generate_button_skins", GENERATE_SKINS)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {GENERATE_SKINS}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.draw_button_skin


def _ui() -> dict:
    return json.loads((HERE / "editor_ui.json").read_text(encoding="utf-8"))


def _button_size() -> int:
    ui = _ui()
    return max(1, int(ui.get("button_width", 40)))


def _write_skins(draw_skin) -> None:
    size = _button_size()
    normal = draw_skin(
        size,
        top=(160, 70, 70, 255),
        bottom=(110, 45, 45, 255),
        border=(70, 28, 28, 255),
    )
    hover = draw_skin(
        size,
        top=(210, 95, 55, 255),
        bottom=(170, 70, 40, 255),
        border=(120, 50, 25, 255),
    )
    normal.save(HERE / "button_skin.png")
    hover.save(HERE / "button_skin_hover.png")
    print(f"wrote {size}x{size} button_skin.png, button_skin_hover.png")


def _tint_icon(source: Path, dest: Path) -> None:
    """Recolor glyph pixels only; keep alpha and transparent background."""
    img = Image.open(source).convert("RGBA")
    tr, tg, tb, _ = ICON_TINT
    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a < 24:
                pixels[x, y] = (0, 0, 0, 0)
                continue
            lum = (r * 299 + g * 587 + b * 114) // 1000
            if lum < 48 and a > 200:
                pixels[x, y] = (0, 0, 0, 0)
                continue
            scale = max(0.15, lum / 255.0)
            pixels[x, y] = (
                int(tr * scale),
                int(tg * scale),
                int(tb * scale),
                a,
            )
    img.save(dest)


def _write_icons() -> None:
    icons = _ui().get("icons") or {}
    for _key, filename in icons.items():
        name = Path(str(filename)).name
        core = CORE_EDITOR / name
        if not core.is_file():
            print(f"skip missing core icon: {name}", file=sys.stderr)
            continue
        _tint_icon(core, HERE / name)
        print(f"wrote {name}")


def main() -> None:
    if not CORE_EDITOR.is_dir():
        raise SystemExit(f"core editor assets not found: {CORE_EDITOR}")
    draw_skin = _load_skin_drawer()
    _write_skins(draw_skin)
    _write_icons()


if __name__ == "__main__":
    main()
