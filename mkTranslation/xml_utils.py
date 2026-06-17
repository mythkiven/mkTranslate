# -*- coding: utf-8 -*-
"""Android strings.xml translation helpers."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from collections.abc import Callable


def element_visible_text(element: ET.Element) -> str:
    parts: list[str] = []
    if element.text:
        parts.append(element.text)
    for child in element:
        if child.text:
            parts.append(child.text)
        if child.tail:
            parts.append(child.tail)
    return "".join(parts).strip()


def translate_element_preserving_markup(
    element: ET.Element,
    translate_fn: Callable[[str], str],
) -> None:
    """Translate text nodes in place, keeping child tags (e.g. <font>)."""
    if element.text and element.text.strip():
        element.text = translate_fn(element.text.strip())

    for child in element:
        if list(child):
            translate_element_preserving_markup(child, translate_fn)
        elif child.text and child.text.strip():
            child.text = translate_fn(child.text.strip())
        if child.tail and child.tail.strip():
            child.tail = translate_fn(child.tail.strip())
