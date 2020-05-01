#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/10
# Location: DongGuang
# Desc:     do the right thing


"""
什么是异常：
    异常是指错误发生的信号，一旦程序出错，并且程序没有处理这个错误，
    那就会抛出异常，并且程序的运行随之终止
    在python中不同的异常可以用不同的类型（python中统一了类与类型，类型即类）去标识，一个异常标识一种错误


错误种类：
    1、语法错误：比如：缩进不规范，缺少括号或引号, 缺少语法符号
    2、逻辑错误：比如: 给非数字字符串使用int方法，对非迭代对象进行迭代，使用未定义的变量，获取不存在的key...


常见异常种类：
    AttributeError 试图访问一个对象没有的树形，比如foo.x，但是foo没有属性x
    IOError 输入/输出异常；基本上是无法打开文件
    ImportError 无法引入模块或包；基本上是路径问题或名称错误
    IndentationError 语法错误（的子类） ；代码没有正确对齐
    IndexError 下标索引超出序列边界，比如当x只有三个元素，却试图访问x[5]
    KeyError 试图访问字典里不存在的键
    KeyboardInterrupt Ctrl+C被按下
    NameError 使用一个还未被赋予对象的变量
    SyntaxError Python代码非法，代码不能编译(个人认为这是语法错误，写错了）
    TypeError 传入对象类型与要求的不符合
    UnboundLocalError 试图访问一个还未被设置的局部变量，基本上是由于另有一个同名的全局变量，
    导致你以为正在访问它
    ValueError 传入一个调用者不期望的值，即使值的类型是正确的

更多异常：
    ArithmeticError
    AssertionError
    AttributeError
    BaseException
    BufferError
    BytesWarning
    DeprecationWarning
    EnvironmentError
    EOFError
    Exception
    FloatingPointError
    FutureWarning
    GeneratorExit
    ImportError
    ImportWarning
    IndentationError
    IndexError
    IOError
    KeyboardInterrupt
    KeyError
    LookupError
    MemoryError
    NameError
    NotImplementedError
    OSError
    OverflowError
    PendingDeprecationWarning
    ReferenceError
    RuntimeError
    RuntimeWarning
    StandardError
    StopIteration
    SyntaxError
    SyntaxWarning
    SystemError
    SystemExit
    TabError
    TypeError
    UnboundLocalError
    UnicodeDecodeError
    UnicodeEncodeError
    UnicodeError
    UnicodeTranslateError
    UnicodeWarning
    UserWarning
    ValueError
    Warning
    ZeroDivisionError
"""


# TypeError:int类型不可迭代
# for i in 3:
#     pass
# TypeError: 'int' object is not iterable


# ValueError
# num=input(">>: ")  # 输入hello
# int(num)
# ValueError: invalid literal for int() with base 10: 'hello'


# NameError
# aaa
# NameError: name 'aaa' is not defined


# IndexError
# l=['egon','aa']
# l[3]
# IndexError: list index out of range


# KeyError
# dic={'name':'egon'}
# dic['age']
# KeyError: 'age'


# AttributeError
# class Foo:pass
# Foo.x
# AttributeError: type object 'Foo' has no attribute 'x'


# ZeroDivisionError:无法完成计算
# res1=1/0
# res2=1+'str'
# ZeroDivisionError: division by zero


# 异常处理： try..except
# 多分支：被监测的代码块抛出的异常有多种可能性，并且我们需要针对每一种异常类型都定制专门的处理逻辑

try:
    print('1........')
    # print(name)   # NameError
    print('2........')
    l = [1,2,3]
    # l[3]          # IndexError
    print('3........')
    d = {}
    # d['name']     # KeyError
    print('4........')
    a = 'hello'
    # int(a)        # ValueError
    print('5........')
    n = 12345
    # for i in n:   # TypeError
    #     print(i)
except NameError as e:
    print(e)
except IndexError as e:
    print(e)
except KeyError as e:
    print(e)
except ValueError as e:
    print(e)
except TypeError as e:
    print(e)


# 万能异常： Exception
# 被监测的代码块抛出的异常有多种可能性,都使用一种处理逻辑
try:
    print('1........')
    # print(name)   # NameError
    print('2........')
    l = [1,2,3]
    # l[3]          # IndexError
    print('3........')
    d = {}
    # d['name']     # KeyError
    print('4........')
    a = 'hello'
    # int(a)        # ValueError
    print('5........')
    n = 12345
    # for i in n:   # TypeError
    #     print(i)
except Exception as e:
    print(e)


# 其它结构：try..except..else..finally
try:
    print('1........')
    # print(name)   # NameError
    print('2........')
    l = [1,2,3]
    # l[3]          # IndexError
    print('3........')
    d = {}
    # d['name']     # KeyError
    print('4........')
    a = 'hello'
    # int(a)        # ValueError
    print('5........')
    n = 12345
    # for i in n:   # TypeError
    #     print(i)
except NameError as e:   # if..elif
    print('NameError:', e)
except IndexError as e:  # if..elif
    print('IndexError:', e)
except Exception as e:   # if..else
    print('其它错误:', e)
else:     # while..else
    print('检测代码块没有发生任何异常时执行')
finally:
    print('不管被检测代码块有无发生异常都会执行')



# 主动触发异常：raise 异常类型(值)
class Foo:
    def __init__(self, name, age):
        if not isinstance(name, str):
            raise TypeError('名字必须为str类型')
        if not isinstance(age, int):
            raise TypeError('年龄必须为int类型')
        self.name = name
        self.age = age

f = Foo('jack', 53)



# 断言: assert 条件,'输出'
d = {'name':'jack', 'age': 53}
assert 'name' in d and 'age' in d, '字典{}中必须要有name与age两个key'.format(d)
print(d['name'])
print(d['age'])



# 自定义异常类型
class MyException(BaseException):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return '<{}>'.format(self.msg)

try:
    raise MyException('自定义的异常类型')
except MyException as e:
    print(e)