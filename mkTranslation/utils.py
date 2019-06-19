# -*- coding: utf-8 -*-
from __future__ import print_function
import json
import ast
import sys
import requests


try:
    from urllib.parse import quote
except:
    from urllib import quote

PY3 = sys.version_info > (3, )
unicode = str if PY3 else unicode

def build_params(query, src, dest, token):
    params = {
        'client': 'webapp',
        'sl': src,
        'tl': dest,
        'hl': dest,
        'dt': ['at', 'bd', 'ex', 'ld', 'md', 'qca', 'rw', 'rm', 'ss', 't'],
        'ie': 'UTF-8',
        'oe': 'UTF-8',
        'otf': 1,
        'ssel': 0,
        'tsel': 0,
        'tk': token,
        'q': query,
    }
    return params


def legacy_format_json(original):
    states = []
    text = original
    for i, pos in enumerate(re.finditer('"', text)):
        p = pos.start() + 1
        if i % 2 == 0:
            nxt = text.find('"', p)
            states.append((p, text[p:nxt]))

    while text.find(',,') > -1:
        text = text.replace(',,', ',null,')
    while text.find('[,') > -1:
        text = text.replace('[,', '[null,')

    for i, pos in enumerate(re.finditer('"', text)):
        p = pos.start() + 1
        if i % 2 == 0:
            j = int(i / 2)
            nxt = text.find('"', p)
            text = text[:p] + states[j][1] + text[nxt:]

    converted = json.loads(text)
    return converted


def format_json(original):
    try:
        converted = json.loads(original)
    except ValueError:
        converted = legacy_format_json(original)
    return converted


def rshift(val, n):
    return (val % 0x100000000) >> n
