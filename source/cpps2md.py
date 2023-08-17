# cpps2md - cpp目录树 转 Markdown
# jamhus_tao @ 2023
import os
import sys
import gen
import git
import iioo


VERSION = "1.3.5"
MODE_NORMAL = 0
MODE_COMMAND = 1
MODE_ARGUMENT = 2

ABOUT_MESSAGE = """
#:          cpps2md - V{}
Developer:  Jamhus Tao
Last:       2023/05/15
1.1.0       Origin.
1.2.0       Support to generate a folder of C++ source files into one Markdown file for the first time.
1.3.0       Support for incremental template export based on git for the first time.
1.3.3       Append Command Mode. Type "Cmd" to enter and use git command and others in the application.
1.3.4       Append Quick Mode. You can drag and drop the icon of files to the application to export. \
Note folder isn't supported. And you can use "-c" / "--cmd" with shell start to enter the Command Mode quickly.
1.3.5       pdfOutlineOddPage tool is added which is separated from cpps2md. \
It can make all the first level outline of pdf keeping on odd pages. You can drag and drop the pdf to the tool to start or run directly.
""".format(VERSION)


# 打印关于信息
def about():
    print(ABOUT_MESSAGE)


# 递交打印文本到内存 并显示 粗略信息
def upload(md: bool):
    _modified_only = md
    iioo.clear()
    for _mode, _path in gen.walk(False):
        iioo.add_content(_path)
    for _mode, _path in gen.walk(_modified_only):
        _empty = False
        if _mode != git.STATUS_DELETE:
            if _mode == git.STATUS_MODIFY:
                print("Modify:          {}".format(_path))
            elif _mode == git.STATUS_CREATE:
                print("Create:          {}".format(_path))
            else:
                print("Collect:         {}".format(_path))
            iioo.write_title(_path)
            with open(_path, "r", encoding="utf-8") as src:
                _block = src.read()
            iioo.write_block(_block, _path)
        else:
            print("Delete:          {}".format(_path))
    print()

    if iioo.empty():
        print("There is nothing to update.")
        print()


# 将打印文本生成文件
def output(md: bool):
    _modified_only = md
    if not git.exists():
        git.init()
        _modified_only = False

    if iioo.empty():
        print("There is nothing to output.")
        print()
    else:
        print("Submitting...")
        if _modified_only:
            for _mode, _path in gen.walk(True):
                iioo.add_log_diff(_mode, _path)
        iioo.output()
        git.commit()
        print("Finished. Saved as {}\\{}".format(iioo.PATH_OUT, iioo.PATH_FILE))
        print()
        os.startfile(os.path.join(iioo.PATH_OUT, iioo.PATH_FILE))


# 一键模式
def normal():
    upload(modified_only)
    if not iioo.empty():
        input("Confirm to output> ")
        print()
        output(modified_only)


# 命令模式, 允许用户像命令行一样操作, 接入 git 命令
def command():
    print("Command mode supports all the git command and others using \"help\" to show.")
    print()
    _modified_only = False
    while True:
        _x = input("(Cmd)> ").lower()
        print()
        if _x == "help":
            print("help        to show help")
            print("git         follow with the full git command.")
            print("reload      show the reload list for all the sources.")
            print("upload      show the upload list compared with the last version.")
            print("output      output as a file depending on the last \"reload\" / \"upload\".")
            print("exit        to exit")
            print()
        elif _x.startswith("git "):
            git.cmd(_x)
            print()
        elif _x == "reload":
            _modified_only = False
            upload(False)
        elif _x == "upload":
            _modified_only = True
            upload(True)
        elif _x == "output":
            output(_modified_only)
        elif _x == "exit":
            exit(0)
        else:
            print("Unknown Command.")
            print()


# 快速模式, 程序使用命令行参数打开时, 这里参数必须是文件路径
# 但如果有 -c / --cmd 参数快速进入命令模式
def argument():
    _paths = [__ for __ in sys.argv[1:]]
    for _path in _paths:
        if not gen.check_type(_path):
            print("Unsupported:     {}".format(_path))
        elif gen.check_skip(_path):
            print("Skipped:         {}".format(_path))
        elif not os.path.isfile(_path):
            print("NotFound:        {}".format(_path))
        else:
            print("Collect:         {}".format(_path))
            _title = _path.rsplit('/', 1)[-1].rsplit('\\', 1)[-1]
            iioo.add_content(_title)
            iioo.write_title(_title)
            with open(_path, "r", encoding="utf-8") as src:
                _block = src.read()
            iioo.write_block(_block, _path)
    print()
    if iioo.empty():
        print("There is nothing to output.")
        print()
    else:
        print("Submitting...")
        iioo.output()
        print("Finished. Saved as {}\\{}".format(iioo.PATH_OUT, iioo.PATH_FILE))
        print()
        os.startfile(os.path.join(iioo.PATH_OUT, iioo.PATH_FILE))


if __name__ == '__main__':
    print("cpps2md powered by Jamhus Tao, V{}".format(VERSION))
    print()

    os.chdir("..")

    gen.load()
    iioo.load()

    if "-c" in sys.argv or "--cmd" in sys.argv:
        mode = MODE_COMMAND
    elif len(sys.argv) > 1:
        mode = MODE_ARGUMENT
    else:
        print("Check the modification, and collect the modified sources only? (Y/N)")
        print("Or \"Cmd\" to enter the command mode.")
        print("Or \"About\" to show more about the application.")
        print()
        while True:
            x = input("> ").lower()
            if x == "cmd":
                mode = MODE_COMMAND
                break
            elif x == "about":
                about()
            elif x == "exit":
                exit(0)
            elif x.startswith("y"):
                modified_only = True
                mode = MODE_NORMAL
                break
            elif x.startswith("n"):
                modified_only = False
                mode = MODE_NORMAL
                break
            else:
                print("Invalid Input.")
            print()
        print()

    if mode == MODE_NORMAL:
        normal()
    elif mode == MODE_COMMAND:
        command()
    elif mode == MODE_ARGUMENT:
        argument()

    input("Exit > ")
