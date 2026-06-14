# -*- coding: UTF-8 -*-
"""Youdao translation with fixed signing and clearer errors."""

from __future__ import annotations

import hashlib
import random
import time

import requests
from requests.exceptions import RequestException

from mkTranslation import utils
from mkTranslation.lang_utils import to_youdao_lang

_SESSION = requests.Session()
_SIGN_SALT = "rY0D^0'nM0}g5Mm1z%1G4"


class mkYouDaoTranslator:
    def __init__(self):
        self.headers2 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://fanyi.youdao.com/",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        self.headers1 = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Origin": "https://ai.youdao.com",
            "Referer": "https://ai.youdao.com/",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        self.url2 = "https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"
        self.url1 = "https://aidemo.youdao.com/trans"

    def translate(self, text: str, dest: str, src: str | None) -> str:
        if not text:
            return ""
        time.sleep(0.1)
        dest_code = to_youdao_lang(dest)
        src_code = to_youdao_lang(src) if src else "AUTO"
        for method in (self._trans1, self._trans2, self._trans3):
            try:
                result = method(text, dest_code, src_code)
                if result:
                    return result
            except Exception:
                continue
        raise RuntimeError("Youdao translation failed for this text.")

    def _trans1(self, text: str, dest: str, src: str) -> str:
        _SESSION.get(self.url1, timeout=20)
        response = _SESSION.post(
            self.url1,
            headers=self.headers1,
            data={
                "q": text,
                "from": src if src and src != "AUTO" else "auto",
                "to": dest.lower() if len(dest) == 2 else dest,
            },
            timeout=20,
        )
        payload = response.json()
        translation = payload.get("translation")
        if translation:
            return translation[0]
        raise KeyError("translation")

    def _trans2(self, text: str, dest: str, src: str) -> str:
        _SESSION.get("https://fanyi.youdao.com/", timeout=20)
        salt = str(int(time.time() * 1000) + random.randint(0, 9))
        sign_input = f"fanyideskweb{text}{salt}{_SIGN_SALT}"
        sign = hashlib.md5(sign_input.encode("utf-8")).hexdigest()
        response = _SESSION.post(
            self.url2,
            headers=self.headers2,
            data={
                "i": text,
                "from": src or "AUTO",
                "to": dest,
                "smartresult": "dict",
                "client": "fanyideskweb",
                "salt": salt,
                "sign": sign,
                "doctype": "json",
                "version": "2.1",
                "keyfrom": "fanyi.web",
                "action": "FY_BY_DEFAULT",
                "typoResult": "false",
            },
            timeout=20,
        )
        payload = response.json()
        return payload["translateResult"][0][0]["tgt"]

    def _trans3(self, text: str, dest: str, src: str) -> str:
        utils.printf("Using legacy Youdao endpoint (zh/en only).")
        response = requests.get(
            "https://fanyi.youdao.com/openapi.do",
            params={
                "keyfrom": "woodcol",
                "key": "1522180019",
                "type": "data",
                "doctype": "json",
                "version": "1.1",
                "q": text,
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        return payload["translation"][0]
