#!/usr/bin/evn python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/4/4
# Location: DongGuang
# Desc:     显示颜色字体,只支持linux终端,windows下pychram也能正常显示


class Colored(object):
    """打印高亮颜色字体"""
    # 显示格式: \033[显示方式（1：高亮/0：正常）;前景色;背景色m
    # 只写一个字段表示前景色,背景色默认,以下全为高亮显示
    RED = '\033[0;31m'  # 红色
    GREEN = '\033[0;32m'  # 绿色
    YELLOW = '\033[0;33m'  # 黄色
    BLUE = '\033[0;34m'  # 蓝色

    #: color reset
    RESET = '\033[0m'  # 终端默认颜色

    def color_str(self, colors, s):
        return '{}{}{}'.format(
            getattr(self, colors),
            s,
            self.RESET
        )

    def red(self, s):
        return self.color_str('RED', s)

    def green(self, s):
        return self.color_str('GREEN', s)

    def yellow(self, s):
        return self.color_str('YELLOW', s)

    def blue(self, s):
        return self.color_str('BLUE', s)


