# mkTranslate(V1.2.0)：支持多种语言的互译

### 安装：

`pip install mkTranslation`

### 使用：

```
-p 指定要翻译文档的路径
-t 指定要翻译的文本
-d 目标语言(缺省'en')
-c 指定翻译渠道:[-c "google"] or [-c "youdao"] (缺省google)
-s 原始语言，有道翻译检测原始文本语言不太准确，翻译的结果会不太准确，所以使用有道翻译时，最好要指定原始的语言
```

- 翻译文档

```
translate -p ./ios.strings -d 'pt'       # 默认使用 google 翻译
translate -p ./android.xml -d 'pt'       # 默认使用 google 翻译
translate -p ./test.txt -d 'pt' -c 'youdao' -s 'zh'   #使用有道翻译
自动在原始文件目录生成翻译后的文件  translate_pt_android.xml translate_pt_ios.strings translate_pt_test.txt
```

- 翻译文本

```
$translate -t 'Facebook發幣，是偉大征途還是飛蛾撲火？' -d 'pt'
# 默认使用谷歌翻译(目标语言是葡萄牙语)
Moeda do Facebook, é uma ótima jornada ou uma mariposa?

$translate -t 'Facebook發幣，是偉大征途還是飛蛾撲火？' -d 'ja' -s 'zh'
# 使用有道翻译(目标语言是日语)
Facebook currency, is it a great journey or a moth?
```

更多用法 参见 `translate -h`


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


### demo

原始 .strings 文件

```
common_btn_sdk_pin_error = "錯誤";
common_btn_sdk_pin_error = "PIN 碼輸入錯誤，請檢查輸入！"; /**"PIN 碼輸入錯誤，請檢查輸入！"*/
common_btn_sdk_cys_error = "助記詞或助記詞密碼錯誤，請檢查輸入！"; /**"助記詞或助記詞密碼錯誤，請檢查輸入！"*/
Home_alertview_pin = "請在設備上輸入 PIN 碼..."; /**"請在設備上輸入 PIN 碼..."*/
Home_alertview_cpinconnect = "正在建立連接.."; /**"正在建立連接.."*/
Home_alertview_cpinunconnect = "已斷開連接"; /**"已斷開連接"*/
/** ********************************************   */
gw_input_title_signtx = "%@/%@转账"; /**"%@转账"*/
gw_input_title_signtx_usdt = "支付 USDT 手續費:%ld/%@"; /**"支付 USDT 手續費:%ld/%@"*/
```

`translate -p ./ios.strings -d 'pt'` 翻译后

```
common_btn_sdk_pin_error ="Erro";
common_btn_sdk_pin_error ="O código PIN é inserido incorretamente, por favor, verifique a entrada!"; /**"PIN 碼輸入錯誤，請檢查輸入！"*/
common_btn_sdk_cys_error ="A senha mnemônica ou mnemônica está errada, por favor verifique a entrada!"; /**"助記詞或助記詞密碼錯誤，請檢查輸入！"*/
Home_alertview_pin ="Por favor, digite seu PIN no seu dispositivo ..."; /**"請在設備上輸入 PIN 碼..."*/
Home_alertview_cpinconnect ="Conectando está sendo estabelecido:"; /**"正在建立連接.."*/
Home_alertview_cpinunconnect ="Desconectado"; /**"已斷開連接"*/
/** ********************************************   */
gw_input_title_signtx ="%@/%@ transfer"; /**"%@转账"*/
gw_input_title_signtx_usdt ="Pagar taxa de manuseio do USDT:%ld/%@"; /**"支付 USDT 手續費:%ld/%@"*/
```

原始 .xml 文件

```
<resources xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2">
    <string name="ensure_app_normal_run_permission"> 为了保证软件的正常运行，必须要获取权限 </string>
    <!-- tab -->
    <string name="network_error"> 网络不可用，点击屏幕重试 </string>
    <string name="last_page"> 错误 </string>
    <string name="scan_qr_code_warn"> 将二维码放入框内，即可自动扫描 </string>
    <string name="album_text"> 相册 </string>
    <string name="qr_code_text"> 二维码 </string>
    <string name="scan_qr_code_from_photo_wrong"> 没有找到二维码 </string>
    <string name="most_withdraw"> 最多可用:</string>
    <string name="all_text"> 全部 </string>
    <string name="withdraw_chain_status"><xliff:g>%s</xliff:g></string>
    <string name="create_wallet_tips"> 开始以下操作前，请确保您处在四周无人、没有摄像头的安全环境，并准备好一支笔和您的助记码记录卡或一张空白卡纸 </string>
    <string name="system_setting"> 系统设置 </string>
    <string name="payfor_miners"> 支付矿工费 </string>
    <string name="high_grade"> 高级设置 </string>
</resources>
```

`translate -p ./android.xml -d 'pt'` 翻译后

```
<resources xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2">
    <string name="ensure_app_normal_run_permission">Para garantir o funcionamento normal do software, você deve obter permissão.</string>
    <!-- tab -->
    <string name="network_error">Rede não está disponível, clique na tela para tentar novamente</string>
    <string name="last_page">Erro</string>
    <string name="scan_qr_code_warn">Coloque o código QR na caixa e você pode digitalizá-lo automaticamente.</string>
    <string name="album_text">Album</string>
    <string name="qr_code_text">Código QR</string>
    <string name="scan_qr_code_from_photo_wrong">Nenhum código QR encontrado</string>
    <string name="most_withdraw">Mais disponível:</string>
    <string name="all_text">Todos</string>
    <string name="withdraw_chain_status"><xliff: g>%s</ xliff: g></string>
    <string name="create_wallet_tips">Antes de iniciar as seguintes operações, certifique-se de estar em um ambiente seguro, sem câmeras, sem câmeras e com uma caneta e seu cartão de memória mnemônico ou um congestionamento em branco.</string>
    <string name="system_setting">Configurações do sistema</string>
    <string name="payfor_miners">Pagar pelos mineiros</string>
    <string name="high_grade">Configurações avançadas</string>
</resources>
```


### 版本

- V1.2.0 增加有道翻译，
有道会对ip封锁，所以可能出现无法翻译的问题，此时将会使用 api 接口翻译，本人申请的 api 接口仅支持中英互译。[使用的key](http://fengmm521.lofter.com/post/2a9e99_7475571)
- V1.1.3 增加命令行直接翻译文本

更新本机的 mkTranslation：`pip install --upgrade mkTranslation`
查看本机的 mkTranslation 信息：

### 后续：

- 修复：

已经添加了一些简单的修复工作：

针对 `"user_notify_type_word_input_index" = "第 %ld/%@ 个单词";`  这种词条，谷歌翻译葡萄牙后 `% ld /% @ palavras`，
脚本会自动删减空格：`"user_notify_type_word_input_index" = "%ld/%@ palavras";`

后续将会增加更多修复

- 翻译渠道：

优化有道翻译
