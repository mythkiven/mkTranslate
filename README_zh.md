# mkTranslate：支持多种语言的互译


### 功能

- 翻译文本文件
- 翻译.strings文件
- 翻译.xml文件
- 翻译 文本
- 支持谷歌翻译
- 支持有道翻译
- 支持 i18ns.com 聚合翻译
- 会自动检测当前网络情况，从而决定使用谷歌还是有道翻译(有道翻译为了防IP封锁，使用3种渠道切换，所以速度会比谷歌慢一些，如果谷歌能用，将优先使用谷歌翻译)


### 安装：

`pip install mkTranslation`

更新现有版本：`pip install --upgrade mkTranslation`

如果安装后,终端不能识别`translate`命令，[参考这里](https://github.com/mythkiven/mkTranslate/issues/1)

### 使用：

#### 选项

```
-p 指定要翻译文档的路径
-t 指定要翻译的文本
-d 目标语言(缺省'en',繁体简体互译时，可以用's'替代'zh-hans',用't'替代'zh-hans',s=simple=简体，t=traditional=繁体)
-c 指定翻译渠道:[-c "google"] or [-c "youdao"] (缺省google)
-s 原始语言，有道翻译检测原始文本语言不太准确，翻译的结果会不太准确，所以使用有道翻译时，最好要指定原始的语言
```

#### 翻译文档

```
translate -p ./chinese.txt  -d 's'                  # 文件转为简体。繁体:'t' 简体:'s'
translate -p ./ios.strings                          # 默认使用 google 翻译，默认目标语言为 'en'
translate -p ./android.xml -d 'pt'                  # 默认使用 google 翻译，目标语言为葡萄牙语
translate -p ./test.txt -d 'pt' -c 'youdao' -s 'ja' # 使用有道翻译，目标语言为日语
自动在原始文件目录生成翻译后的文件  translate_pt_android.xml translate_en_ios.strings translate_ja_test.txt
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

#### translate -p ./ios.strings -d 'pt'

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

#### translate -p ./android.xml
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

