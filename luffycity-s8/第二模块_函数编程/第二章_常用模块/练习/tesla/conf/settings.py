#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/24
# Location: DongGuang
# Desc:     全局配置

import os
import sys

import os
import sys
import logging

# 密码重试次数
PASSWORD_MAX_RETRY = 3
# 转帐手续费率
TRANSFER_FEE_RATE = 0.05
# 提现利率
WITHDRAWAL_RATE = 0.05
# 提现手续费
WITHDRAWAL_FEE_RATE = 0.05
# 日志级别
LOG_LEVEL = logging.INFO
# 日志格式
LOG_TO_FILE_FORMAT = '[%(asctime)s] [%(levelname)s] %(name)s:%(funcName)s:%(lineno)s - %(message)s'
LOG_TO_CONSOLE_FORMAT = '%(message)s'
"""
logging FORMAT 字段变量说明：
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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 帐号文件目录名
ACCOUNT_DIR = 'account'
# 帐号文件绝对路径
ACCOUNT_PATH = r'{}\{}'.format(BASE_DIR, ACCOUNT_DIR)

