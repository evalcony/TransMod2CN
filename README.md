# TransMod2CN

# 介绍

针对 baldur's gate2 的英文 mod，将其自动翻译为中文，并调整好文件编码。

输出文件编码为 `gb18030`。

基本思路是，将文件中的 `~xxx~` 内容解析出来，先对其专有名词进行识别，或直接翻译，或替换为 token 然后走 API 接口调用。对于替换为 token 的，在翻译后还要进行还原操作。

# 使用方法

```
python3 main.py
```

# 翻译 API

目前支持 `有道`、`google`的翻译。可在 `appconf.ini` 中配置选择哪个API。默认是有道翻译。

有道需要自己申请appkey。

google 在国内的话需要设置代理。

# 执行所依赖的文件介绍

- default_word_dict.txt 一个单词作为专有名词。不能包含空格。因为代码中的逻辑是依据单词匹配和替换（先根据空格分词，再进行匹配）。以 `#` 分割。

- comp_word_dict.txt 复合单词组成的专有名词，允许包含空格。代码中的识别方式是字符串匹配和替换。以 `#` 分割。
进一步的，当一行中仅仅包含这个词时，则不进行翻译的API调用。

- manual_trans_word_dict.txt 复合单词组成的专有名词，允许包含空格。代码中的识别方式是字符串和替换。以 `#` 分割。
如果命中这个文件里的单词，则不进行翻译的API调用。

- name_dict.txt 这个文件目前无作用。因为API对于中英文混合的内容支持不够好。以 `#` 分割。

- tra 需要翻译的原始的.tra文件

- output 翻译后的.tra文件

- appconf.ini 配置文件，放翻译API的相关配置信息。
目前默认是调用有道词典的API

自己创建 `appconf.ini` 文件后，在其中加入如下信息，并自行申请相关API。

`appconf_demo.ini` 是 `appconf.ini` 的模板。

项目中给出了一个以上若干文件写法的例子，是翻译一个 `威尔逊编年史`mod 的实现。

### 注意

由于实现机制是字符串匹配，所以如果 `*_dict.txt` 文件中(comp_word_dict.txt, manual_trans_word_dict.txt)有 key 互相包含时，比如 `aaa包含a`，这时就应该将 aaa 写在 a 的前面，优先被遍历到，而不会干扰到 a 的识别。

例如，文件中配置了下面2项
```
THACO#零级命中值
AC#护甲值
```
就应该将 THACO 写在 AC 前面，否则，AC会先识别并完成替换，那么 THACO 就无法正确识别。

# 其他介绍

### debug

debug.py 文件中，设置 `mode='debug'` 模式，不进行 API 调用，而且打印更为详细的信息，便于调试。

设置 `mode=''` 就是正常模式，会调用 API。

使用方法
```
python3 debug.py
```

### counter 计数器

为了防止调用频繁触发风控策略，使用 counter 进行计数器，每调用一定次数后，进行适当长休。