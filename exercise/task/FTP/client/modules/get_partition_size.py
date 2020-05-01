#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/17
# Location: DongGuang
# Desc:     获取指定磁盘分区可用空间


import ctypes
import os
import platform

def get_partition_free_space(folder):
    """ 获取指定磁盘或分区可用空间
    :param folder: 磁盘分区
    :return bytes单位大小
    """
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize
