"""Registry Ping — community registry smoke test for shared LSM UI primitives."""

from __future__ import annotations

import tkinter as tk
import types
from pathlib import Path

import customtkinter as ctk
from tkinter import messagebox

import config  # noqa: F401 — registers lsm_core runtime provider
from config import ENGINE_CONFIG, ROOT_DIR
from lsm_core.ui.code_editor import CodeEditorPanel
from lsm_core.ui.developer_console import DeveloperConsoleFrame, TelemetryStatusBar
from lsm_core.ui.file_tree import FileTreeFeatures, FileTreeWidget
from lsm_core.ui.file_tree_model import editor_mode_for_path, editable_suffixes_from_filters
from lsm_core.ui.prose_lint_settings import ProseLintSettingsDialog, ProseLintSettingsSpec

_DATA_DIR = ROOT_DIR / "data"
_TREE_FILTERS = ("*.txt", "*.tex", "*.json", "*.html", "*.dat")
_EDITABLE_SUFFIXES = editable_suffixes_from_filters(_TREE_FILTERS)


class RegistryPingFrame(ctk.CTkFrame):
    """File tree + mode-aware editor harness (shared lsm_core widgets)."""

    def __init__(self, master, *, embedded: bool = False, on_close=None):
        super().__init__(master, fg_color="transparent")
        self.embedded = embedded
        self.on_close = on_close
        self._current_file: Path | None = None
        self._editor_panel: CodeEditorPanel | None = None

        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(self, fg_color="#142A32", corner_radius=8)
        header.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header,
            text="Registry Ping — GitHub install + Studio embedding smoke test",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#A8F0E8",
        ).grid(row=0, column=0, sticky="w", padx=12, pady=(10, 2))
        ctk.CTkLabel(
            header,
            text=(
                "Filters: .txt, .tex, .json, .html, .dat — "
                "ignored.exe is hidden; .dat and folders have no editor."
            ),
            font=ctk.CTkFont(size=12),
            text_color="#7EC8BE",
        ).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 10))

        btn_row = ctk.CTkFrame(header, fg_color="transparent")
        btn_row.grid(row=0, column=1, rowspan=2, padx=12, pady=8)
        ctk.CTkButton(
            btn_row,
            text="Prose Lint Settings…",
            width=160,
            fg_color="#2A7A86",
            hover_color="#3A9AA8",
            command=self._open_prose_settings,
        ).pack(side="left", padx=4)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew", padx=8, pady=4)
        body.grid_rowconfigure(0, weight=1)
        body.grid_columnconfigure(0, weight=1)

        self._paned = tk.PanedWindow(
            body,
            orient=tk.HORIZONTAL,
            sashwidth=6,
            sashrelief=tk.RAISED,
            opaqueresize=True,
            bg="#333333",
            bd=0,
        )
        self._paned.grid(row=0, column=0, sticky="nsew")

        left = ctk.CTkFrame(self._paned, fg_color="#0F1F24", width=280)
        right = ctk.CTkFrame(self._paned, fg_color="transparent")
        self._paned.add(left, minsize=200, width=280)
        self._paned.add(right, minsize=360)

        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            left,
            text="Project files",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#A8E8DC",
        ).grid(row=0, column=0, sticky="w", padx=8, pady=(8, 4))

        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._file_tree = FileTreeWidget(
            left,
            root_path=_DATA_DIR,
            app_root=ROOT_DIR,
            filters=_TREE_FILTERS,
            features=FileTreeFeatures(
                new_file=True,
                new_folder=True,
                import_files=True,
                drag_drop=True,
                delete=True,
                rename=True,
                download=True,
                default_new_file_suffix=".tex",
            ),
            on_select=self._on_tree_select,
        )
        self._file_tree.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 8))

        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)
        self._editor_host = ctk.CTkFrame(right, fg_color="transparent")
        self._editor_host.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)
        self._editor_host.grid_rowconfigure(0, weight=1)
        self._editor_host.grid_columnconfigure(0, weight=1)

        self._placeholder = ctk.CTkLabel(
            self._editor_host,
            text="Select a .txt, .tex, .json, or .html file to edit.",
            font=ctk.CTkFont(size=14),
            text_color="#888888",
        )
        self._placeholder.grid(row=0, column=0, sticky="nsew")

        self._lint_engine = types.SimpleNamespace(adv_dir=str(ROOT_DIR / "configs"))

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="nsew", padx=8, pady=(4, 8))
        footer.grid_rowconfigure(1, weight=1)
        footer.grid_columnconfigure(0, weight=1)
        self._telemetry = TelemetryStatusBar(
            footer,
            app_id="registry_ping",
            initial_text="Registry Ping ready — community install OK.",
        )
        self._telemetry.grid(row=0, column=0, sticky="ew", pady=(0, 4))
        self._console = DeveloperConsoleFrame(
            footer,
            app_id="registry_ping",
            intro="Registry Ping — telemetry console (shared lsm_core widget).\n",
        )
        self._console.grid(row=1, column=0, sticky="nsew")

    def _prose_lint_config(self) -> dict:
        return {
            "get_engine": lambda: self._lint_engine,
            "is_enabled": lambda: bool(ENGINE_CONFIG.get("offline_spell_check", True)),
            "is_grammar_enabled": lambda: bool(
                ENGINE_CONFIG.get("offline_grammar_check", True)
            ),
            "is_synonyms_enabled": lambda: bool(ENGINE_CONFIG.get("offline_synonyms", False)),
        }

    def _clear_editor(self) -> None:
        if self._editor_panel is not None:
            self._editor_panel.destroy()
            self._editor_panel = None
        self._placeholder.grid(row=0, column=0, sticky="nsew")

    def _show_placeholder(self, message: str) -> None:
        self._clear_editor()
        self._placeholder.configure(text=message)
        self._placeholder.grid(row=0, column=0, sticky="nsew")

    def _on_tree_select(self, path: Path | None, is_dir: bool) -> None:
        self._current_file = path
        if path is None:
            self._show_placeholder("Select a .txt, .tex, .json, or .html file to edit.")
            self._telemetry.set_status("No selection.")
            return
        if is_dir:
            self._show_placeholder(f"Folder “{path.name}” — select a file to edit.")
            self._telemetry.set_status(f"Folder: {path.relative_to(_DATA_DIR)}")
            return

        mode = editor_mode_for_path(path, editable_suffixes=_EDITABLE_SUFFIXES)
        if mode is None:
            self._show_placeholder(
                f"“{path.name}” is listed but not editable (.dat has no text editor)."
            )
            self._telemetry.set_status(f"Not editable: {path.name}")
            return

        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Open file", str(exc), parent=self)
            return

        self._clear_editor()
        self._placeholder.grid_remove()
        validate = mode in ("json", "html", "latex")
        self._editor_panel = CodeEditorPanel(
            self._editor_host,
            mode=mode,
            show_gutter=True,
            show_line_col=True,
            show_status=True,
            show_toolbar=True,
            app_root=ROOT_DIR,
            validation=validate,
            prose_lint=self._prose_lint_config(),
            initial_status=f"{mode} — {path.name}",
        )
        self._editor_panel.grid(row=0, column=0, sticky="nsew")
        self._editor_panel.set_text(text)
        rel = path.relative_to(_DATA_DIR)
        self._telemetry.set_status(f"Editing {rel} ({mode})")

    def _open_prose_settings(self) -> None:
        spec = ProseLintSettingsSpec(
            intro_text="Registry Ping prose lint toggles (shared lsm_core dialog).",
            lexicon_text=(
                f"Test lexicon: {ROOT_DIR / 'configs' / 'spelling_lexicon.json'}\n"
                "(Add words via editor right-click when spell check is on.)"
            ),
            include_scope=True,
        )
        locale_labels = {
            "american": "American",
            "british": "British",
            "both": "Both Allowed",
        }
        scope_labels = {"story": "Registry Ping", "global": "Global"}
        ProseLintSettingsDialog(
            self.winfo_toplevel(),
            engine_config=ENGINE_CONFIG,
            save_engine_config=self._save_engine_config,
            locale_labels=locale_labels,
            scope_labels=scope_labels,
            spec=spec,
        )

    def _save_engine_config(self, updates: dict) -> None:
        ENGINE_CONFIG.update(updates)
        try:
            import json

            path = ROOT_DIR / "configs" / "engine_config.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(ENGINE_CONFIG, indent=2), encoding="utf-8")
        except OSError:
            pass
        self._telemetry.set_status("Prose lint settings updated.")

    def prepare_to_close(self) -> bool:
        return True

    def _on_closing(self) -> None:
        if callable(self.on_close):
            self.on_close()
        elif not self.embedded:
            self.destroy()


class RegistryPingApp(ctk.CTk):
    """Standalone window wrapper (direct ``scripts/gui.py`` launch)."""

    def __init__(self):
        super().__init__()
        self.title("Registry Ping")
        self.geometry("1100x720")
        self.minsize(800, 520)
        frame = RegistryPingFrame(self, embedded=False, on_close=self.destroy)
        frame.pack(fill="both", expand=True)
        self.protocol("WM_DELETE_WINDOW", frame._on_closing)
