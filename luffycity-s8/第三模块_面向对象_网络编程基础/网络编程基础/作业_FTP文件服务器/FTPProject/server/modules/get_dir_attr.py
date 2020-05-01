#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/17
# Location: DongGuang
# Desc:     获取指定目录下的属性：文件与目录，大小


import os
from os.path import join, getsize, getmtime
import time
from modules.size_format import SizeUnitFormat

class GetDirAttr:
    """获取指定目录下的文件与目录相关属性"""
    def get_dir_file(self, path):
        """获取指定目录下的所有文件与目录的大小与修改时间,只获取第一层(不获取子目录下的)
        :param path: 目录路径
        :return dir and file list
        """
        SizeFormat = SizeUnitFormat()
        data = []
        total_size = 0
        for _path, _dirs, _files in os.walk(path):
            data.append('\n++++++++++ Dir:[{}]\n'.format(len(_dirs)))
            for _dir in _dirs:
                _dir_path = join(_path, _dir)
                _dir_size = self.get_dir_size(_dir_path)
                total_size += _dir_size
                data.append('  DIR:[{}] {} {}\n'.format(_dir,   # 目录名
                            SizeFormat.size2human(_dir_size),  # 目录大小
                            time.strftime('%Y%m%d/%H:%M:%S', time.localtime(getmtime(_dir_path)))))  # 修改时间
            data.append('---------- File:[{}]\n'.format(len(_files)))
            for _file in _files:
                _file_path = join(_path, _file)
                _file_size = getsize(_file_path)
                total_size += _file_size
                data.append('  FILE:[{}] {} {}\n'.format(_file,
                            SizeFormat.size2human(_file_size),
                            time.strftime('%Y%m%d/%H:%M:%S', time.localtime(getmtime(_file_path)))))
            data.append('========== Total:[{}]; Size:[{}]\n'.format(len(_dirs)+len(_files),
                                                                    SizeFormat.size2human(total_size)))
            return data

    @staticmethod
    def get_dir_size(path):
        """获取目录大小
        :param path: 目录路径
        :return dir_size
        """
        dir_size = 0
        for _path, _dirs, _files in os.walk(path):
            try:
                dir_size += sum([getsize(join(_path, name)) for name in _files])
            except Exception:  # C盘或/根分区有些文件可能没有权限获取
                continue
        return dir_size
