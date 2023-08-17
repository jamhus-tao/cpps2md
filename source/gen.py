# cpps2md - 路径生成器
# jamhus_tao @ 2023
import os
from pypinyin import lazy_pinyin as pinyin
import git


PATH_SKIP = ".bin\\skip.ini"  # 黑名单路径
FILE_TYPE = (".cpp", ".md")  # 支持文件类型

skips = []  # 路径黑名单


# 加载黑名单
def load():
    global skips
    with open(PATH_SKIP, "r", encoding="utf-8") as file:
        skips = [__.strip().lower() for __ in file.readlines()]


# 检查是否属于黑名单
def check_skip(s: str) -> bool:
    if s.startswith("."):
        return True
    for _skip_key in skips:
        if _skip_key in s.lower():
            return True
    return False


# 检查类型支持
def check_type(s: str) -> bool:
    if s.endswith(FILE_TYPE):
        return True
    return False


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
