## 简介

这是一个 `cpp` 文件树转单一 `markdown` 脚本的工具，初衷主要用于帮助 ACMer 整理板子。



## 配置条件

您的 `cpp` 目录必须满足以下条件：

* `cpp`目录采用文件树的格式，`cpp`文件必须是纯文本的 `cpp` 源代码。
* 该脚本（`cpps2md.exe/cpp2md.py`）及其相关配置文件必须位于您期望的 `cpp` 目录（工作目录）的 `.bin` 目录下。



您的设备必须满足以下条件：

* `Windows 7` 及以上操作系统。

* 必须安装 `git` 命令行工具。

* `git` 必须配置环境变量。



您需要配置以下配置文件：

* 首先声明，即使你不需要以下配置文件功能，您仍需要创建它，然后它可以不包含任何内容。

* `head.txt`：文件头部，您的文件可能包含一些头部代码，如 `#include <bits/stdc++.h>` 。您可以加入这个头部，之后生成的文件都将去除这个头部。例如：

  `head.txt`：

  ``` cpp
  #include <bits/stdc++.h>
  using namespace std;
  ```

  `example.cpp`：

  ``` cpp
  #include <bits/stdc++.h>
  using namespace std;
  
  void solve() {
  	cout << "hello world!" << endl;
  }
  ```

  `Output`：

  ``` cpp
  void solve() {
  	cout << "hello world!" << endl;
  }
  ```

* `skip.ini`：黑名单条目，如果被搜索到的目录包含黑名单条目中的任意一条，它将被忽略。黑名单条目暂不支持 `正则表达式` 匹配。另外，一些路径被内置地设为过滤：非`*.cpp`文件、`.*`文件和目录。



## 导出格式

程序的导出规范：

* 导出的文件名为 `日期时间.md`，位于目录 `.out`。不支持更改导出目录与导出文件名。
* 导出的 `markdown` 文件中，每个 `cpp` 文件使用一级标题分隔，标题由路径名生成。
* 在 `Typora` 中，您可以设置使用一级标题自动分页导出 `PDF` 这样你的每个 `cpp` 文件都是整页的。但这不在脚本的工作范围内。