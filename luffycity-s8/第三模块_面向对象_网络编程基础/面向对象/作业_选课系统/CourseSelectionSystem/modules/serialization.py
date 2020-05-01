#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/26
# Location: DongGuang
# Desc:     数据序列化


import pickle

class Serialize:
    @staticmethod
    def dump(file, obj):
        if obj:
            with open(file, 'wb') as f:
                pickle.dump(obj, f)

    @staticmethod
    def load(file):
        try:
            with open(file, 'rb') as f:
                data = pickle.load(f)
                return data
        except FileNotFoundError:
            return {}

