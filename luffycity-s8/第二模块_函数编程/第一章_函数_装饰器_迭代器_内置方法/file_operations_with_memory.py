#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/7
# Location: DongGuang
# Desc:     占用内存的方法修改文件内容，with open() 方式


import os
import sys


def update_file(file_name, old_str, new_str):
    """
    修改文件内容
    :param file_name: 要修改的源文件
    :param old_str: 要被替换的字符串
    :param new_str: 替换后的字符串
    :return:
    """
    # 打开文件(打开多个文件中间用 ',' 分隔)
    with open(file_name, 'r+', encoding='utf8') as f:

        # 读取文件并修改符合条件的内容
        content = f.read().replace(old_str, new_str)  # 将文件内容读到内存,并替换相应字符
        f.seek(0)     # 把光标移到文件开头(read()过后光标已移至文件结尾)
        f.truncate()  # 把文件内容清空
        f.write(content)  # 把修改后的内容写入文件


def main():
    """
    主程序
    :return:
    """
    if len(sys.argv) < 3 or sys.argv[1] in ['-h', '-H', '--help', 'help']:
        exit("Usage: sys.argv[0] old_str new_str filename")
    file_name = sys.argv[3]
    old_str = sys.argv[1]
    new_str = sys.argv[2]
    update_file(file_name, old_str, new_str)


if __name__ == "__main__":
    main()

