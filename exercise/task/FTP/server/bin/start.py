#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/15
# Location: DongGuang
# Desc:     运行入口


import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from modules.make_account import make_account
from core.ftp_server import FTPServer
from conf import settings


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == 'create_user':
            make_account()
        if sys.argv[1] == 'run':
            ftp_server = FTPServer(settings.SERVER_ADDR, settings.SERVER_PORT)
            ftp_server.run()
    else:
        script_name = os.path.basename(sys.argv[0])
        print("""Usage:
            python3 {} create_user : 创建登录帐号
            python3 {} run : 运行FTP服务
            """.format(script_name, script_name))