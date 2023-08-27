# cpps2md - git链接器
# jamhus_tao @ 2023
import os
import time
import subprocess


STATUS_MODIFY = 1
STATUS_DELETE = 2
STATUS_CREATE = 3
STATUS_UNKNOWN = 4

PATH_GIT = ".git.jamhus"
PATH_IGNORE = ".gitignore"


def cmd(s: str):
    subprocess.run("git \"--git-dir={}\" --work-tree=. {}".format(PATH_GIT, s.lstrip("git ")))


def exists():
    if os.path.isdir(PATH_GIT):
        return True
    return False


def init():
    subprocess.run(["git", "--git-dir={}".format(PATH_GIT), "--work-tree=.", "init", "-q"], stdout=subprocess.PIPE)
    with open(PATH_IGNORE, "w", encoding="utf-8") as _file:
        _file.write(".*\n")
    subprocess.run(["attrib", PATH_GIT, "+h"], stdout=subprocess.PIPE)
    subprocess.run(["attrib", PATH_IGNORE, "+h"], stdout=subprocess.PIPE)
    print("Git initialized.")


def commit():
    subprocess.run(["git", "--git-dir={}".format(PATH_GIT), "--work-tree=.", "add", "-A"], stdout=subprocess.PIPE)
    subprocess.run(
        ["git", "--git-dir={}".format(PATH_GIT), "--work-tree=.", "commit", "-m", time.strftime("Auto %Y%m%d%H%M%S")],
        stdout=subprocess.PIPE
    )
    print("Git committed.")


def status(s: str):
    _ret = subprocess.run(
        ["git", "--git-dir={}".format(PATH_GIT), "--work-tree=.", "status", "-s", s],
        stdout=subprocess.PIPE
    ).stdout.decode("utf-8").split('\n')[:-1]
    _res = []
    for _item in _ret:
        _opt = _item[:3]
        if _opt == " M ":
            _opt = STATUS_MODIFY
        elif _opt == " D ":
            _opt = STATUS_DELETE
        elif _opt == "?? ":
            _opt = STATUS_CREATE
        else:
            _opt = STATUS_UNKNOWN
        _path = _item[3:].strip("\"")
        _path_decoded = []
        _i = 0
        while _i < len(_path):
            if _path[_i] == '\\':
                _path_decoded.append(int(_path[_i + 1: _i + 4], 8))
                _i += 4
            else:
                _path_decoded.append(ord(_path[_i]))
                _i += 1
        _path_decoded = bytes(_path_decoded).decode("utf-8")
        _res.append((_opt, _path_decoded))
    return _res


def diff(s: str, fp: str):
    subprocess.run(
        ["git", "--git-dir={}".format(PATH_GIT), "--work-tree=.", "diff", s],
        stdout=open(fp, "a", encoding="utf-8")
    )
