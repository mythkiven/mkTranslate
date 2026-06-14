# -*- coding: utf-8 -*-
"""Core translation orchestration for strings, xml, and text files."""

from __future__ import annotations

import json
import os
import re
import sys
import xml.etree.ElementTree as ET

import requests

from mkTranslation import network, utils
from mkTranslation.io_utils import read_lines, write_text
from mkTranslation.lang_utils import normalize_dest
from mkTranslation.translate_chinese import mkConverter
from mkTranslation.translate_google import mkGoogleTranslator
from mkTranslation.translate_youdao import mkYouDaoTranslator

pathSeparator = os.sep
STRINGS_PATTERN = re.compile(r'=\s*"(.+?)"\s*;')


class mkTranslator:
    def get_file(self, path: str) -> str:
        if os.path.exists(path):
            return path
        file_name = os.path.basename(path)
        return os.path.join(os.path.abspath("."), file_name)

    def translate_i18ns(self, dest: str, word: str, language: str | None) -> str:
        if not language:
            return "null"
        uri = "https://i18ns.com/translate/_search"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Basic aTE4bnM6KioqKioq",
            "user-agent": "mkTranslate/2.0",
        }
        body = json.dumps(
            {
                "query": {
                    "simple_query_string": {
                        "query": word,
                        "fields": [f"translations.{language}"],
                        "minimum_should_match": "100%",
                        "default_operator": "AND",
                        "analyzer": "smartcn",
                    }
                }
            }
        )
        try:
            response = requests.post(url=uri, data=body, headers=headers, timeout=120)
            if response.status_code != 200:
                return "null"
            payload = response.json()
            translations = payload["hits"]["hits"][0]["_source"]["translations"]
        except Exception:
            return "null"

        if len(translations) <= 1:
            return "null"

        source_values = [
            json.dumps(item[language], ensure_ascii=False)
            .replace("[", "")
            .replace("]", "")
            .replace('"', "")
            for item in translations
            if language in item
        ]
        if word not in source_values:
            return "null"

        for item in translations:
            if dest in item:
                utils.printf(
                    f"use 'https://i18ns.com/' translation {word} to {item[dest][0]}"
                )
                return str(item[dest][0])
        return "null"

    def translate(self, word: str, destination: str, language: str | None, channel: str) -> str:
        if not word:
            return ""
        destination = normalize_dest(destination)

        try:
            cached = self.translate_i18ns(destination, word, language)
            if cached != "null":
                return cached
        except Exception:
            pass

        if destination == "zh-hant":
            return mkConverter("zh-hant").convert(word)
        if destination == "zh-hans":
            return mkConverter("zh-hans").convert(word)

        if channel == "google":
            return self._translate_with_channel(word, destination, language, "google")
        return self._translate_with_channel(word, destination, language, "youdao")

    def _translate_with_channel(
        self,
        word: str,
        destination: str,
        language: str | None,
        channel: str,
    ) -> str:
        alternate = "google" if channel == "youdao" else "youdao"
        for current in (channel, alternate):
            try:
                if current == "google":
                    return mkGoogleTranslator().translate(
                        word, dest=destination, src=language or "auto"
                    ).text
                return mkYouDaoTranslator().translate(word, destination, language)
            except Exception as exc:
                utils.printf(f"{current} translation failed: {exc}")
        raise RuntimeError(f"Translation failed for: {word[:80]}")

    def fix_tx(self, txt: str) -> str:
        if "% ld" in txt or "% @" in txt:
            match = re.search(r"%\s*(@|ld)\s*/\s*%\s*(ld|@)", txt)
            if match:
                fixed = match.group(0).replace(" ", "")
                txt = txt.replace(match.group(0), fixed)
        return txt

    def _should_translate_name(self, name: str | None, names_filter: set[str] | None) -> bool:
        if not names_filter:
            return True
        return bool(name and name in names_filter)

    def _element_text(self, element: ET.Element) -> str:
        parts = [element.text or ""]
        for child in list(element):
            if child.text:
                parts.append(child.text)
            if child.tail:
                parts.append(child.tail)
        return "".join(parts).strip()

    def _set_element_text(self, element: ET.Element, value: str) -> None:
        for child in list(element):
            element.remove(child)
        element.text = value

    def translate_xml(
        self,
        filepath: str,
        newfile: str,
        destination: str,
        sourcelanguage: str | None,
        channel: str,
        names_filter: set[str] | None = None,
    ) -> None:
        tree = ET.parse(filepath)
        root = tree.getroot()
        for element in root.iter("string"):
            name = element.attrib.get("name")
            if not self._should_translate_name(name, names_filter):
                utils.printf(f"skip name={name}")
                continue
            original = self._element_text(element)
            if not original:
                utils.printf(f"skip empty string name={name}")
                continue
            utils.printf(f"original[{name}]: {original}")
            translated = self.translate(original, destination, sourcelanguage, channel)
            translated = self.fix_tx(translated)
            self._set_element_text(element, translated)
            utils.printf(f"translated[{name}]: {translated}")
            utils.printf("-----")

        if hasattr(ET, "indent"):
            ET.indent(tree, space="    ")
        tree.write(newfile, encoding="utf-8", xml_declaration=True)

    def translate_strings(
        self,
        filepath: str,
        newfile: str,
        destination: str,
        sourcelanguage: str | None,
        channel: str,
    ) -> None:
        lines_out: list[str] = []
        for raw_line in read_lines(filepath):
            line = raw_line.rstrip("\n")
            if not line.strip():
                lines_out.append(raw_line)
                continue

            origin_line = line
            utils.printf(f"original:{origin_line}")
            match = STRINGS_PATTERN.search(line)
            if match:
                translated = self.translate(match.group(1), destination, sourcelanguage, channel)
                if translated:
                    origin_line = STRINGS_PATTERN.sub(f'="{translated}"', line, count=1)
                else:
                    utils.printf(f"translate fail: {match.group(1)}")
            else:
                utils.printf(f"skip: {origin_line}")

            origin_line = self.fix_tx(origin_line)
            utils.printf(f"translated:{origin_line}")
            lines_out.append(origin_line + "\n")
            utils.printf("-----")

        write_text(newfile, "".join(lines_out))

    def translate_text_file(
        self,
        filepath: str,
        newfile: str,
        destination: str,
        sourcelanguage: str | None,
        channel: str,
    ) -> None:
        lines_out: list[str] = []
        for raw_line in read_lines(filepath):
            line = raw_line.rstrip("\n")
            if not line:
                lines_out.append("\n")
                continue
            utils.printf(f"original:{line}")
            translated = self.translate(line, destination, sourcelanguage, channel)
            translated = self.fix_tx(translated)
            utils.printf(f"translated:{translated}")
            lines_out.append(translated + "\n")
            utils.printf("-----")
        write_text(newfile, "".join(lines_out))

    def log(self, channel: str, dest: str) -> None:
        if dest in {"zh-hant", "zh-hans"}:
            return
        if channel == "None":
            utils.printf("[No network, no translation!]")
            sys.exit(1)
        if channel == "google":
            utils.printf("[Use google translation]")
        else:
            utils.printf("[Use youdao translation]")

    def translate_text(
        self,
        text: str,
        destination: str,
        sourcelanguage: str | None,
        channel: str,
    ) -> None:
        channel = network.select_network(channel)
        destination = normalize_dest(destination)
        self.log(channel, destination)
        if channel == "google":
            utils.printf(mkGoogleTranslator().translate(text, dest=destination).text)
        else:
            utils.printf(mkYouDaoTranslator().translate(text, destination, sourcelanguage))

    def translate_doc(
        self,
        filepath: str,
        destination: str,
        sourcelanguage: str | None,
        channel: str,
        names_filter: set[str] | None = None,
    ) -> None:
        channel = network.select_network(channel)
        destination = normalize_dest(destination)
        self.log(channel, destination)

        filepath = self.get_file(filepath)
        old_file_name = os.path.basename(filepath)
        file_type = old_file_name.rsplit(".", 1)[-1].lower()
        current_path = os.path.dirname(filepath) or os.path.abspath(".")

        if destination in {"zh-hant", "zh-hans"}:
            new_file = os.path.join(current_path, f"translate_{destination}_{old_file_name}")
        else:
            new_file = os.path.join(current_path, f"translate_{destination}_by_{channel}_{old_file_name}")

        utils.printf("translating..")
        if file_type in {"text", "txt"}:
            self.translate_text_file(filepath, new_file, destination, sourcelanguage, channel)
        elif file_type == "strings":
            self.translate_strings(filepath, new_file, destination, sourcelanguage, channel)
        elif file_type == "xml":
            self.translate_xml(
                filepath,
                new_file,
                destination,
                sourcelanguage,
                channel,
                names_filter=names_filter,
            )
        else:
            self.translate_text_file(filepath, new_file, destination, sourcelanguage, channel)

        utils.printf(f"translation completed,file saved in [{new_file}]")
