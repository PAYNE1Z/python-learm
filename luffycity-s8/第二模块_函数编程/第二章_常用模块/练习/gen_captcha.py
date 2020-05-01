#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/23
# Location: DongGuang
# Desc:     获取一个指定长度的包含必要字符类型的随机验证码

import random
import string

class GetCAPTCHA:
    """获取一个指定长度的包含必要字符类型的随机验证码
     # string 模块各类字符串集：
        string.ascii_lowercase 小写字母
        string.ascii_uppercase 大写字母
        string.ascii_letters   大小写字母
        string.digits          数字
        string.hexdigits       十六进制数
        string.octdigits       八进制数
        string.punctuation     特殊字符
        string.printable       以上所有字符集合
    Example:  文档测试用例
    >>> lens, uppers, lowers, digits, punctuations = 8, 2, 2, 2, 3
    >>> captcha1 = GetCAPTCHA(lens=lens, uppers=uppers, lowers=lowers, digits=digits, punctuations=punctuations)
    >>> v_code = captcha1.get_code()
    参数不合法: 必要字符数大于总长度
    >>> lens, uppers, lowers, digits, punctuations = 8, 'a', '2', 2, 3
    >>> captcha2 = GetCAPTCHA(lens=lens, uppers=uppers, lowers=lowers, digits=digits, punctuations=punctuations)
    Traceback (most recent call last):
        ...
    TypeError: 只接受int类型参数
    >>> lens, uppers, lowers, digits, punctuations = 8, 2, 2, 2, 1
    >>> captcha3 = GetCAPTCHA(lens=lens, uppers=uppers, lowers=lowers, digits=digits, punctuations=punctuations)
    >>> v_code = captcha3.get_code()
    >>> import re
    >>> pl = (re.findall(r'[{}]'.format(string.punctuation), v_code))
    >>> ul = (re.findall(r'[{}]'.format(string.ascii_uppercase), v_code))
    >>> ll = (re.findall(r'[{}]'.format(string.ascii_lowercase), v_code))
    >>> dl = (re.findall(r'[{}]'.format(string.digits), v_code))
    >>> if len(pl) >= punctuations and len(ul) >= uppers and len(ll) >= lowers and len(dl) >= digits: \
    print('验证码符合指定规则')
    验证码符合指定规则
    """

    def __init__(self, lens=6, uppers=0, lowers=0, digits=0, punctuations=0):
        """:param lens: 验证码长度
        :param uppers: 大写字母个数
        :param lowers: 小写字母个数
        :param digits: 数字个数
        :param punctuations: 特殊字符个数
        """
        for arg in [lens, uppers, lowers, digits, punctuations]:
            if not isinstance(arg, int):
                raise TypeError('只接受int类型参数')
        self.lens = lens
        self.str_map = {
            'uppers': (string.ascii_uppercase, uppers),
            'lowers': (string.ascii_lowercase, lowers),
            'digits': (string.digits, digits),
            'punctuations': (string.punctuation, punctuations),
        }

    def get_code(self):
        """生成并返回随机验证码
        :return code
        """
        code = []
        custom_str_len = sum(s[1] for s in self.str_map.values())  # 自定义验证码字符串类型个数
        if custom_str_len <= self.lens:
            self.str_map['fills'] = (string.printable, self.lens - custom_str_len)   # 填充字符
            code.extend(''.join(random.sample(v[0], v[1])) for k, v in self.str_map.items() if v[1])  # 生成随机字符列表
            # 以上获取结果会出现相同类型的字符串永远是靠在一起的情况，所以再做一下处理，打乱一下顺序
            code = list(''.join(code))
            random.shuffle(code)
            return ''.join(code)
        else:
            print('参数不合法: 必要字符数大于总长度')


if __name__ == '__main__':
    import doctest
    # 文档用例测试，python3 gen_captcha.py 运行脚本没有任何输出，说明程序运行结果符合预期
    doctest.testmod()