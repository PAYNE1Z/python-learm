#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/4/25
# Location: DongGuang
# Desc:     do the right thing



name = input("what you name: ")
sex = input("what you sex[m|w]: ")
age = int(input("how old are you: "))


if sex == "w":
    if age < 28:
        print("我喜欢女生")
    else:
        print("姐弟恋也挺好")
else:
    print("一起来搞基")


