# -*- coding: utf-8 -*-
"""Helpers for iOS .strings file values."""

from __future__ import annotations

import re

# Matches a single-line "key" = "value"; entry (supports backslash escapes).
STRINGS_VALUE_PATTERN = re.compile(r'=\s*"((?:[^"\\]|\\.)*)"\s*;')


def unescape_strings_value(value: str) -> str:
    return (
        value.replace(r"\\", "\\")
        .replace(r"\"", '"')
        .replace(r"\n", "\n")
        .replace(r"\t", "\t")
    )


def escape_strings_value(value: str) -> str:
    return (
        value.replace("\\", r"\\")
        .replace('"', r"\"")
        .replace("\n", r"\n")
        .replace("\t", r"\t")
    )


def replace_strings_value(line: str, new_value: str) -> str | None:
    match = STRINGS_VALUE_PATTERN.search(line)
    if not match:
        return None
    escaped = escape_strings_value(new_value)
    return STRINGS_VALUE_PATTERN.sub(f'= "{escaped}";', line, count=1)
