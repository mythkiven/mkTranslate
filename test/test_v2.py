import os
import tempfile
import unittest
import xml.etree.ElementTree as ET

from mkTranslation.io_utils import detect_encoding, write_text
from mkTranslation.lang_utils import normalize_dest, to_google_lang
from mkTranslation.network import select_network
from mkTranslation.translate_chinese import mkConverter
from mkTranslation.translator import mkTranslator


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


class StringsTranslationTest(unittest.TestCase):
    def test_translate_strings_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = os.path.join(tmp, "Localizable.strings")
            write_text(source, '"hello" = "错误";\n')
            out = os.path.join(tmp, "translate_en_by_youdao_Localizable.strings")
            mkTranslator().translate_strings(source, out, "en", "zh", "youdao")
            content = open(out, encoding="utf-8").read()
            self.assertIn('="', content)
            self.assertNotIn("错误", content)


class XmlTranslationTest(unittest.TestCase):
    def test_translate_xml_with_name_filter(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = os.path.join(tmp, "strings.xml")
            write_text(
                source,
                '<resources><string name="keep">保留</string>'
                '<string name="go">翻译我</string></resources>\n',
            )
            out = os.path.join(tmp, "out.xml")
            mkTranslator().translate_xml(
                source,
                out,
                "en",
                "zh",
                "youdao",
                names_filter={"go"},
            )
            root = ET.parse(out).getroot()
            values = {elem.attrib["name"]: (elem.text or "") for elem in root.findall("string")}
            self.assertEqual(values["keep"], "保留")
            self.assertNotEqual(values["go"], "翻译我")


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
