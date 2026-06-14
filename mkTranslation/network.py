# -*- coding: utf-8 -*-
"""Network channel selection."""

from __future__ import annotations

import os
import subprocess
import sys


def _ping(host: str) -> bool:
    if sys.platform == "win32":
        cmd = ["ping", host, "-n", "1"]
        sink = "NUL"
    else:
        cmd = ["ping", "-c", "1", host]
        sink = "/dev/null"
    try:
        return subprocess.call(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ) == 0
    except OSError:
        return False


def select_network(channel: str | None) -> str:
    """Return a translation channel, honoring explicit user choice."""
    if channel:
        normalized = channel.strip().lower()
        if normalized in {"google", "youdao"}:
            return normalized
        if normalized == "auto":
            pass
        elif normalized not in {"", "none"}:
            return normalized

    env_channel = os.getenv("MKTRANSLATE_CHANNEL", "").strip().lower()
    if env_channel in {"google", "youdao"}:
        return env_channel

    if _ping("translate.google.com"):
        return "google"
    if _ping("youdao.com"):
        return "youdao"
    return "youdao"
