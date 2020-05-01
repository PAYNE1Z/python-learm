#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/9
# Location: DongGuang
# Desc:     嵌套函数与变量作用域


age = 18

def func1():
    global age  # 引入全局变量

    def func2():
        print(age)  # 这里会打印全局的值 18

    func2()   # 在上层函数age定义前执行了嵌套函数
    age = 20  # 这里将age改成了20

func1()
print(age)  # 所以这里会打印20

# 1、如果age 没用global定义，那么会报错，
#    因为func1中的age是在执行func2后才定义，所以在func2中不知道要用哪个age的值
# 2、如果func1中的age在func2执行前定义，那么func2中的age打印值就会是20了
#    因为变量作用域是由内到外，一层一层的找

"""
注意：代码定义完成后，作用域已经生成，作用域链向上查找
"""

name = 'Jack'

def echo_name1():
    name = 'Pony'

    def echo_name2():
        print(name)

    return echo_name2

func = echo_name1()
func()
# 这里应该返回 Pony 因为代码定义后，作用域已经生成，
# 所以即使看起来echo_name2是在函数外执行的，但name依然还是用的它的上层函数的
