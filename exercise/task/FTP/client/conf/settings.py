#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/9
# Location: DongGuang
# Desc:     服务端配置文件

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 服务端地址
SERVER_ADDR = '127.0.0.1'

# 服务端端口
SERVER_PORT = 8888

# 服务器中断时客户端尝试重新连接次数与重试时间间隔
RETRY_CONN_NUM = 10
RETRY_CONN_INTERVAL = 5

# 默认编码 windows:gbk, linux:utf8
# DEFAULT_CODING = 'utf8' if os.name == 'posix' else 'gbk'
DEFAULT_CODING = 'utf8'

# 客户端默认数据下载目录
DEFAULT_DATA_DIR = os.path.join(BASE_DIR, 'data')
