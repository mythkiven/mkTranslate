# -*- coding: utf-8 -*-
"""File encoding helpers for localization files."""

from __future__ import annotations

import codecs


def detect_encoding(path: str) -> str:
    with open(path, "rb") as handle:
        raw = handle.read(4)
    if raw.startswith(codecs.BOM_UTF16_LE) or raw.startswith(codecs.BOM_UTF16_BE):
        return "utf-16"
    if raw.startswith(codecs.BOM_UTF8):
        return "utf-8-sig"
    return "utf-8"


def read_text(path: str) -> str:
    encoding = detect_encoding(path)
    with open(path, "r", encoding=encoding, newline="") as handle:
        return handle.read()


def read_lines(path: str) -> list[str]:
    encoding = detect_encoding(path)
    with open(path, "r", encoding=encoding, newline="") as handle:
        return handle.readlines()


def write_text(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(content)
