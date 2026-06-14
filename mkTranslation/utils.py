# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import re

import requests


def build_params(query, src, dest, token):
    return {
        "client": "webapp",
        "sl": src,
        "tl": dest,
        "hl": dest,
        "dt": ["at", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t"],
        "ie": "UTF-8",
        "oe": "UTF-8",
        "otf": 1,
        "ssel": 0,
        "tsel": 0,
        "tk": token,
        "q": query,
    }


def legacy_format_json(original: str):
    states = []
    text = original
    for i, pos in enumerate(re.finditer('"', text)):
        p = pos.start() + 1
        if i % 2 == 0:
            nxt = text.find('"', p)
            states.append((p, text[p:nxt]))

    while text.find(",,") > -1:
        text = text.replace(",,", ",null,")
    while text.find("[,") > -1:
        text = text.replace("[,", "[null,")

    for i, pos in enumerate(re.finditer('"', text)):
        p = pos.start() + 1
        if i % 2 == 0:
            j = int(i / 2)
            nxt = text.find('"', p)
            text = text[:p] + states[j][1] + text[nxt:]

    return json.loads(text)


def printf(text: str) -> None:
    print(text)


def format_json(original: str):
    try:
        return json.loads(original)
    except ValueError:
        return legacy_format_json(original)


def rshift(val, n):
    return (val % 0x100000000) >> n
