# Translation-of-DarkRPG
因为我自己想玩，所以我尝试把旧版本的汉化移植到新版本上。  
旧版本的整合包主要由指星汉化组翻译。遵照他们和 CFPA 的许可协议，我使用 CC BY-NC-SA 4.0 协议再分发。  
我不对本项目的运行作任何保证。  
但是，你可以在 Issue 界面提问，亦或者提交你的 Pull Request ，我会在力所能及的范围下回复。  
我不在乎手段，例如我随时可能使用 GPT ，但我会人工进行校对——这是在我汉化 GTNH 时便已经采取的。  
由于我的特立独行，我不会加入任何团队。  
特别感谢指星汉化组提供了旧版本整合包的汉化，感谢 CFPA 译者翻译了近百万条模组文件。本汉化是对其余内容的补遗。

Plasma(duoduo70)  
2024/5/13

## 如何使用
因为这个汉化需要支持尽可能多的版本，它是需要根据你玩的版本去编译然后注入的。  
你需要先安装个 Python3 ，然后确保你可以用 `python` 命令，安装完 Python 应该是会自动给你配置的，如果不行的话你去设置个环境变量。是 `python` 命令，不是 `python3` 命令，如果你在用 Python3 刚发布那会儿的 Python 它可能会给你这么设。

下载下来，覆盖你的整合包目录，打开控制台，输入：
```
python ./pmt.py -u replace_rules.json global_packs
```

别告诉我你这都不会，那你开啥服务器啊，洗洗睡吧，或者去玩米米世界。

如果你只是想和女朋友玩，那等我啥时候心情好编译一份最新版发 Release 里，但我现在心情不好。或者发 Issue 求我。

## 如何参与翻译
首先，你用我的 PMT 翻译肯定是比传统方法要强，但是 PMT 现在还是个 demo ，只能做很简单的替换工作，字节码替换啥的还得用老方法。这个脚本的好处是翻译一份就能撑一辈子，尤其是 DarkRPG 这种更新很快还没人专门维护汉化的。并且它移植原有翻译也很快，直接自动转换各种格式到 PMT 格式。曾几何时我翻译 GTNH ，那堆魔改差点没送走我——现在魔改汉化也可以无限兼容新版本。自己玩的时候，看见英文，可以直接在汉化文件里加一行，重新编译之后就成中文了——以前还得找找它在哪儿。  
用 Python 写的原因纯粹是用 Python 的人多，很多人电脑上都有，不用再额外安装了——并且跨平台——java 我完全不想用，连 JSON 解析的标准库都没有——那么多高端功能都有，就这个基础功能没有，很脑残，所以我宁肯用 Python 。  
PMT 也可以代替 CFPA 的那套工具链，那东西太重量级了。像我一样图一乐翻译的，直接用这个小脚本就成。当然，不是让你把自动汉化更新模组删掉——PMT是为了方便做零碎的翻译而生的，是各种汉化源之间的最后一点胶水。  
欢迎发 PR ，如果我半个月不回你，那我大概率是猝死了，你自己开个分支得了，明年清明记得给我赛博扫墓一下。  
现在实际上只缺一个检测机制——我写这个程序实际上就是简单的“找规律”——检测那些首字母大写的英文，大概率是要翻译的文本，然后把它们是什么以及它们的位置打印出来，最好再来个 REPL ，直接顺手就给翻译了。  
如果想对 PMT 进行任何更改，可以合并更改到我这里，让它越来越好。

所以怎么快速提炼汉化呢？你只需要找到你想玩的整合包中最新的汉化，然后找到当时版本对应的英文版，这样写：
```
python pmt.py --transform <英文目录> <中文目录>
```
然后它会自动生成 PMT 格式的汉化，如果有错误（比如找不到中文翻译对应的英文原始文件），会以百分号括住错误一个错误提示，例如`%PMT_FILE_NOT_FOUND_ERROR%`——你需要手动翻译这些内容。  
如果你不管它们，其实一般也没事，无非是少几条汉化。  
有些时候，这些缺失非常多，那么你可能需要使用：
```
python pmt.py --transform-dump <英文目录> <中文目录>
```
它会输出一些辅助信息，你可以利用这些信息寻找对应的英文。  

如果有很多配置文件，你想要找到其中的中文汉化的位置，你可以使用：
```
python -t <目录>
```

如果你要翻译大量存在于 jar 包内的数据（就像 DarkRPG 一样），你可以用`unzip`功能。
详情请参见本项目的 `replace_rules.json`。

对于一些特殊位置的翻译，例如你要翻译 NBT ——它有大量的转译字符，我们的简易引擎无法自动识别——那么你可以使用 early-init 和 lately-init 脚本，同样，在本项目中也用到了。

如果你掌握了上述功能，并且能够熟练运用 GPT 和拼凑网上的零散资源，那么你实际上已经可以一个人顶一个汉化组了。

另外，其实这个汉化比其他人的反而慢一些，虽然同步很方便，但是我生活繁忙，同步随缘。主要是可以兼容更新的官方版本，在有基本的英文能力的情况下或许体验会更好一些。  
授人以鱼不如授人以渔吧（摊手）