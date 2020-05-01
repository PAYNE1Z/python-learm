#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/6
# Location: DongGuang
# Desc:     do the right thing



"""
exec('a=x+y', globals(), locals())
    参数1：字符串形式的命令
    参数2：全局作用域(字典形式)，如果不指定默认就使用 globals()
    参数3：局部作用域(字典形式), 如果不指定默认就使用 locals()

使用示例: https://www.jianshu.com/p/5caf0415214b
"""


g = {'x': 1, 'y': 2}  # 假设这是全局空间
l = {}  # 假设这是局部空间

# 要执行的命令
cmd = """
global x,m   
x = 10
m = x*y
z = 3
print(m, z)
"""
# exec执行命令，作用于全局变量g 与 局部变量l
# global x,m 会将x,m两个变量名设为全局空间，如果全局空间g中没有就会加到g中
# x = 10 修改全局空间g中x的值
# z = 3  这个变量没有global将会加到局部空间l中，如果l中已存在则修改它
exec(cmd, g, l)
# 执行结果： 20 3

print(l)
# {'z': 3}





# 1、最简单的例子
# 在这个例子中，将program转为python代码执行
program = 'a = 5\nb=10\nprint("Sum =", a+b)'
exec(program)  # 省略 globals 和 locals参数
# Sum = 15


# 2、查看在exec中能够使用的变量和方法
exec('print(dir())')
# 可以看到存在__builtins__，这也是exec调用的字符串中能够识别print()和dir()函数的原因
# ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'a', 'b', 'cmd', 'g', 'l', 'program']


# 3、还可以访问自己定义的函数和变量
def func():
    print("in func")
x = 4
exec('print(dir())')
exec('print(x)')
exec('x=5\nprint(x)')
exec('func()')
# 可以看到调用dir()时，多打印出了'func', 'x'，表明在exec()中可以访问func函数和x变量。
# ['__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'func', 'x']
# 4
# 5
# in func
