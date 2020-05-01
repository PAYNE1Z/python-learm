#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/30
# Location: DongGuang
# Desc:     threading多线程应用


"""
编写一个简单的文本处理工具，具备三个任务，
    一个接收用户输入，
    一个将用户输入的内容格式化成大写，
    一个将格式化后的结果存入文件
"""

from threading import Thread
import time


def receive():
    """接收用户输入"""
    while True:
        text = input('>>>: ').strip()
        if text is None: continue
        t2 = Thread(target=text_format, args=(text,))
        t2.start()


def text_format(_text):
    """格式化文本"""
    try:
        format_text = _text.upper()
        print(f'FORMAT: {format_text}', flush=True)
        t3 = Thread(target=save_text, args=(format_text, ))
        t3.start()
    except Exception as e:
        print(e)
        return None


def save_text(data):
    """存入文件"""
    with open('test.txt', 'a', encoding='utf8') as f:
        time.sleep(2)  # 模拟写入延迟
        f.write(f'{data}\n')


if __name__ == "__main__":
    t1 = Thread(target=receive)
    t1.start()