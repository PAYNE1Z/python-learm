#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/24
# Location: DongGuang
# Desc:     do the right thing


import hashlib


def make_md5(user_pass):
    """
    检测md5
    :param user_pass: 用户明文密码
    :return: user_pass_md5
    """
    _md5 = hashlib.md5()
    _md5.update(user_pass.encode('utf-8'))
    user_pass_md5 = _md5.hexdigest()
    return user_pass_md5