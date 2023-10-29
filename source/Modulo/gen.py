# cpps2md - 路径生成器
# jamhus_tao @ 2023
import os
import re
import json
from pypinyin import lazy_pinyin as pinyin
from Modulo import git


PATH_CFG = ".bin\\config.json"  # 配置路径
FILE_TYPE = {}  # 支持文件类型
SKIP_WITH_REGEX = True  # 使用正则匹配文件名
SKIPS = []  # 路径黑名单


# 加载配置
def init():
    with open(PATH_CFG, "r", encoding="utf-8") as _file:
        _data = json.load(_file)

    global FILE_TYPE
    FILE_TYPE = _data["file_type"]

    global SKIP_WITH_REGEX
    SKIP_WITH_REGEX = _data["skip"]["regex"]

    global SKIPS
    SKIPS = _data["skip"]["list"]


init()


# 检查是否属于黑名单
def check_skip(s: str) -> bool:
    if s.startswith("."):
        return True
    if SKIP_WITH_REGEX:
        for _skip_key in SKIPS:
            if re.match(_skip_key, s.lower()):
                return True
    else:
        for _skip_key in SKIPS:
            if _skip_key in s.lower():
                return True
    return False


# 检查类型支持
def check_type(s: str) -> bool:
    return s.endswith(tuple(FILE_TYPE))


# 排序函数
def key_sort_path(fp: str, path: str):
    return os.path.isfile(os.path.join(fp, path)), "".join(pinyin(path.upper()))


# 路径生成器
def walk(md: bool, fp='.'):
    # 路径生成器 - git status 支持
    def _gen_filepath_1(fp='.'):
        for _mode, _filepath in sorted(git.status(fp), key=lambda __: key_sort_path(fp, __[1])):
            _full_path = os.path.join(fp, _filepath)
            if not check_skip(_filepath):
                if not os.path.exists(_full_path) or os.path.isfile(_full_path):
                    if check_type(_full_path):
                        yield _mode, _full_path[2:]
                else:
                    yield from _gen_filepath_2(_full_path, _mode)

    # 路径生成器 - 全路径筛选
    def _gen_filepath_2(fp='.', mode=git.STATUS_UNKNOWN):
        for _filepath in sorted(os.listdir(fp), key=lambda __: key_sort_path(fp, __)):
            _full_path = os.path.join(fp, _filepath)
            if not check_skip(_filepath):
                if os.path.isfile(_full_path):
                    if check_type(_full_path):
                        yield mode, _full_path[2:]
                else:
                    yield from _gen_filepath_2(_full_path, mode)

    # 选择模式
    if md:
        yield from _gen_filepath_1(fp)
    else:
        yield from _gen_filepath_2(fp)
