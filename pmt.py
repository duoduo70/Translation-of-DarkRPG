#!/usr/bin/python3
r"""
这是一个帮助汉化整合包和使用汉化的程序。
本程序所支持的汉化文件格式被称为 PMT 格式。
通常来说，当发布汉化时，会附带一个使用本程序的指引。
Github 仓库：https://github.com/duoduo70/Translation-of-DarkRPG
用法：

选项:
    -u <汉化文件> <欲将其作用的目录> 使用一个汉化
    -h 显示本文档
    -t <目录> 获取翻译辅助信息
    -v 查看本软件的版本
    --transform <英文目录> <中文目录> 自动转换旧有汉化到 PMT 格式。需要手动处理很多内容。
    --transform-dump <英文目录> <中文目录> 输出关于 --transform 选项的调试信息
"""
import json
import os
import shutil
import sys
import re
import zipfile
import chardet

# Python 的可读性太差了, 语法还哆嗦，真的，我想用 Perl ……
# 还管啥效率啊，能跑起来就成


def replace_in_file(file_path, replacements):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        for replacement in replacements:
            old_content = content
            content = content.replace(
                '"' + replacement["replace"] + '"', '"' + replacement["to"] + '"'
            )
            if old_content != content:
                print(
                    "注入成功："
                    + file_path
                    + ': "'
                    + replacement["replace"]
                    + '" 到 '
                    + '"'
                    + replacement["to"]
                    + '"'
                )

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
    except:
        pass


def print_title(message):
    print("\033[34m:: " + message + "\033[0m")


def print_warning(message):
    print("\033[33m警告：\033[0m" + message)


def print_error(message):
    print("\033[31m错误：\033[0m" + message)


def replace_in_folder(folder_path, replacements):
    print_title("正在注入汉化……")
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            replace_in_file(file_path, replacements)


def contains_chinese(line):
    return any("\u4e00" <= char <= "\u9fff" for char in line)


def find_chinese_files(directory):
    print_title("正在扫描……")
    print("以下是中文字符所在位置的信息：")
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line_number, line in enumerate(f, 1):
                        if contains_chinese(line):
                            print(f"\t文件 {file_path} 的第 {line_number} 行")
            except UnicodeDecodeError:
                print_warning(f"自动跳过 {file_path}，可能不是文本文件或编码不是UTF-8")


def check_config_before_using(config, args):
    print_title("正在检查路径是否错误")
    if not os.path.isdir(args[3]):
        print_error(args[2] + "不是一个文件夹")
        return False
    if "dirname" in config:
        if os.path.basename(args[3]) != config["dirname"]:
            print_warning(
                "你填写的路径可能不是正确的路径，该汉化的作者指引你将汉化使用到这个文件夹："
                + config["dirname"]
            )
        else:
            print("正确无误")
    if "early-init" in config or "lately-init" in config:
        print_warning(
            "该汉化附加了一个 Python 脚本，如果这是恶意脚本，它将足以毁坏您的计算机，请确认您真的相信该汉化包。"
        )
        if "early-init" in config and not os.path.isfile(
            "./" + os.path.dirname(args[2]) + "/" + config["early-init"]
        ):
            print_error(
                "找不到附带的 Python 脚本，该汉化包可能已经损坏："
                + config["early-init"]
            )
            return False
        if "lately-init" in config and not os.path.isfile(
            "./" + os.path.dirname(args[2]) + "/" + config["lately-init"]
        ):
            print_error(
                "找不到附带的 Python 脚本，该汉化包可能已经损坏："
                + config["lately-init"]
            )
            return False
    print("")
    while True:
        confirm_message = input("是否确定注入本汉化？[Y/n]")
        if confirm_message == "y" or confirm_message == "Y" or confirm_message == "":
            return True
        elif confirm_message == "n" or confirm_message == "N":
            return False


def find_chinese_in_quotes(line):
    pattern = re.compile(r'"(?:\\.|[^"\\])*[\u4e00-\u9fa5]+(?:\\.|[^"\\])*"')
    matches = pattern.finditer(line)

    results = []
    for match in matches:
        results.append((match.start(), match.end(), match.group()))

    return results


def get_quoted_substring(line, position):
    if line[position] != '"':
        return '"%PMT_INDEX_ERROR%"'

    start = position
    end = position + 1

    while end < len(line):
        if line[end] == "\\" and end + 1 < len(line) and line[end + 1] == '"':
            end += 2
        elif line[end] == '"':
            return line[start : end + 1]
        else:
            end += 1

    return '"%PMT_CAN_NOT_FOUND_ERROR%"'


