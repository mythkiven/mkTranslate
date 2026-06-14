# -*- coding: utf-8 -*-
"""Normalize language codes across translation backends."""

from __future__ import annotations

GOOGLE_LANG_MAP = {
    "zh-hans": "zh-CN",
    "zh-hant": "zh-TW",
    "zh-cn": "zh-CN",
    "zh-tw": "zh-TW",
    "zh-hk": "zh-TW",
    "zh-mo": "zh-TW",
    "zh-sg": "zh-CN",
    "pt-br": "pt",
    "pt-pt": "pt",
}

YOUDAO_LANG_MAP = {
    "zh-hans": "zh-CHS",
    "zh-hant": "zh-CHT",
    "zh-cn": "zh-CHS",
    "zh-tw": "zh-CHT",
    "en": "EN",
    "ja": "ja",
    "ko": "ko",
    "fr": "fr",
    "de": "de",
    "es": "es",
    "pt": "pt",
    "ru": "ru",
}


def normalize_dest(dest: str) -> str:
    if not dest:
        return "en"
    dest = dest.lower().strip()
    if dest in ("s", "t"):
        return f"zh-han{dest}"
    if dest == "zh-cn":
        return "zh-hans"
    if dest in ("zh-hk", "zh-mo", "zh-sg", "zh-tw"):
        return "zh-hant"
    return dest


def to_google_lang(code: str) -> str:
    code = normalize_dest(code)
    if code in GOOGLE_LANG_MAP:
        return GOOGLE_LANG_MAP[code]
    base = code.split("-")[0]
    if base == "zh":
        return "zh-CN"
    return base


def to_youdao_lang(code: str) -> str:
    code = normalize_dest(code)
    if code in YOUDAO_LANG_MAP:
        return YOUDAO_LANG_MAP[code]
    base = code.split("-")[0]
    if base == "zh":
        return "zh-CHS"
    return base if len(base) > 2 else base.upper()
