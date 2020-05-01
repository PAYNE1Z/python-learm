#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/18
# Location: DongGuang
# Desc:     进度条生成器

import time
from modules.size_format import SizeUnitFormat
from modules.colored import Colored

colors = Colored()
SizeFormat = SizeUnitFormat()

def progress_bar(length):
    """打印进度条
    \r：   将光标移动到当前行的首位而不换行
    \n：   将光标移动到下一行，并不移动到首位
    \r\n： 将光标移动到下一行首位
    :param length: 总长度
    """
    bar_style = ">"           # 进度条样式
    bar_total_length = 50     # 总共显示多少个进度条样式
    rotate_list = "|/-\\"     # 进度旋转图示
    start_time = time.time()
    size = 0
    while size <= length:
        if size == length:print()  # 大小接收完后打印个空来结束end='\r',不然进度条内容会被清空
        size = yield               # 当前进度需要调用者通过 send()方法传入
        bar_num = bar_style * int(size*(bar_total_length/length))   # 当前进度条长度
        rate = size/length*100     # 当前百分比
        print(colors.yellow('[{}][size:{}][time:{:.2f}s][{}][{:.2f}%]'.format(
            rotate_list[int(rate) % 4],
            SizeFormat.size2human(size),
            time.time() - start_time,
            bar_num,
            rate)), end='\r')
    # print()  # 生成器写在这里不会被执行，所以写在上面


# # 调用示例：
# total_size = 138763400
# p = progress_bar(total_size)
# next(p)
# for i in range(0, total_size+1, 100):
#     p.send(i)
# print('done')
