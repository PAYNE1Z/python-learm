#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/7
# Location: DongGuang
# Desc:     占用硬盘的方法修改文件内容，with open()方式


import os
import sys


def update_file(old_file, new_file, old_str, new_str):
    """
    修改文件内容
    :param old_file: 要修改的源文件
    :param new_file: 修改后内容的暂存文件
    :param old_str: 要被替换的字符串
    :param new_str: 替换后的字符串
    :return:
    """
    # 打开文件(打开多个文件中间用 ',' 分隔)
    with open(old_file, 'r', encoding='utf8') as old_f, open(new_file, 'w', encoding='utf8') as new_f:

        # 读取文件并修改符合条件的内容
        for line in old_f:
            if old_str in line:
                line = line.replace(old_str, new_str)
            new_f.write(line)

    # 将新文件覆盖旧文件
    os.remove(old_file)  # (在windows系统中，不能直接使用os.rename方法覆盖)
    os.rename(new_file, old_file)


def main():
    """
    主程序
    :return:
    """
    if len(sys.argv) < 3 or sys.argv[1] in ['-h', '-H', '--help', 'help']:
        exit("Usage: sys.argv[0] old_str new_str filename")
    old_file = sys.argv[3]
    old_str = sys.argv[1]
    new_str = sys.argv[2]
    new_file = "%s.new" % old_file
    update_file(old_file, new_file, old_str, new_str)


if __name__ == "__main__":
    main()