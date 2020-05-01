#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/17
# Location: DongGuang
# Desc:     日志记录模块 logging



"""
很多程序都有记录日志的需求，
并且日志中包含的信息即有正常的程序访问日志，还可能有错误、警告等信息输出，
python 的 logging 模块提供了标准的日志接口，你可以通过它存储各种格式的日志，
logging 的日志可以分为:
    debug(), info(), warning(), error() and critical() 5个级别
"""

import logging

logging.basicConfig(filename='log_test.log',  # 日志文件，默认输出到终端
                    level=logging.INFO,       # 打印的日志级别(打印INFO以上级别的日志,debug级别将会忽略)
                    format='%(asctime)s %(filename)s:%(funcName)s:%(lineno)d %(message)s',  # 要打印的日志格式
                    datefmt='%Y/%m/%d %H:%M:%S %p',  # 日期时间格式
                    )
"""
logging 格式字段变量说明：
%(levelno)s	    数字形式的日志级别
%(levelname)s	文本形式的日志级别
%(pathname)s	调用日志输出函数的模块的完整路径名，可能没有
%(filename)s	调用日志输出函数的模块的文件名
%(module)s	    调用日志输出函数的模块名
%(funcName)s	调用日志输出函数的函数名
%(lineno)d	    调用日志输出函数的语句所在的代码行
%(created)f	    当前时间，用UNIX标准的表示时间的浮 点数表示
%(relativeCreated)d	输出日志信息时的，自Logger创建以 来的毫秒数
%(asctime)s	    字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d	    线程ID。可能没有
%(threadName)s	线程名。可能没有
%(process)d	    进程ID。可能没有
%(message)s	    用户输出的消息
"""

def log_test():
    logging.info('in the log_test functions')
log_test()
logging.warning('this is warning message')
logging.critical('service is down')