def extract_substring(filename, localize_line_number, localize_col_number):
    try:
        with open(filename, "r") as file:
            for line_number, line in enumerate(file, 1):
                if line_number == localize_line_number:
                    return get_quoted_substring(line, localize_col_number)
    except FileNotFoundError:
        return '"%PMT_FILE_NOT_FOUND_ERROR%"'


def transform(inter_path, local_path, dump_mode=False):
    try:
        localize_list = []
        for root, dirs, files in os.walk(local_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line_number, line in enumerate(f, 1):
                            if contains_chinese(line):
                                results = find_chinese_in_quotes(line)
                                for result in results:
                                    localize_list.append(
                                        (
                                            file_path[len(local_path) + 1 :],
                                            line_number,
                                            result[0],
                                            result[2],
                                        )
                                    )
                except UnicodeDecodeError:
                    pass
        if dump_mode:
            print("\n".join(str(i) for i in localize_list))
        else:
            for file_path, line_number, col_number, local_str in localize_list:
                print(
                    '{"replace": '
                    + extract_substring(
                        inter_path + "/" + file_path, line_number, col_number
                    )
                    + ', "to": '
                    + local_str
                    + "},"
                )
    except Exception as e:
        print_warning(
            "由于未知原因，程序收到了一个错误，以上不是全部的条目。请使用 `"
            + sys.argv[0]
            + " --transform-dump "
            + sys.argv[2]
            + " "
            + sys.argv[3]
            + "` 进行调试。"
        )


def move_folders(source_folder, target_folder, folders_to_move):
    # 遍历源文件夹中的所有子文件夹
    sub_folders = next(os.walk(source_folder))[1]
    for folder in sub_folders:
        if folder in folders_to_move:
            print(f"正在移动 '{folder}' 到 '{target_folder}'")
            source_path = os.path.join(source_folder, folder)
            target_path = os.path.join(target_folder, folder)
            # 移动文件夹
            shutil.move(source_path, target_path)


def unzip(config, basedir):
    print_title("正在解压文件")
    for filename in os.listdir(basedir + config["extract-from"]):
        if filename.endswith(".jar"):
            filepath = os.path.join(basedir + config["extract-from"], filename)
            with zipfile.ZipFile(filepath, "r") as zip_ref:
                zip_ref.extractall(basedir + ".pmt-tmp")
            print(f"解压 {filename} 完成")
    print_title("正在移动需要的目录")
    move_folders(
        basedir + ".pmt-tmp/data",
        basedir + config["extract-data-to"],
        config["extract-data"],
    )
    shutil.rmtree(basedir + ".pmt-tmp")


def main():
    try:
        if sys.argv[1] == "-h":
            print(__doc__)
        elif sys.argv[1] == "-u":
            config_path = sys.argv[2]
            print_title("正在列出分包名称")
            if os.path.isdir(config_path):
                print_error("暂不支持导入多个汉化文件")
                return
            else:
                with open(config_path, "r") as file:
                    config = json.load(file)
                print(config["name"] + "\n\t版本：" + config["version"])
                if "extra-info" in config:
                    print("\t 附加信息：" + config["extra-info"])
            if check_config_before_using(config, sys.argv) == False:
                return
            if "early-init" in config:
                print_title("正在执行附加脚本")
                os.system(
                    "python ./"
                    + os.path.dirname(sys.argv[2])
                    + "/"
                    + config["early-init"]
                )
            if "unzip" in config and config["unzip"] == True:
                unzip(config, sys.argv[3] + "/")
            replace_in_folder(sys.argv[3], config["replacements"])
            os.system(
                "python ./" + os.path.dirname(sys.argv[2]) + "/" + config["lately-init"]
            )
            print("汉化注入完成")
        elif sys.argv[1] == "-t":
            find_chinese_files(sys.argv[2])
        elif sys.argv[1] == "--transform":
            transform(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "--transform-dump":
            transform(sys.argv[2], sys.argv[3], True)
        elif sys.argv[1] == "-v":
            print_title("pmt (Plasma's Modpack Translator) 0.1 20240513")
            print(
                "本程序属于公有领域且没有任何担保。\n使用本软件的任何后果由您自己承担。"
            )
        else:
            print(
                '未知选项"'
                + sys.argv[1]
                + '"，请检查你传入的参数，以下是本程序的文档：\n\n'
            )
            print(__doc__)
    except Exception as e:
        print("用法不对或汉化包已损坏，请检查你传入的参数，或使用 -h 选项查看文档：\n")


if __name__ == "__main__":
    main()
