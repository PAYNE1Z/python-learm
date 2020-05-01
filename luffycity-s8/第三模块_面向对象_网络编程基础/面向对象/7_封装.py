#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/4
# Location: DongGuang
# Desc:     do the right thing


# 1：封装数据
#
# 将数据隐藏起来这不是目的。隐藏起来然后对外提供操作该数据的接口，然后我们可以在接口附加上对该数据操作的限制，以此完成对数据属性操作的严格控制。

class Teacher:
    def __init__(self,name,age):
        self.__name=name
        self.__age=age

    def tell_info(self):
        print('姓名:%s,年龄:%s' %(self.__name,self.__age))

    def set_info(self,name,age):
        if not isinstance(name,str):
            raise TypeError('姓名必须是字符串类型')
        if not isinstance(age,int):
            raise TypeError('年龄必须是整型')
        self.__name=name
        self.__age=age


t=Teacher('egon',18)
t.tell_info()

t.set_info('egon',19)
t.tell_info()


# 2：封装方法：目的是隔离复杂度
# 取款是功能,而这个功能有很多功能组成:插卡、密码认证、输入金额、打印账单、取钱
# 对使用者来说,只需要知道取款这个功能即可,其余功能我们都可以隐藏起来,很明显这么做
# 隔离了复杂度,同时也提升了安全性

class ATM:
    def __card(self):
        print('插卡')

    def __auth(self):
        print('用户认证')

    def __input(self):
        print('输入取款金额')

    def __print_bill(self):
        print('打印账单')

    def __take_money(self):
        print('取款')

    def withdraw(self):
        self.__card()
        self.__auth()
        self.__input()
        self.__print_bill()
        self.__take_money()

a=ATM()
a.withdraw()


# 封装与扩展性
# 类的设计者
class Room:
    def __init__(self,name,owner,width,length,high):
        self.name=name
        self.owner=owner
        self.__width=width
        self.__length=length
        self.__high=high

    def tell_area(self):  # 对外提供的接口，隐藏了内部的实现细节，此时我们想求的是面积
        return self.__width * self.__length

# 使用者
r1=Room('卧室','egon',20,20,20)
r1.tell_area()  # 使用者调用接口tell_area


# 类的设计者，轻松的扩展了功能，而类的使用者完全不需要改变自己的代码
class Room:
    def __init__(self,name,owner,width,length,high):
        self.name=name
        self.owner=owner
        self.__width=width
        self.__length=length
        self.__high=high

    def tell_area(self):
        # 对外提供的接口，隐藏内部实现，此时我们想求的是体积,内部逻辑变了,
        # 只需求修该下列一行就可以很简答的实现,而且外部调用感知不到,仍然使用该方法，但是功能已经变了
        return self.__width * self.__length * self.__high

# 对于仍然在使用tell_area接口的人来说，根本无需改动自己的代码，就可以用上新功能
r1.tell_area()