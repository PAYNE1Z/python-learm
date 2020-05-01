#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/8/1
# Location: DongGuang
# Desc:     do the right thing

"""
使用定时器实现一个随机验证码认证
"""

from threading import Timer
import random
import string


class Code:
    def __init__(self, lens=4):
        self.lens = lens
        self.code = None
        self.t = None
        self.get_code()

    def get_code(self, interval=10):
        self.code = self.make_code()
        print('\n', self.code)
        self.t = Timer(interval, self.get_code)
        self.t.start()

    def make_code(self):
        code_lst = random.choices(string.hexdigits, k=self.lens)
        return ''.join(code_lst)

    def check(self):
        while True:
            u_code = input('请输入验证码>>: ').strip()
            if u_code.upper() == self.code.upper():
                print('验证成功')
                self.t.cancel()  # 验证成功，取消线程执行
                break


obj = Code()
obj.check()