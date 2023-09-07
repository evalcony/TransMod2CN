# TransMod2CN

# 介绍

针对 baldur's gate2 的英文 mod，将其自动翻译为中文，并调整好文件编码。

输出文件编码为 `gb18030`。

基本思路是，将文件中的 `~xxx~` 内容解析出来，先对其专有名词进行识别，或直接翻译，或替换为 token 然后走 API 接口调用。对于替换为 token 的，在翻译后还要进行还原操作。

# 相关文件介绍

- default_word_dict.txt 一个单词作为专有名词。不能包含空格。因为代码中的逻辑是依据单词匹配。

- comp_word_dict.txt 复合单词组成的专有名词，允许包含空格。
进一步的，当一行中仅仅包含这个词时，则不进行翻译的API调用。

- manual_trans_word_dict.txt 复合单词组成的专有名词，允许包含空格。如果命中这个文件里的单词，则不进行翻译的API调用。

- name_dict.txt 这个文件目前无作用。因为API对于中英文混合的内容支持不够好。

- tra 放需要翻译的原始的.tra文件

- output 翻译后的.tra文件

- appconf.ini 配置文件，放翻译API的相关配置信息。
目前默认是调用有道词典的API

自己创建 `appconf.ini` 文件后，在其中加入如下信息，并自行申请相关API。
```
[youdao]
appKey=你的appkey
appSecret=你的appsecret
```

# 使用方法
```
python3 main.py
```