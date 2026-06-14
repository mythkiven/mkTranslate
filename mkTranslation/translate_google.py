# -*- coding: utf-8 -*-
"""Google translation via deep-translator with optional Cloud API."""

from __future__ import annotations

import os
from typing import Optional

import requests

from mkTranslation.lang_utils import to_google_lang
from mkTranslation.model import Detected, Translated


class mkGoogleTranslator:
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.api_key = os.getenv("GOOGLE_TRANSLATE_API_KEY", "").strip()

    def translate(self, text: str, dest: str = "en", src: str = "auto") -> Translated:
        if isinstance(text, list):
            return [self.translate(item, dest=dest, src=src) for item in text]

        dest_lang = to_google_lang(dest)
        src_lang = "auto" if not src or src == "auto" else to_google_lang(src)
        translated = self._translate_text(text, dest_lang, src_lang)
        return Translated(
            src=src_lang,
            dest=dest_lang,
            origin=text,
            text=translated,
            pronunciation=text,
        )

    def translate_text(self, text: str, dest: str = "en") -> Translated:
        return self.translate(text, dest=dest, src="auto")

    def detect(self, text: str) -> Detected:
        result = self.translate(text, dest="en", src="auto")
        return Detected(lang=result.src, confidence=1.0)

    def _translate_text(self, text: str, dest: str, src: str) -> str:
        if self.api_key:
            cloud = self._translate_cloud(text, dest, src)
            if cloud:
                return cloud

        try:
            from deep_translator import GoogleTranslator

            translator = GoogleTranslator(source=src, target=dest, timeout=self.timeout)
            return translator.translate(text)
        except Exception as exc:
            raise RuntimeError(
                "Google translation failed. Try `-c youdao` or set GOOGLE_TRANSLATE_API_KEY."
            ) from exc

    def _translate_cloud(self, text: str, dest: str, src: str) -> Optional[str]:
        params = {
            "q": text,
            "target": dest,
            "format": "text",
            "key": self.api_key,
        }
        if src and src != "auto":
            params["source"] = src
        response = requests.post(
            "https://translation.googleapis.com/language/translate/v2",
            data=params,
            timeout=self.timeout,
        )
        if response.status_code != 200:
            return None
        payload = response.json()
        return payload["data"]["translations"][0]["translatedText"]
