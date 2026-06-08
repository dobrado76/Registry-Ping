"""Minimal config for the Registry Ping community sample app."""

from __future__ import annotations

import json
from pathlib import Path

from lsm_core.config import runtime as lsm_runtime
from lsm_core.prose import spell_check as _spell_check

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIGS_DIR = ROOT_DIR / "configs"
_ENGINE_PATH = CONFIGS_DIR / "engine_config.json"

_DEFAULT_ENGINE: dict = {
    "ui_scaling": 1.0,
    "offline_spell_check": True,
    "offline_grammar_check": True,
    "offline_synonyms": False,
    "spelling_locale": "american",
    "custom_dictionary_scope": "story",
}


def _load_engine_config() -> dict:
    if _ENGINE_PATH.is_file():
        try:
            raw = json.loads(_ENGINE_PATH.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                merged = dict(_DEFAULT_ENGINE)
                merged.update(raw)
                return merged
        except (OSError, json.JSONDecodeError):
            pass
    return dict(_DEFAULT_ENGINE)


ENGINE_CONFIG = _load_engine_config()
lsm_runtime.set_engine_config_provider(lambda: ENGINE_CONFIG)
_spell_check.set_lexicon_paths(
    global_path=lambda: CONFIGS_DIR / "spelling_lexicon_global.json",
    universe_path=None,
)
