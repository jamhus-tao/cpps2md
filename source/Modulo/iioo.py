# cpps2md - 读写缓冲器
# jamhus_tao @ 2023
import os
import time
import json
from Modulo import git


PATH_CFG = ".bin\\config.json"  # 配置路径
PATH_OUT = ".out"  # 输出文件夹
PATH_FILE = ""  # Markdown 导出路径
PATH_LOG = ""  # 更新日志导出路径"
FILE_TYPE = {}  # 支持文件类型
HEAD = ""  # 公共头部文本
YAML_FRONT_MATTER = ""


content = []  # 目录缓冲
data = []  # 正文缓冲


# 加载配置
def init():
    global PATH_FILE, PATH_LOG
    PATH_FILE = "{}.md".format(time.strftime("%Y%m%d%H%M%S"))  # Markdown 导出路径
    PATH_LOG = "{}.log".format(time.strftime("%Y%m%d%H%M%S"))  # 更新日志导出路径"

    with open(PATH_CFG, "r", encoding="utf-8") as _file:
        _data = json.load(_file)

    global FILE_TYPE
    FILE_TYPE = _data["file_type"]

    global HEAD
    HEAD = _data["ignore_head"].split('\n')
    _i = 0
    while _i < len(HEAD) and (HEAD[_i].lstrip() == '' or HEAD[_i].lstrip().startswith('//')):
        _i += 1
    HEAD = '\n'.join(HEAD[_i:])

    global YAML_FRONT_MATTER
    if len(_data["front_matter"]) == 0:
        YAML_FRONT_MATTER = ""
    else:
        YAML_FRONT_MATTER = "---\n{}---\n\n\n\n".format("".join(["{}: {}\n".format(*__) for __ in _data["front_matter"].items()]))


init()


# 标题载入正文缓冲
def write_title(title: str):
    data.append("# {}\n".format(title.replace("\\", "::").replace("/", "::").rsplit('.', 1)[0]))
    data.append("\n")


# 代码格式文本载入正文缓存
def write_code_block(block: str, lang: str):
    if len(HEAD):
        block = block.split('\n')
        _i = 0
        while _i < len(block) and (block[_i].lstrip() == '' or block[_i].lstrip().startswith('//')):
            _i += 1
        block = '\n'.join(block[_i:])
        if block.startswith(HEAD):
            block = block[len(HEAD):]
    block = block.replace("`", "'")
    block = block.strip() + "\n"
    data.append("``` {}\n".format(lang))
    data.append(block)
    data.append("```\n")
    data.append("\n")


# md 格式文本载入正文缓存
def write_org_block(block: str):
    data.append(block)
    data.append("\n")


# 文本载入正文缓存
def write_block(block: str, file: str):
    _type = FILE_TYPE.get(os.path.splitext(file)[1], None)
    if _type is None:
        write_org_block(block)
    else:
        write_code_block(block, _type)


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
