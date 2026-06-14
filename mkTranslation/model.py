# -*- coding: utf-8 -*-

from __future__ import annotations


class Translated:
    def __init__(self, src, dest, origin, text, pronunciation, extra_data=None):
        self.src = src
        self.dest = dest
        self.origin = origin
        self.text = text
        self.pronunciation = pronunciation
        self.extra_data = extra_data

    def __str__(self) -> str:
        return (
            f"Translated(src={self.src}, dest={self.dest}, text={self.text}, "
            f"pronunciation={self.pronunciation})"
        )


class Detected:
    def __init__(self, lang, confidence):
        self.lang = lang
        self.confidence = confidence

    def __str__(self) -> str:
        return f"Detected(lang={self.lang}, confidence={self.confidence})"
