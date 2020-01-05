# 什么是ChakraCore

ChakraCore 是微软开源的 Microsoft Edge 浏览器 Chakra JavaScript 引擎的核心部分，主要用于 Microsoft Edge 和 Windows 中 HTML/CSS/JavaScript 编写的应用

ChakraCore 支持 x86/x64/ARM 架构 JavaScript 的 Just-in-time (JIT) 编译，垃圾收集和大量的最新 JavaScript 特性。ChakraCore 还支持 JavaScript Runtime (JSRT) APIs，允许用户简单嵌入 ChakraCore 到应用中。

ChakraCore 是一个功能完整的、独立的 JavaScript 虚拟机，可嵌入到衍生产品中，驱动需要脚本功能的产品如 NoSQL 数据库、生产力工具和游戏引擎。ChakraCore 现在已经跨平台支持：Windows、MacOS、Ubuntu

详细参考微软开源地址：https://github.com/Microsoft/ChakraCore

# JS脚本支持有哪些优势？
在流行的脚本语言中，Lua的小巧高性能（性能指LuaJit的性能），Python的功能性一直受开发者青睐。有什么理由使用JS脚本呢？
JS脚本有众多的库支持
JS脚本被用于HTML网页开发，开发者众多
JS有众多大公司的支持
JS有优秀的即时编译（JIT）性能
JS有无敌的开发工具Visual Studio的支持
JS语言特性更类似C/C++，相比Lua要舒服很多
Chakra的嵌入优势：相比Lua的堆栈式API，Chakra的API更容易写胶水代码。
很多游戏使用Lua的原因是比Python性能好，没有其他可选方案了。Chakra的开源，应该带动开发者去使用JS脚本。Chakra对于大型Windows游戏开发者更大的好处在于系统支持，Lua需要去下载编译，而Chakra只需要包含头文件，链接lib。

# QA
可以列出全局对象或函数吗？
可以，除了Intl，这是个特例
JS可以使用引用（c++的&，c#的ref）参数吗？
不可以，即使你为传入Native的函数参数修改值也是没用的。
如果一定要用，那只能传一个引用类型的对象，在函数内部修改此对象的成员。var arr=[];(function (v){v[1]=1;})(arr);//arr[1] == 1
Chakra的API支持多线程吗？
支持，据我当前的研究，不同线程必须有各自的runtime对象，每个runtime可以有多个环境（context），同一个runtime下的多个环境可以自由交换数据，但环境之间不共享数据。也就是说api级别可以把环境1的数据带到环境2，但是脚本里，环境2是看不到环境1的数据的。
Chakra支持ES6的Symbol吗？
完全支持。
Chakra如何在原生函数里支持JS的闭包？
函数（function）也是对象（object），可以有自定义属性，所以，在原生API级别操作Chakra时，可以把需要闭包的变量放在函数的属性里。如果希望在脚本中是只读的，那么可以设置属性描述。如果希望在脚本中是隐藏的，那么可以用符号属性。

# 关于python目前的js执行

1、pyexecjs+node -> 目前使用最广泛最全面的一个，可以跨平台，也自带有很多js封装函数，最大缺点是性能，一旦并发很吃资源
2、pyv8 -> 据了解，性能很好。不过光是安装都比较费劲，对python3似乎不如python2友好，因为本人未曾使用，不多做说明，具体大家可以补充。
3、js2py -> 这个执行简单的一下js还是不错的，但是稍微大一点的js，就困难了。好像是要先转py代码再执行
4、windows自带的com组件 -> 不如node全面，可执行范围有限，不能跨平台
5、就是本场主角ChakraCore了 -> 该引擎不仅综合node，更是解决了性能问题，本人亲测并发效果1000线程效果是execjs+node的两倍以上

# 注意
由于网上所找到的有限，没有针对python方面的使用，所以根据https://xz.aliyun.com/t/2450 做了一些处理，本代码当前仅支持在windows系统下调用ChakraCore.dll，对于Linux需要ChakraCore.so，详细后面抽时间补充下。有兴趣的朋友可以补充下Linux/Mac 下的使用。

.dll和.so文件下载可自行网上搜索，也可以直接在本站下载
