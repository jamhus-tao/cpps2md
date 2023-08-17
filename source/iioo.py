# cpps2md - 读写缓冲器
# jamhus_tao @ 2023
import os
import time
import git


PATH_HEAD = ".bin\\head.txt"  # 公共头部文本路径
PATH_OUT = ".out"  # 输出文件夹
PATH_FILE = "{}.md".format(time.strftime("%Y%m%d%H%M%S"))  # Markdown 导出路径
PATH_LOG = "{}.log".format(time.strftime("%Y%m%d%H%M%S"))  # 更新日志导出路径
YAML_FRONT_MATTER = """---
title: ACM Code Template
author: Jamhus Tao
header: Jamhus Tao / GreatLiangpi ${today}
footer: ACM Code Template
---
"""


head = ""  # 公共头部文本
content = []  # 目录缓冲
data = []  # 正文缓冲


# 加载头部文本
def load():
    global head
    with open(PATH_HEAD, "r", encoding="utf-8") as file:
        head = file.read()
    head = head.split('\n')
    _i = 0
    while _i < len(head) and (head[_i].lstrip() == '' or head[_i].lstrip().startswith('//')):
        _i += 1
    head = '\n'.join(head[_i:])


# 标题载入正文缓冲
def write_title(title: str):
    data.append("# {}\n".format(title.replace("\\", "::").replace("/", "::").rsplit('.', 1)[0]))
    data.append("\n")


# cpp 格式文本载入正文缓存
def write_cpp_block(block: str):
    if len(head):
        block = block.split('\n')
        _i = 0
        while _i < len(block) and (block[_i].lstrip() == '' or block[_i].lstrip().startswith('//')):
            _i += 1
        block = '\n'.join(block[_i:])
        if block.startswith(head):
            block = block[len(head):]
    block = block.replace("`", "'")
    block = block.strip() + "\n"
    data.append("``` cpp\n")
    data.append(block)
    data.append("```\n")
    data.append("\n")


# markdown 格式文本载入正文缓存
def write_md_block(block: str):
    data.append(block)
    data.append("\n")


def write_block(block: str, file: str):
    if file.endswith(".cpp"):
        write_cpp_block(block)
    elif file.endswith(".md"):
        write_md_block(block)


# 标题载入目录缓存
def add_content(title: str):
    content.append("**{}**\n".format(title.replace("\\", "::").replace("/", "::").rsplit('.', 1)[0]))


# 即时导出生成日志
def add_log_diff(mode: int, path: str):
    _path_log = os.path.join(PATH_OUT, PATH_LOG)
    _file = open(_path_log, "a", encoding="utf-8")
    if mode == git.STATUS_MODIFY:
        _file.write("Modify\t\t{}\n".format(path))
        _file.write("----------------------------------------------------------------\n")
        _file.close()
        git.diff(path, _path_log)
        _file = open(_path_log, "a", encoding="utf-8")
        _file.write("----------------------------------------------------------------\n")
        _file.write("\n\n\n\n")
    elif mode == git.STATUS_DELETE:
        _file.write("Delete\t\t{}\n".format(path))
        _file.write("----------------------------------------------------------------\n")
        _file.write("\n\n\n\n")
    elif mode == git.STATUS_CREATE:
        _file.write("Create\t\t{}\n".format(path))
        _file.write("----------------------------------------------------------------\n")
        _file.write("\n\n\n\n")
    else:
        _file.write("Uncertain\t\t{}\n".format(path))
        _file.write("----------------------------------------------------------------\n")
        _file.write("\n\n\n\n")
    _file.close()


# 清空缓存区
def clear():
    global PATH_FILE, PATH_LOG
    PATH_FILE = "{}.md".format(time.strftime("%Y%m%d%H%M%S"))
    PATH_LOG = "{}.log".format(time.strftime("%Y%m%d%H%M%S"))
    content.clear()
    data.clear()


# 缓存区为空
def empty():
    return not len(data)


# 导出缓存区但不清空
def output(with_content=True):
    if not os.path.exists(PATH_OUT):
        os.mkdir(PATH_OUT)
    with open(os.path.join(PATH_OUT, PATH_FILE), "w", encoding="utf-8") as _file:
        _file.writelines(YAML_FRONT_MATTER)
        if with_content:
            _file.writelines(["# 目录\n", "\n"])
            _file.writelines(content)
            _file.writelines(["\n"])
        _file.writelines(data)
    print("Markdown outputted.")
