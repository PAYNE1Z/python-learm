#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/3
# Location: DongGuang
# Desc:     do the right thing


"""
python到底是如何实现继承的，对于你定义的每一个类，
python会计算出一个方法解析顺序(MRO)列表，
这个MRO列表就是一个简单的所有基类的线性顺序列表

为了实现继承,python会在MRO列表上从左到右开始查找基类,
直到找到第一个匹配这个属性的类为止。而
这个MRO列表的构造是通过一个C3线性化算法来实现的。
我们不去深究这个算法的数学原理,它实际上就是合并所有父类的MRO列表并遵循如下三条准则:
    1.子类会先于父类被检查
    2.多个父类会根据它们在列表中的顺序被检查
    3.如果对下一个类存在两个合法的选择,选择第一个父类

在Java和C#中子类只能继承一个父类，而Python中子类可以同时继承多个父类，
如果继承了多个父类，那么属性的查找方式有两种，
分别是：
    经典类：深度优先
    新式类：广度优先
    说明：以上两种优先必须满足一个条件，子类继承的多个父类必须要有一个共同的父类
"""

class A:
    test = 'A'

class B(A):
    test = 'B'
    pass

class C:
    test = 'C'

class D(B):
    test = 'D'
    pass

class E(C):
    test = 'E'

class F(D):
    test = 'F'
    pass

class G(E):
    test = 'G'

class H(F,G):
    test = 'H'
    pass


obj = H()
print(H.__mro__)  # H.mro() 返回H类的MRO列表(继承查找顺序表)
# print(H.__base__)  # 返回当前类的父类(如有多个则为从左往右第一个)
# print(H.__bases__)  # 返回当前类的所有父类
print(obj.test)   # 顺序：H.F.D.B.G.E.C.A.object  广度优先
print(obj.test)   # 如果C类没继承A类：H.F.D.B.A.G.E.C.object  深度优先