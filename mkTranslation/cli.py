#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI entry point for mkTranslate 2.0."""

from __future__ import annotations

import argparse
import re

from mkTranslation import utils
from mkTranslation.translator import mkTranslator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Translate iOS .strings, Android strings.xml, and text files."
    )
    parser.add_argument("-t", "--text", dest="text", help="Translate text directly in terminal")
    parser.add_argument("-p", "--path", dest="file_path", help="Path to file to translate")
    parser.add_argument(
        "-d",
        "--dest",
        dest="dest_language",
        default="en",
        help='Target language (default: "en"; 简体:"s"; 繁体:"t")',
    )
    parser.add_argument(
        "-s",
        "--sourcelanguage",
        dest="sourcelanguage",
        help="Source language (recommended for youdao)",
    )
    parser.add_argument(
        "-c",
        "--channel",
        dest="channel",
        default="youdao",
        help='Translation channel: youdao (default), google, or auto',
    )
    parser.add_argument(
        "--names",
        dest="names",
        help="Comma-separated Android string names to translate (xml only)",
    )
    return parser


def normalize_dest_arg(dest_language: str | None) -> str:
    if not dest_language:
        return "en"
    if dest_language in {"s", "t"}:
        return f"zh-han{dest_language}"
    if re.search(r"zh-[HK|MO|SG|TW]", dest_language, re.I):
        return "zh-hant"
    if dest_language.lower() == "zh-cn":
        return "zh-hans"
    return dest_language


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.dest_language = normalize_dest_arg(args.dest_language)
    utils.printf(f"Target language: {args.dest_language}")

    names_filter = None
    if args.names:
        names_filter = {name.strip() for name in args.names.split(",") if name.strip()}

    translator = mkTranslator()
    if args.text:
        translator.translate_text(
            text=args.text,
            destination=args.dest_language,
            sourcelanguage=args.sourcelanguage,
            channel=args.channel,
        )
    elif args.file_path:
        translator.translate_doc(
            filepath=args.file_path,
            destination=args.dest_language,
            sourcelanguage=args.sourcelanguage,
            channel=args.channel,
            names_filter=names_filter,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
