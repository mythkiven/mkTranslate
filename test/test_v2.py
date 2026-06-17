import os
import tempfile
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

from mkTranslation.io_utils import detect_encoding, write_text
from mkTranslation.lang_utils import normalize_dest, to_google_lang
from mkTranslation.network import select_network
from mkTranslation.strings_utils import escape_strings_value, replace_strings_value, unescape_strings_value
from mkTranslation.translate_chinese import mkConverter
from mkTranslation.translator import mkTranslator
from mkTranslation.xml_utils import element_visible_text, translate_element_preserving_markup


class LangUtilsTest(unittest.TestCase):
    def test_normalize_dest_aliases(self):
        self.assertEqual(normalize_dest("s"), "zh-hans")
        self.assertEqual(normalize_dest("t"), "zh-hant")
        self.assertEqual(normalize_dest("zh-CN"), "zh-hans")

    def test_google_lang_mapping(self):
        self.assertEqual(to_google_lang("zh-hans"), "zh-CN")


class NetworkTest(unittest.TestCase):
    def test_respects_explicit_channel(self):
        self.assertEqual(select_network("youdao"), "youdao")
        self.assertEqual(select_network("google"), "google")


class ChineseConverterTest(unittest.TestCase):
    def test_simplified_conversion(self):
        self.assertEqual(mkConverter("zh-hans").convert("繁體測試"), "繁体测试")


class StringsUtilsTest(unittest.TestCase):
    def test_escape_quotes_and_backslashes(self):
        self.assertEqual(escape_strings_value('Say "hi"'), r'Say \"hi\"')
        self.assertEqual(escape_strings_value("a\\b"), r"a\\b")

    def test_unescape_roundtrip(self):
        raw = r'line1\nline2\t\"quote\"'
        self.assertEqual(unescape_strings_value(raw), 'line1\nline2\t"quote"')

    def test_replace_strings_value(self):
        line = '"key" = "old";'
        updated = replace_strings_value(line, 'Say "new"')
        self.assertEqual(updated, r'"key" = "Say \"new\"";')


class XmlUtilsTest(unittest.TestCase):
    def test_preserve_font_markup(self):
        root = ET.fromstring(
            '<string name="invite">Invitation<font color="#999">(optional)</font></string>'
        )

        def fake_translate(text: str) -> str:
            return f"EN:{text}"

        translate_element_preserving_markup(root, fake_translate)
        self.assertEqual(root.text, "EN:Invitation")
        font = root.find("font")
        self.assertIsNotNone(font)
        self.assertEqual(font.text, "EN:(optional)")


class StringsTranslationTest(unittest.TestCase):
    def test_translate_strings_file_with_mock(self):
        translator = mkTranslator()
        with patch.object(
            translator,
            "translate",
            side_effect=lambda word, *args, **kwargs: f"EN:{word}",
        ):
            with tempfile.TemporaryDirectory() as tmp:
                source = os.path.join(tmp, "Localizable.strings")
                write_text(source, '"key" = "错误";\n')
                out = os.path.join(tmp, "out.strings")
                translator.translate_strings(source, out, "en", "zh", "youdao")
                with open(out, encoding="utf-8") as handle:
                    content = handle.read()
                self.assertIn("EN:错误", content)

    def test_strings_escape_special_chars(self):
        translator = mkTranslator()
        with patch.object(
            translator,
            "translate",
            return_value='He said "hello"',
        ):
            with tempfile.TemporaryDirectory() as tmp:
                source = os.path.join(tmp, "Localizable.strings")
                write_text(source, '"greet" = "你好";\n')
                out = os.path.join(tmp, "out.strings")
                translator.translate_strings(source, out, "en", "zh", "youdao")
                with open(out, encoding="utf-8") as handle:
                    content = handle.read()
                self.assertIn(r'He said \"hello\"', content)


class XmlTranslationTest(unittest.TestCase):
    def test_translate_xml_with_name_filter(self):
        translator = mkTranslator()
        with patch.object(
            translator,
            "translate",
            side_effect=lambda word, *args, **kwargs: f"EN:{word}",
        ):
            with tempfile.TemporaryDirectory() as tmp:
                source = os.path.join(tmp, "strings.xml")
                write_text(
                    source,
                    '<resources><string name="keep">保留</string>'
                    '<string name="go">翻译我</string></resources>\n',
                )
                out = os.path.join(tmp, "out.xml")
                translator.translate_xml(
                    source,
                    out,
                    "en",
                    "zh",
                    "youdao",
                    names_filter={"go"},
                )
                root = ET.parse(out).getroot()
                values = {elem.attrib["name"]: element_visible_text(elem) for elem in root.findall("string")}
                self.assertEqual(values["keep"], "保留")
                self.assertEqual(values["go"], "EN:翻译我")

    def test_translate_xml_preserves_html(self):
        translator = mkTranslator()
        with patch.object(
            translator,
            "translate",
            side_effect=lambda word, *args, **kwargs: f"EN:{word}",
        ):
            with tempfile.TemporaryDirectory() as tmp:
                source = os.path.join(tmp, "strings.xml")
                write_text(
                    source,
                    '<resources><string name="invite">邀请'
                    '<font color="#999">(可选)</font></string></resources>\n',
                )
                out = os.path.join(tmp, "out.xml")
                translator.translate_xml(source, out, "en", "zh", "youdao")
                root = ET.parse(out).getroot()
                elem = root.find("string")
                self.assertEqual(elem.text, "EN:邀请")
                font = elem.find("font")
                self.assertIsNotNone(font)
                self.assertEqual(font.get("color"), "#999")
                self.assertEqual(font.text, "EN:(可选)")


class EncodingTest(unittest.TestCase):
    def test_detect_utf16_bom(self):
        with tempfile.NamedTemporaryFile(delete=False) as handle:
            handle.write(b"\xff\xfe" + "键".encode("utf-16-le"))
            path = handle.name
        try:
            self.assertEqual(detect_encoding(path), "utf-16")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
