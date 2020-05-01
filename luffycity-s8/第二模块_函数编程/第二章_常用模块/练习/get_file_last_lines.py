#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/29
# Location: DongGuang
# Desc:     获取文件最后几行


import chardet
import os

def get_file_encodig(file):
    """
    攻取文件编码格式
    :param file: 文件
    :return: coding
    """
    with open('file.txt', 'rb') as f:
        coding_ret = chardet.detect(f.read(4096))
        print(coding_ret)
        return coding_ret.get('encoding')


def get_num_lines(file, lines):
    """
    获取文件最后几行内容
    :param file:  文件
    :param lines:   行数
    :return: 最后lines 或 None
    """
    file_coding = get_file_encodig(file)

    try:
        file_size = os.path.getsize(file)
        if file_size == 0:
            return None

        with open(file, 'rb') as f:
            pass

    except FileNotFoundError:
        exit('{}: 文件不存在'.format(file))

get_num_lines('file.txt', 1)




