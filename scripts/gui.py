"""Standalone entry for Registry Ping."""

from __future__ import annotations

import customtkinter as ctk

from ui.app import RegistryPingApp


def main() -> None:
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = RegistryPingApp()
    app.mainloop()


if __name__ == "__main__":
    main()
