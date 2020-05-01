#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/9
# Location: DongGuang
# Desc:     数据序列化


import json

class Serialize:
    @staticmethod
    def dump(file, obj):
        if obj:
            with open(file, 'w') as f:
                json.dump(obj, f)

    @staticmethod
    def dumps(dic):
        data = json.dumps(dic)
        return data

    @staticmethod
    def load(file):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return {}

    @staticmethod
    def loads(_str):
        data = json.loads(_str)
        return data
