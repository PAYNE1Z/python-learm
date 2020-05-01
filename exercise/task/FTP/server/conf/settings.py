#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/9
# Location: DongGuang
# Desc:     服务端配置文件

import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 服务端地址
SERVER_ADDR = '127.0.0.1'

# 服务端端口
SERVER_PORT = 8888

# 最大监听链接数(排队长度)
MAX_QUEUE_SIZE = 5

# 接受最大并发连接数
MAX_CONCURRENCY = 10

# 默认编码 windows:gbk, linux:utf8
DEFAULT_CODING = 'utf8' if os.name == 'posix' else 'gbk'

# FTP服务器数据目录
SEVER_DATA_DIR = os.path.join(BASE_DIR, 'data')

# 帐号数据目录
USER_DB_DIR = os.path.join(SEVER_DATA_DIR, 'db')

# 帐号数据文件
USER_DB = os.path.join(USER_DB_DIR, 'userdb.json')

# FTP用户主目录
FTP_USER_DIR = os.path.join(SEVER_DATA_DIR, 'home')

# 日志目录
LOG_PATH = os.path.join(SEVER_DATA_DIR, 'logs')

# 访问日志路径
ACCESS_LOG_FILE = os.path.join(LOG_PATH, 'access.log')

# 错误日志路径
ERROR_LOG_FILE = os.path.join(LOG_PATH, 'error.log')

# 日志级别 DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = logging.INFO

# 日志格式
# 写入文件格式
LOG_TO_FILE_FORMAT = '[%(asctime)s] [%(levelname)s] %(name)s:%(funcName)s:%(lineno)s - %(message)s'
# 写入console格式
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

# 创建相关目录
if not os.path.isdir(USER_DB_DIR): os.makedirs(USER_DB_DIR, exist_ok=True)
if not os.path.isdir(FTP_USER_DIR): os.makedirs(FTP_USER_DIR, exist_ok=True)
if not os.path.isdir(LOG_PATH): os.makedirs(LOG_PATH, exist_ok=True)