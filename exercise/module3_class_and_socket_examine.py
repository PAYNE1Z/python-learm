#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/7/27
# Location: DongGuang
# Desc:     do the right thing


# 1.编写一个学生类，要求有一个计数器的属性，统计总共实例化了多少个学生

class Student:
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count += 1

    def __str__(self):
        return f'name is {self.name}'

    @property
    def get_count(self):
        return self.count


s1 = Student('jack')
s2 = Student('pony')
s3 = Student('robin')
print(s1, s2, s3)
print('共创建了{}个实例'.format(s1.get_count))

# 2.
# 编写游戏角色交互
# 要求：
#
# Garen, 所属阵营Demacia, 具有昵称，生命值200，攻击力100，具备攻击敌人的技能
# Riven, 所属阵营Noxus, 具有昵称，生命值100，攻击力200，具备攻击敌人的技能
# 交互: Garen对象攻击了Riven对象


class Hero:
    """英雄类"""
    def __init__(self, team, name, live, attack_value):
        self.team = team
        self.name = name
        self.live = live
        self.attack_value = attack_value

    def attack(self, obj):
        """攻击方法
        :param obj: 攻击对象"""
        print('{} attack {} attack_value:[{}]'.format(self.name, obj.name, self.attack_value))
        print('{} live value is {}'.format(obj.name, obj.live - self.attack_value))


garen = Hero('Demacia', 'garen', 200, 100)
riven = Hero('Noxus', 'riven', 100, 200)

garen.attack(riven)