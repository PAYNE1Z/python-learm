#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/4/28
# Location: DongGuang
# Desc:     do the right thing


names = ['old_driver', 'rain', 'jack', 'shanshan', 'peiqi', 'black_girl']
print(names)
names.insert(names.index('black_girl'), 'alex')
print(names)
names[names.index('shanshan')] = '姗姗'
print(names)
names.insert(names.index('rain')+1, ['oldboy', 'oldgirl'])
print(names)
print(names.index('peiqi'))
names.extend([1, 2, 3, 4, 2, 5, 6, 2])
print(names)

# 列表切片
print(names[4:7])      # 打印索引4到7的值
print(names[2:10:2])   # 每隔一个打印索引2到10的值 [2:10:2]后面那个2表示步长
print(names[-3:])      # 打列表最后三个值

# 循环打印列表的索引与值
for i,v in enumerate(names):
    print(i, v)

# 循环打印列表中索引为偶数的索引与值，并把奇数索引的值改为 -1
for i,v in enumerate(names):
    if i % 2:
        print(i, v)
    else:
        names[i] = -1
print(names)

# 取列表中有多个相同值的索引
print("###############")
print(names.index(2))            # 第一个2的index
print(names[names.index(2)+1:])  # 第一个2后面列表切片
# 第二个2在列表切片中的index
print(names[names.index(2)+1:].index(2))
# 第二个2在整个列表中的index (第一个2的index+1+列表切片中2的index)
print(names[names.index(2)+1:].index(2) + names.index(2)+1)

# 商品选购小程序
products = [['iPhone8', 6888], ['MacPro', 14800], ['MI6', 2499], ['Mate20Pro', 5399], ['P20Pro', 4788]]
shop_list = []
exit_flag = False
while not exit_flag:
    print("----------商品列表----------")
    for i in range(0,len(products)):
        print("%s. %s  %s" % (i, products[i][0], products[i][1]))

    user_choose = input("请输入商品编号选择商品, 如要退出请按[q|Q]：")

    if user_choose.isdigit():
        user_choose = int(user_choose)
        if 0 <= user_choose < len(products):
            print("已选商品[%s]" % products[int(user_choose)])
            shop_list.append(products[int(user_choose)])
        else:
            print("没有你选择的商品，请重新选择")
    elif user_choose in ['q', 'Q']:
        if len(shop_list):
            print("----------已选商品----------")
            for i in range(0, len(shop_list)):
                print("%s. %s  %s" % (i, shop_list[i][0], shop_list[i][1]))
        else:
            print('你没有选购商品')
        exit_flag = True

