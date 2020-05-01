#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/10
# Location: DongGuang
# Desc:     存储字节大小单位转换


class SizeUnitFormat:
    """存储字节大小单位转换"""
    units = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')

    def __init__(self):
        self.unit_map = self.get_unit_value_map()

    @staticmethod
    def is_number(int_str):
        """检测字符串是否是数字类型"""
        try:
            return int(int_str)
        except ValueError:
            print('请输入数字类型')
            return False

    def get_unit_value_map(self):
        """使用位运算生成单位值对应表"""
        prefix = {}
        for i, s in enumerate(self.units):  # i=0, s='K'; i=1, s='M' ...
            prefix[s] = 1 << (i + 1) * 10  # {'K': 1左移10位为(2**10) 1024, 'M': 1左移20位为(2**20) 1048576, ...}
        return prefix

    def size2human(self, n):
        """将字节大小转换为可读性高的带单位的值
        :param n: 要转换的值
        :return 带单位的值
        """
        for s in reversed(self.units):  # Y,Z,E,P,T,G,M,K
            if n >= self.unit_map[s]:
                value = float(n) / self.unit_map[s]
                return '%.2f%s' % (value, s)
        return '%sB' % n   # 小于1024单位为B，直接返回

    def human2size(self, str_value):
        """将带单位的字符串大小转换为字节大小
        :param str_value: 字符串值 eg: 520K,200M,1G
        :return 字节大小数值
        """
        unit = str_value[-1].upper()  # 截取单位
        value = self.is_number(str_value.strip(unit))  # 截取数值
        bytes_size = value * self.unit_map[unit]
        return bytes_size
