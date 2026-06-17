# mkTranslate：支持多种语言的互译

## 2.1 更新

- **XML 内嵌 HTML 保留**：`<font>` 等标签不丢失，只翻译文本节点
- **`.strings` 转义修复**：翻译结果正确转义 `"`、`\`、换行
- **翻译重试**：失败自动重试后再切换通道
- **i18ns.com 默认关闭**：需设置 `MKTRANSLATE_I18NS=1` 才启用
- **测试不依赖外网**：CI 更稳定

## 2.0 更新

- 仅支持 **Python 3.9+**
- 默认翻译通道改为 **有道**（`-c youdao`）
- Google 翻译改用 **deep-translator**，修复 `tkk` 失效问题
- 可选 `GOOGLE_TRANSLATE_API_KEY` 使用官方 Google Cloud 翻译
- `.strings` 自动识别 **UTF-8 / UTF-16 BOM**
- Android `strings.xml` 使用 **ElementTree** 解析，支持 CDATA
- 新增 `--names` 只翻译指定 `name` 的 string
- **`-c` 参数生效**，不再被 ping 逻辑覆盖

更加便捷的翻译方式：

![](https://github.com/mythkiven/tmp/blob/master/resource/img/oc/translate_quick.png)

## 快速安装

**推荐从 GitHub 安装 2.0**（PyPI 最新仍为 1.6.1）：

```bash
pip install "git+https://github.com/mythkiven/mkTranslate.git@v2.1.0"
translate -h
```

或本地安装：

```bash
git clone https://github.com/mythkiven/mkTranslate.git
cd mkTranslate
pip install -e .
```

[更新日志](CHANGELOG.md) · [Releases](https://github.com/mythkiven/mkTranslate/releases)

### 功能

- 翻译文本 / `.strings` / `.xml` / `.txt`
- Google 翻译（`deep-translator`）+ 可选 Cloud API
- 有道翻译（默认）
- i18ns.com 聚合翻译
- 简繁互译（离线）
- UTF-8 / UTF-16 编码自动识别
- Android XML 使用 ElementTree 解析
- `--names` 按 key 筛选翻译
- macOS / Linux / Windows（Python 3.9+）

### 使用

#### 选项

```
-p 指定要翻译文档的路径
-t 指定要翻译的文本
-d 目标语言(缺省'en'；简体:'s'；繁体:'t')
-c 翻译渠道: youdao(默认)、google、auto
-s 原始语言，使用有道时建议指定
--names 仅翻译指定 Android string name，逗号分隔
```

#### 翻译文档

```bash
translate -p ./chinese.txt -d s
translate -p ./ios.strings -d en -c youdao -s zh
translate -p ./android.xml -d pt -c youdao -s zh
translate -p ./android.xml -d en --names "app_name,login_title" -s zh
```

#### 翻译文本

繁体简体互译
```
$ translate -t '1932年中華民國教育部公佈《國音常用字匯》' -d 'zh-hans'
1932年中华民国教育部公布《国音常用字汇》
$ translate -t '1932年中华民国教育部公布《国音常用字汇》' -d 'zh-hant'
1932年中華民國教育部公佈《國音常用字彙》

$ translate -t '1932年中华民国教育部公布《国音常用字汇》' -d t
1932年中華民國教育部公佈《國音常用字彙》
$ translate -t '1932年中華民國教育部公佈《國音常用字匯》' -d s
1932年中华民国教育部公布《国音常用字汇》
```

```
$translate -t 'Facebook發幣，是偉大征途還是飛蛾撲火？'  # 默认使用谷歌翻译(目标语言是葡萄牙语)
[Use google translation]
Facebook currency, is it a great journey or a moth?


