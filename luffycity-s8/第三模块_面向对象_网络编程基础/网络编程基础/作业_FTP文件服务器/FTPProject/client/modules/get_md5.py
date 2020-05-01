#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/09
# Location: DongGuang
# Desc:     获取对象的md5值


import hashlib

class GetMD5:
    """获取传入对象的md5值"""
    @staticmethod
    def get_str_md5(text):
        """
        检测md5
        :param text: 用户明文
        :return: md5
        """
        md5_obj = hashlib.md5()
        md5_obj.update(text.encode('utf-8'))
        return md5_obj.hexdigest()

    @staticmethod
    def get_file_md5(file):
        """计算文件的md5
        :param file: 文件
        :return md5
        """
        md5_obj = hashlib.md5()
        try:
            with open(file, 'rb') as f:
                for data in f:
                    md5_obj.update(data)
                return md5_obj.hexdigest()
        except FileNotFoundError as e:
            print(e)
            return False