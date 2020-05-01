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

from core.ftp_client import FTPClient
from conf import settings

if __name__ == '__main__':
    ftp_client = FTPClient(settings.SERVER_ADDR, settings.SERVER_PORT)
    ftp_client.run()