$translate -t 'Facebook发币，是伟大征途还是飞蛾扑火?' -d 'ja' -s 'zh' -c 'youdao' # 使用有道翻译(目标语言是日语)
[Use youdao translation]
[オピニオン]フェイスブックのボーナス、偉大な征途か、蛾の灯か。？
```


###  Demo

#### 繁体简体互译：translate -p ./chinese.txt -d 'zh-hans'

from ./chinese.txt

```
歷史
漢字简化可追溯至新文化運動中關於文字及語文教言和國家發展的討論。
1932年中華民國教育部公佈《國音常用字匯》（見现代標準汉语），確定了現代中國國語標準音系，还收录了部分“破体”、“小字”等宋元以来“通俗的简体字”。
```

to ./translate_zh-hant_chinese.txt

```
历史
汉字简化可追溯至新文化运动中关于文字及语文教言和国家发展的讨论。
1932年中华民国教育部公布《国音常用字汇》（见现代标准汉语），确定了现代中国国语标准音系，还收录了部分“破体”、“小字”等宋元以来“通俗的简体字”。
```

#### strings文件翻译：translate -p ./ios.strings -d 'pt'

from ./ios.strings

```
common_tips_error = "错误";
common_btn_sdk_pin_error = "PIN码输入错误，请检查输入！"; /**"PIN码输入错误，请检查输入！"*/
/** ********************************************   */
gw_input_title_signtx_usdt = "支付USDT手续费:%ld/%@"; /**"支付USDT手续费:%ld/%@"*/
```

to ./translate_pt_by_google_ios.strings

```
common_tips_error = "Erro";
common_btn_sdk_pin_error = "O código PIN é inserido incorretamente, por favor, verifique a entrada!"; /**"PIN码输入错误，请检查输入！"*/
/** ********************************************   */
gw_input_title_signtx_usdt = "Pagar taxa de manuseio do USDT:%ld/%@"; /**"支付USDT手续费:%ld/%@"*/
```

#### xml文件翻译：translate -p ./android.xml
from ./android.xml

```
<resources xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2">
    <!-- tab -->
    <string name="network_error">网络不可用，点击屏幕重试</string>
    <string name="scan_qr_code_warn">将二维码放入框内，即可自动扫描</string>
    <string name="album_text">相册</string>
</resources>
```

to ./translate_en_by_google_android.xml

```
<resources xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2">
    <!-- tab -->
    <string name="network_error">Network is not available, click screen to try again</string>
    <string name="scan_qr_code_warn">Put the QR code into the box and you can scan it automatically.</string>
    <string name="album_text">Album</string>
