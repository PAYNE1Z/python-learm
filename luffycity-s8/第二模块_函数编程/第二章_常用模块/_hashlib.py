#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/16
# Location: DongGuang
# Desc:     加密模块 hashlib




import hashlib

m = hashlib.md5()
m.update(b"Hello")
m.update(b"It's me")
print(m.digest())
m.update(b"It's been a long time since last time we ...")

print(m.digest())  # 2进制格式hash
print(len(m.hexdigest()))  # 16进制格式hash

'''
def digest(self, *args, **kwargs): # real signature unknown
    """ Return the digest value as a string of binary data. """
    pass

def hexdigest(self, *args, **kwargs): # real signature unknown
    """ Return the digest value as a string of hexadecimal digits. """
    pass

'''

import hashlib

# ######## md5 ########

_hash = hashlib.md5()
_hash.update('admin')
print(_hash.hexdigest())

# ######## sha1 ########

_hash = hashlib.sha1()
_hash.update('admin')
print(_hash.hexdigest())

# ######## sha256 ########

_hash = hashlib.sha256()
_hash.update('admin')
print(_hash.hexdigest())


# ######## sha384 ########

_hash = hashlib.sha384()
_hash.update('admin')
print(_hash.hexdigest())

# ######## sha512 ########

_hash = hashlib.sha512()
_hash.update('admin')
print(_hash.hexdigest())