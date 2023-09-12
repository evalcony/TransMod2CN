# TransMod2CN

# 介绍

针对 baldur's gate2 的英文 mod，将其自动翻译为中文，并调整好文件编码。

输出文件编码为 `gb18030`。

代码的基本思路是，将文件中的 `~xxx~` 内容解析出来，先对其专有名词进行识别，或直接翻译，或替换为 token 然后走 API 接口调用。对于替换为 token 的，在翻译后还要进行还原操作。

# 项目功能

- 对 mod 的 .tra 文件进行翻译。支持单文件翻译、批量文件翻译。
- 支持有道、google 的翻译API
- 支持对文件自动转码。gb18030, utf-8 等。
- 支持断点恢复。失败之后重新执行时，从失败文件开始执行。
- 支持多语言翻译。
- 限流保护。限制请求API的频率，保证翻译的稳定性（代价是牺牲性能）。

# 使用方法

1. 初次执行前，需要执行项目初始化脚本 init_shell.sh，自动创建程序执行需要的目录和文件。
2. 修改配置文件 appconf.ini
3. 执行需要的程序（如 main.py, simple_main.py, debug.py 等）

- 翻译 tra/ 目录下的文件。将需要翻译的 .TRA 文件放入 tra/ 目录下，然后执行：

```
python3 main.py
```

- simple_main.py 可翻译单个文件、或者一个 file_list。并且，还支持断点重续功能，从失败位置继续翻译，而不是从头开始。
建议使用此方法，比 main.py 更灵魂，功能更丰富。
```
python3 simple_main.py
```

- debug.py 用来做一些简单的功能和测试。
- sep_and_combine.py 对大文件进行切分和聚合，减少每次执行的时间成本。
- correctness_check.py 文件正确性校验。由于句子内会有' @xxx = ~ 111 222~ 333~ ' 这种形式的句子，所以存在误报情况。
- merge_file.py 对将多个文件合并入 master 文件，并输出为新文件。
- ctnt_search.py 提供对目标内容的搜索功能，并将搜索结果导出文件。格式为:
```commandline
filename | pattern | line_num | content
文件名 | 匹配字符串 | 行号 | 该行内容
```
ctnt_search 支持批量替换功能。在搜索结果的 search.txt 文件中，删除不想替换的行，保留想替换的行，执行命令 `python3 ctnt_search.py -r "要替换的内容""` 即可完成对这部分结果的替换。
如果要替换为 `''`，则需要命令 `python3 ctnt_search.py -d`
- compare_enzh.py 对搜索关键字的原文和译文进行比较。使用方法 `python3 compare_enzh.py -s "关键字""`，搜索结果放在 output/compare.txt 中，格式为
```commandline
原文文件路径
原文
译文
```
使用这个工具可以快速查找一个英文在所有文件中的翻译是怎样的，便于快速定位不同的翻译结果。


# 翻译 API

目前支持 `有道`、`google`的翻译。可在 `appconf.ini` 中配置选择哪个API。默认是有道翻译。

有道需要自己申请appkey。

google 在国内的话需要设置代理。

在 appconf.ini 中，`use=youdao` `use=google` 表示使用有道或google翻译。

# 执行所依赖的文件介绍

- word_dict.txt 一个单词作为专有名词。不能包含空格。因为代码中的逻辑是依据单词匹配和替换（先根据空格分词，再进行匹配）。以 `#` 分割。

- comp_word_dict.txt 复合单词组成的专有名词，允许包含空格。代码中的识别方式是字符串匹配和替换。以 `#` 分割。
进一步的，当一行中仅仅包含这个词时，则不进行翻译的API调用。

- manual_trans_word_dict.txt 复合单词组成的专有名词，允许包含空格。代码中的识别方式是字符串和替换。以 `#` 分割。
如果命中这个文件里的单词，则不进行翻译的API调用。

- sp_word_dict.txt 当检测到 manual_trans_word_dict 中词时，要在 sp_word_dict.txt 这个文件中检测。因为有些常用词在日常的翻译和游戏环境上下文的翻译，是不一样的。必须要把这两种情况区分开。

- name_dict.txt 存放姓名的翻译。以 `#` 分割。

- tra/ 存放需要翻译的原始的.tra文件。需要自己建目录。

- output/ 存放翻译后的.tra文件。需要自己建目录。

- appconf.ini 配置文件，放翻译API的相关配置信息。

通过执行初始化shell脚本 `init_shell.sh` 后，在 `appconf.ini` 文件中加入相关信息。

- readlog.txt 记录上次执行结束点功能。每次任务时，会先读 readlog.txt，找到上一次的记录点，然后从该位置开始执行。
每次任务执行成功后，调用 log.done(), 在文件末尾写入 'done' 记录，表示本次任务全部执行完。下次再执行时，则会忽略 readlog.txt 中全部内容。
readlog.txt 的格式为 `filename|line_num`
filename 表示读的文件
line_num 表示下一次执行的行号(在代码中，即`当前行+1`) 
例如，假如上一次在成功写入第10行后，接口报错退出，那么readlog.txt 中最后一条记录是 `file|11`

- 在 simple_main.py 中，增加了 `trans_and_write_append` 方法，作用是每翻译一行，立即写文件。 
这在API容易出错的情况下，这个方案可以解决出错导致整个文件没保存的部分白白浪费的情况。 
由于每次调用都有一定时延，所以不会特别频繁写文件。
这个方案做到了断点重续，从失败位置开始继续翻译，而不是从文件头开始重新翻译，提升了效率。

- 
项目中给出了一个以上若干文件写法的例子，是翻译一个 `威尔逊编年史`mod 的实现。

### 注意

1.

由于实现机制是字符串匹配，所以如果 `*_dict.txt` 文件中(comp_word_dict.txt, manual_trans_word_dict.txt)有 key 互相包含时，比如 `aaa包含a`，这时就应该将 aaa 写在 a 的前面，优先被遍历到，而不会干扰到 a 的识别。

例如，文件中配置了下面2项
```
THACO#零级命中值
AC#护甲值
```
就应该将 THACO 写在 AC 前面，否则，AC会先识别并完成替换，那么 THACO 就无法正确识别。

2.

会自动忽略 SETUP.TRA 文件。因为自己测试时，翻译这个文件会导致 mod 安装界面乱码。
所以，翻译完成后，需要手动复制 SETUP.TRA 文件到需要安装的 mod 的 schinese/ 目录下。

# 其他介绍

### debug

Solver 的入参设置 `mode='debug'` 模式，则不进行 API 调用，而且打印更为详细的信息，便于调试。

缺省则是正常模式，会调用 API。

### counter 计数器

为了防止调用频繁触发风控策略，使用 counter 进行计数器，每调用一定次数后，进行适当长休。

# todo

- 失败重试