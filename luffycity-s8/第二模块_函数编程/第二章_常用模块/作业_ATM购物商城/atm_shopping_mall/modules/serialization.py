#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/24
# Location: DongGuang
# Desc:     do the right thing

import json


def load_account(file):
    """
    加载帐户信息
    :param file: 帐号文件
    :return:
    """
    with open(file, 'r', encoding='utf8') as f:
        data = json.load(f)
        return data


def dump_account(data, file):
    """
    序列化json数据
    :param data: 要序列化的数据
    :param file: 序列化文件
    :return:
    """
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f)