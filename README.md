# mkTranslate: support multi-language translation


### 1.Features

- translated text
- translate .string file
- translate .xml file
- translate .txt file
- support google translation
- support youdao translation
- support i18ns.com translation
- more features will be added..

**The default translation is google translation, you can specify other translation channels**


### 2.installation：

`pip install mkTranslation`

Update existing version : `pip install --upgrade mkTranslation`

If installed, the terminal cannot recognize the `translate` command, [reference here](https://github.com/mythkiven/mkTranslate/issues/1)


### 3.Usage：

#### Options
```
-p  path to the translated document
-t  translated text
-d  target language (default 'en')
-c  translation channel: [-c "google"] or [-c "youdao"] (default google)
-s  original language, when using 'youdao' translation, it is best to specify the original language
```


#### Translating documents

```
translate -p ./ios.strings        # Use google translation by default （the default target language is 'en'）
translate -p ./android.xml -d 'pt'       # Use google translation by default (the default target language is 'pt'）
translate -p ./test.txt -d 'zh' -c 'youdao' -s 'ja'   # Use 'youdao' translation  (the default target language is 'ja'）

Automatically generate translated files in the original file directory : translate_pt_android.xml translate_en_ios.strings translate_ja_test.txt
```

#### Translated text

```
$translate -t 'mkTranslate 支持多种语言的互译'                  # Will use the default google translation （the default target language is 'en'）
    mkTranslate supports translation in multiple languages
$translate -t 'mkTranslate 支持多种语言的互译' -d 'ja'          # Will use the default google translation ( the target language is 'ja')
    mkTranslateは複数の言語での翻訳をサポートします
$translate -t 'mkTranslate 支持多种语言的互译' -d 'ja' -s 'zh'  # Will use 'youdao' translation ( the target language is 'ja')
    mkTranslateは複数の言語での翻訳をサポートします
```


### 4.Support the translation of any two languages as follows

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


### 4.demo

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


### Version
- V1.3.1 Fix bugs in previous versions
- V1.2.3 Increase fast translation `$translate  'mkTranslate 支持多种语言的互译'`
- V1.2.0 Add youdao translation:
There is a way to block ip, so three translation channels are used, of which api translation is a last resort, because the **api interface only supports Chinese-English translation**.Apikey is not registered yet, the currently used apikey is derived from: [api key](http://fengmm521.lofter.com/post/2a9e99_7475571).Although there are three translation channels, they may not be translated and need to be optimized.
- V1.1.3 Add command line to translate text directly



### Future plan：

- Repair translation channel：

- Improve translation quality：

Some simple fixes have been added so far：

For `"user_notify_type_word_input_index" = "第 %ld/%@ 个单词";`  this entry，google translates to:  `% ld /% @ palavras`，
and the script is automatically fixed as：`"user_notify_type_word_input_index" = "%ld/%@ palavras";`


### other
