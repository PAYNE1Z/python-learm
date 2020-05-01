#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/16
# Location: DongGuang
# Desc:     序列化模块 json pickle

import pickle
import json


data = {'k1':123,'k2':'Hello'}

# json.dumps 将数据通过特殊的形式转换为所有程序语言都认识的字符串
j_str = json.dumps(data)
print(j_str)

# json.loads 将字符串转换为dumps前的数据类型
j_dict = json.loads(j_str)
print(j_dict, type(j_dict))

# json.dump 将数据通过特殊的形式转换为只有python语言认识的字符串，并写入文件
# 写入的是字符串类型
with open('result.json', 'w') as fp:
    json.dump(data,fp)

# json.load 将文件对象中的数据转换为dump前的数据类型
with open('result.json', 'r') as fp:
    j_dict = json.load(fp)
    print(j_dict, type(j_dict))



# pickle.dumps 将数据通过特殊的形式转换为只有python语言认识的字符串
# 写入的是二进制类型
p_str = pickle.dumps(data)
print(p_str)

# pickle.loads 将dumps的数据转换为dumps前的数据类型
pk_dict = pickle.loads(p_str)
print(pk_dict, type(pk_dict))

# pickle.dump 将数据通过特殊的形式转换为只有python语言认识的字符串，并写入文件
with open('result.pk','wb') as fp:
    pickle.dump(data,fp)

# pickle.load 将文件对象中的数据转换为dump前的数据类型
with open('result.pk', 'rb') as fp:
    pk_dict = pickle.load(fp)
    print(pk_dict, type(pk_dict))


