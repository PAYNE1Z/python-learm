#!/usr/bin/evn python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/4/4
# Location: DongGuang
# Desc:     显示颜色字体

class Colored(object):
    """打印高亮颜色字体"""
    # 显示格式: \033[显示方式（1：高亮/0：正常）;前景色;背景色m
    # 只写一个字段表示前景色,背景色默认,以下全为高亮显示
    HIGHLIGHT_RED = '\033[1;31m'  # 红色
    HIGHLIGHT_GREEN = '\033[1;32m'  # 绿色
    HIGHLIGHT_YELLOW = '\033[1;33m'  # 黄色
    HIGHLIGHT_BLUE = '\033[1;34m'  # 蓝色

    #: color reset
    RESET = '\033[0m'  # 终端默认颜色

    def color_str(self, colors, s):
        return '{}{}{}'.format(
            getattr(self, colors),
            s,
            self.RESET
        )

    def red(self, s):
        return self.color_str('HIGHLIGHT_RED', s)

    def green(self, s):
        return self.color_str('HIGHLIGHT_GREEN', s)

    def yellow(self, s):
        return self.color_str('HIGHLIGHT_YELLOW', s)

    def blue(self, s):
        return self.color_str('HIGHLIGHT_BLUE', s)