"""Chinese font registration helpers."""

from __future__ import annotations

import os

from kivy.core.text import LabelBase

FONT_NAME = "ChineseFont"

FONT_PATHS = [
    "C:/Windows/Fonts/msyh.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "assets/fonts/msyh.ttc",
    "assets/fonts/simhei.ttf",
    "assets/fonts/simsun.ttc",
    "assets/fonts/NotoSansSC-Regular.otf",
    "assets/fonts/NotoSansSC-Regular.ttf",
]

_found_font = None
_registered = False


def find_chinese_font():
    """Return the first available Chinese font path."""
    global _found_font
    if _found_font:
        return _found_font

    for path in FONT_PATHS:
        if os.path.exists(path):
            _found_font = path
            return path
    return None


def register_chinese_font():
    """Register the Chinese font alias used by the app."""
    global _registered
    if _registered:
        return True

    font_path = find_chinese_font()
    if not font_path:
        print("[Font] Chinese font not found. Chinese text may not render correctly.")
        return False

    try:
        LabelBase.register(name=FONT_NAME, fn_regular=font_path)
        _registered = True
        print(f"[Font] Registered {FONT_NAME} from {font_path}")
        return True
    except Exception as exc:
        print(f"[Font] Failed to register {FONT_NAME}: {exc}")
        return False


def get_font_name():
    """Return the registered font alias when available."""
    return FONT_NAME if _registered else None
