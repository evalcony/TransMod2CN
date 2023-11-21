# TransMod2CN

## 项目简介

针对博德之门(BG1, BG2, EE, EET, etc.) 的英文 mod，将其自动翻译为中文，并调整好文件编码。

一般而言，汉化中文 mod 需要将输出文件编码设置为`utf-8`或者`gb18030（GBK）`。取决于具体的 mod 实现（不同的 mod 在编码上有所不同，需要自己测试）。大多情况下，设置成`utf-8`即可。

代码的基本思路是，将文件中的 `~xxx~` 内容解析出来，先对其专有名词进行识别，或直接翻译，或替换为 token 然后走 API 接口调用。对于替换为 token 的，在翻译后还要进行还原操作。

## 项目功能

- 对 mod 的 .tra 文件进行翻译。支持单文件翻译、批量文件翻译。
- 支持有道、google 的翻译API。
- 支持对文件自动转码。gb18030, utf-8 等。
- 支持断点恢复。失败之后重新执行时，从失败文件的失败位置开始执行。
- 支持多语言翻译（默认英译汉）。
- 限流保护。限制请求API的频率，保证翻译的稳定性（代价是牺牲性能）。
- 支持 tra 文件中中英文混杂情况下，跳过中文部分。这种场景一般来说发生在一个对已有汉化的 mod 的更新。
- 支持 namespace，兼容多个翻译任务

## 使用方法

1. 初次执行前，需要执行项目初始化脚本 init_shell.sh，输入`namespace`，自动创建程序执行需要的目录和文件。
2. 修改配置文件 appconf.ini
3. 将待汉化 .tra 文件放入 tra/ 目录下。
4. 执行需要的程序（如 main.py, simple_main.py, debug.py 等）

main.py 对 tra/ 目录下的文件进行翻译。
```
python3 main.py
```

simple_main.py 可翻译单个文件、或者一个 file_list。并且，还支持断点重续功能，从失败位置继续翻译，而不是从头开始。
建议使用此方法，比 main.py 更灵活，功能更丰富。
```
python3 simple_main.py
```

## 一些辅助程序

见[辅助程序介绍](docs/辅助程序介绍.md)


## 翻译 API 设置

目前支持的翻译工具
- `有道`
- `google`

可在 `appconf.ini` 中配置选择哪个API。默认是有道翻译。（建议使用google）
有道需要自己申请appkey。

参数介绍

- use: 表示使用哪个API进行翻译。可选项 youdao, google
- appKey: appKey
- appSecret: appSecret
- proxy: 代理地址
- namespace: 命名空间，根据mod进行区分。一般来说，即mod名。


## 依赖文件介绍

见[依赖文件介绍](docs/执行所依赖的文件介绍.md)


## 其他介绍

见[其他介绍](docs/其他介绍.md)

## todo

- 失败重试
- 不同版本 mod 文件比对
- 支持多语言翻译配置

## 已汉化案例

1. 龙矛围攻 BG1EE:SoD Siege of Dragonspear v2.6.6
2. 索劳芬罗曼史 Solaufein v2.04
3. 未竟的事业 Unfinished Business v29
4. 威尔逊编年史 Wilson Chronicles
5. 漫长的旅途 The Longer Road v2.06
6. 巅峰之战 Ascension v2.023
7. 艾德温罗曼史 Edwin Romance v3.1
8. 伊文德拉 Evandra NPC mod