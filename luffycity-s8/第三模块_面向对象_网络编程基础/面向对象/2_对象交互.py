#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/6/3
# Location: DongGuang
# Desc:     do the right thing

"""
练习2： 模拟绝地求生定义两个特种兵

要求：
    特种兵需要有昵称、使用枪械、生命值等属性;
    实例化了两个对象，之间可以互相攻击,被击中的一方掉血,血量小于0则判定为死亡
"""

import time

class SpecialArms:
    """特种兵类"""
    hurt = ...  # type: int
    injury_value = {   # 枪械伤害值
        'M416': 23,
        'Groza': 41
    }

    def __init__(self, nickname, firearms, life_value):
        """
        初始化函数
        :param nickname: 昵称
        :param firearms: 枪械
        :param life_value: 生命值
        """
        self.nickname = nickname
        self.firearms = firearms
        self.life_value = life_value

    def attack(self, victim):
        """
        攻击
        :param victim: 被攻击对象
        """
        self.hurt = SpecialArms.injury_value[self.firearms]  # 根据枪械计算伤害值
        victim.life_value -= self.hurt   # 被攻击对象生命值减少
        print('[{}]使用<{}>击中[{}]造成[{}]伤害'.format(self.nickname, self.firearms, victim.nickname, self.hurt))
        print('[{}]当前生命值:[{}]'.format(victim.nickname, victim.life_value))


arms1 = SpecialArms('P城小霸王', 'Groza', 100)  # 实例化两个特种兵对象
arms2 = SpecialArms('机场一把手', 'M416', 100)

game_over = False

while not game_over:
    arms1.attack(arms2)
    arms2.attack(arms1)
    time.sleep(1)
    if arms1.life_value <= 0:  # 生命值小于或等于0为阵亡，退出游戏
        game_over = True
        print('[{}]已阵亡'.format(arms1.nickname))
    if arms2.life_value <= 0:
        game_over = True
        print('[{}]已阵亡'.format(arms2.nickname))