</resources>
```


### 支持的文件和语种:

- 支持 txt、iOS(.strings) 和 Android(.xml) 的配置文件

- 支持翻译的语言

支持如下任意两个语种互译

```
'af': 'afrikaans',
'sq': 'albanian',
'am': 'amharic',
'ar': 'arabic',
'hy': 'armenian',
'az': 'azerbaijani',
'eu': 'basque',
'be': 'belarusian',
'bn': 'bengali',
'bs': 'bosnian',
'bg': 'bulgarian',
'ca': 'catalan',
'ceb': 'cebuano',
'ny': 'chichewa',
'zh-cn': 'chinese (simplified)',
'zh-tw': 'chinese (traditional)',
'co': 'corsican',
'hr': 'croatian',
'cs': 'czech',
'da': 'danish',
'nl': 'dutch',
'en': 'english',
'eo': 'esperanto',
'et': 'estonian',
'tl': 'filipino',
'fi': 'finnish',
'fr': 'french',
'fy': 'frisian',
'gl': 'galician',
'ka': 'georgian',
'de': 'german',
'el': 'greek',
'gu': 'gujarati',
'ht': 'haitian creole',
'ha': 'hausa',
'haw': 'hawaiian',
'iw': 'hebrew',
'hi': 'hindi',
'hmn': 'hmong',
'hu': 'hungarian',
'is': 'icelandic',
'ig': 'igbo',
'id': 'indonesian',
'ga': 'irish',
'it': 'italian',
'ja': 'japanese',
'jw': 'javanese',
'kn': 'kannada',
'kk': 'kazakh',
'km': 'khmer',
'ko': 'korean',
'ku': 'kurdish (kurmanji)',
'ky': 'kyrgyz',
'lo': 'lao',
'la': 'latin',
'lv': 'latvian',
'lt': 'lithuanian',
'lb': 'luxembourgish',
'mk': 'macedonian',
'mg': 'malagasy',
'ms': 'malay',
'ml': 'malayalam',
'mt': 'maltese',
'mi': 'maori',
'mr': 'marathi',
'mn': 'mongolian',
'my': 'myanmar (burmese)',
'ne': 'nepali',
'no': 'norwegian',
'ps': 'pashto',
'fa': 'persian',
'pl': 'polish',
'pt': 'portuguese',
'pa': 'punjabi',
'ro': 'romanian',
'ru': 'russian',
'sm': 'samoan',
'gd': 'scots gaelic',
'sr': 'serbian',
'st': 'sesotho',
'sn': 'shona',
'sd': 'sindhi',
'si': 'sinhala',
'sk': 'slovak',
'sl': 'slovenian',
'so': 'somali',
'es': 'spanish',
'su': 'sundanese',
'sw': 'swahili',
'sv': 'swedish',
'tg': 'tajik',
'ta': 'tamil',
'te': 'telugu',
'th': 'thai',
'tr': 'turkish',
'uk': 'ukrainian',
'ur': 'urdu',
'uz': 'uzbek',
'vi': 'vietnamese',
'cy': 'welsh',
'xh': 'xhosa',
'yi': 'yiddish',
'yo': 'yoruba',
'zu': 'zulu',
'fil': 'Filipino',
'he': 'Hebrew'
```


### 版本

- **V2.1.0** (2026) 保留 XML HTML、`.strings` 转义、重试、i18ns 可选 — [CHANGELOG](CHANGELOG.md)
- **V2.0.0** (2026) Python 3.9+、deep-translator、ElementTree、UTF-16、`--names` — [CHANGELOG](CHANGELOG.md)
- V1.6.0 支持 windows 系统
- V1.5.0 增加中文简体和中文繁体的互译
- V1.4.0 增加网络检测，自动切换谷歌或有道翻译
- V1.2.3 增加快速翻译 `$translate  'mkTranslate 支持多种语言的互译'`
- V1.2.0 增加有道翻译，
有道会对ip封锁，所以使用了3种翻译通道，其中api翻译是不得已才会调用的，因为**api 接口仅支持中英互译**。暂未注册apikey，目前使用的apikey源于:[api key](http://fengmm521.lofter.com/post/2a9e99_7475571)。虽然有三种翻译通道，但是还可能翻译不出来，还需要优化。
- V1.1.3 增加命令行直接翻译文本


### 其他：

#### 修复：

目前已经添加了一些简单的修复工作：

针对 `"user_notify_type_word_input_index" = "第 %ld/%@ 个单词";`  这种词条，谷歌翻译葡萄牙后 `% ld /% @ palavras`，
脚本会自动删减空格：`"user_notify_type_word_input_index" = "%ld/%@ palavras";`

#### Language Code Table:
![](https://github.com/mythkiven/tmp/blob/master/resource/img/oc/language_code_table.png)



**翻译之后，请务必人工核实，否则可能会因为语义上的差异带来理解困扰或政治风险。实际上任何一种翻译工具，都会有这种问题，请务必谨慎处理**

### 常见问题

| 问题 | 处理 |
|------|------|
| 找不到 `translate` 命令 | 使用 `python3 -m mkTranslation.cli` |
| `.strings` 编码报错 | 升级到 2.0，自动识别 UTF-16 BOM |
| Google 翻译失败 | 使用 `-c youdao` 或配置 `GOOGLE_TRANSLATE_API_KEY` |
| Android XML 被跳过 | 升级到 2.0；可用 `--names` 指定 key |
| PyPI 装到旧版 | PyPI 为 1.6.1，请从 GitHub 安装 2.1 |
| i18ns 未生效 | 2.1 起默认关闭，设置 `MKTRANSLATE_I18NS=1` 启用 |

**更多工具参见：[mkBox](https://github.com/mythkiven/mkBox)**






