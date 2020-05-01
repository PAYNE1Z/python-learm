#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/2
# Location: DongGuang
# Desc:     第一模块 第二章作业<购物车>


"""
基本需求：75%
    1. 启动程序后，输入用户名密码后，让用户输入工资，然后打印商品列表
    2. 允许用户根据商品编号购买商品
    3. 用户选择商品后，检测余额是否够，够就直接扣款，不够就提醒
    4. 可随时退出，退出时，打印已购买商品和余额
    5. 在用户使用过程中， 关键输出，如余额，商品已加入购物车等消息，需高亮显示

升级需求：10%
    1. 用户下一次登录后，输入用户名密码，直接回到上次的状态，即上次消费的余额什么的还是那些，再次登录可继续购买
    2. 允许查询之前的消费记录
"""

import os
import json
import time
from colored import Colored
# colored 模块作用为输出高亮颜色字体


def login():
    """
    帐号登录
    :return:
    """
    input_user = input(color.blue("请输入你的帐号："))
    if input_user == user_name:
        if auth_password('登录', login_pass):
            print(color.green("\n登录成功，欢迎<%s>\n" % input_user))
        else:
            exit(color.red("重试次数过多!!!请稍后再试"))
    else:
        exit(color.red("帐号错误，请重新登录"))


def recharge_balance():
    """
    充值
    :return: 当前余额
    """
    global balance
    re_balance = input(color.blue("\n请输入你的充值金额（小写数字）: "))
    if re_balance.isdigit():
        re_balance = int(re_balance)
        balance += re_balance
        return balance
    else:
        print(color.red('您输入的金额格式不对,充值失败！'))


def format_product_list(plist, title="购物车"):
    """
    格式化打印商品列表
    :param plist: 商品列表 或 购物车列表
    :param title: 商品列表 或 购物车
    :return: 格式化的列表
    """
    print(color.blue(title.center(30, '=')))
    for i, n in enumerate(plist):
        print(color.yellow("%s. %s  %s" % (i, n['name'], n['price'])))


def get_total_price(_shop_car, _price):
    """
    计算选购商品总价
    :param _shop_car: 购物车
    :param _price: 商品总价
    :return: 购物车商品总价
    """
    for i, n in enumerate(_shop_car):
        _price += n['price']
    return int(_price)


def check_balance(_balance, total_shop_price):
    """
    检查余额
    :param _balance: 当前余额
    :param total_shop_price: 当前购物车商品总价
    :return: True or False
    """
    tag = True if _balance >= total_shop_price else False
    return tag


def auth_password(tag, auth_pass):
    """
    验证密码
    :param tag: 密码类型（支付|登录)
    :param auth_pass: 要验证对应类型的密码
    :return: True or False
    """
    count = 0
    while count < 3:
        input_pass = input(color.blue("请输入您的%s密码：" % tag))
        if input_pass == auth_pass:
            return True
        else:
            print(color.red("%s密码错误,请重试：" % tag))
            count += 1
    else:
        return False


def data_dump(file, data):
    """
    序列化存储已加入购物车商品列表与价格与消费记录
    :param file: 购物车、价格、消费记录存入不同文件
    :param data: 要在序列化的数据
    :return
    """
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def data_load(file):
    """
    读取已加入购物车商品与价格
    :param file 购物车、价格、消费记录从不同文件加载
    :return
    """
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def write_shop_log(_shop_car, _balance):
    """
    记录购买消费记录
    :param _shop_car: 当前购物车商品列表
    :param _balance: 当前余额
    :return:
    """
    log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    with open(SHOP_LOG_FILE, 'a', encoding='utf-8') as f:
        f.writelines("%s : \n您购买了如下商品:\n" % log_time)
        for i, n in enumerate(_shop_car):
            f.writelines('%s. %s %s\n' % (i, n['name'], n['price']))
        f.writelines('消费金额：%s\n--------------------\n' % _balance)


def read_shop_log():
    """
    读取购买消费记录
    :return:
    """
    try:
        with open(SHOP_LOG_FILE, 'r', encoding='utf-8') as f:
            print(color.yellow("\n您的消费记录如下：\n%s" % (f.read())))
            go_back = input(color.green('【按任意键返回】:')).strip()
            if go_back:
                pass
    except FileNotFoundError:
        print(color.red('您还没有消费记录\n'))


def update_shop_car(_shop_car):
    """
    更新购物车
    :param _shop_car: 当前购物车
    :return:
    """
    while True:
        format_product_list(_shop_car)
        num = input(color.blue('【请选择要从购物车删除的商品编号：(0-%s) ; 返回:b】：' % (len(_shop_car)-1))).strip()

        if num.isdigit() and int(num) < len(_shop_car):
            num = int(num)
            print(color.yellow('已将商品<%s>从购物车删除!' % _shop_car[num]['name']))
            del _shop_car[num]
        elif num == "b":
            break
        else:
            print(color.red('您购物车中没有所选商品，请重试！'))

        # 购物车为空返回选购列
        if len(_shop_car) < 1:
            print(color.red('\n购物车为空!!!\n'))
            break


def check_out(_shop_car, _shop_price):
    """
    结算
    :param _shop_car: 购买的商品
    :param _shop_price: 购买商品的价格
    :return:
    """
    global exit_flag, balance
    shop_info()
    total_shop_price = get_total_price(_shop_car, _shop_price)

    # 检查余额
    if check_balance(balance, total_shop_price):
        # 支付
        pay = input(color.blue('\n【按任意键返回商品列表；支付请按:p】:')).strip()
        if pay == 'p':
            if auth_password('支付', pay_pass):
                balance -= total_shop_price
                write_shop_log(_shop_car, total_shop_price)
                _shop_car.clear()
                print(color.green("\n支付成功, 您的余额为：%s" % balance))
                go_on = input(color.blue("\n【按任意键继续选购; 退出:q】>>")).strip()
                if go_on == 'q':
                    exit_flag = True
            else:
                print(color.red('\n重试次数过多！支付失败！'))

    # 余额不足=>提供充值与删除购物车商品选项
    else:
        rod = input(color.red("\n【对不起你的余额不足! 充值:r ; 删除已选商品:d】")).strip()
        # 充值
        if rod == 'r':
            recharge_balance()
            print(color.green('\n充值成功，余额：%s' % balance))
        # 修改购物车商品
        elif rod == 'd':
            update_shop_car(_shop_car)


def get_exit_balance():
    """
    获取上次退出时购物车与余额状态
    :return:
    """
    global exit_flag, shop_car
    if os.path.isfile(SHOP_CAR_FILE):
        shop_car = data_load(SHOP_CAR_FILE)
        print(color.yellow("### 上次退出时的购物车与余额状态:"))
        shop_info()
        yes = input(color.blue('\n【按任意键继续，按q退出】：')).strip()
        if yes == 'q':
            exit_flag = True


def shop_info():
    """
    打印当前购物车商品与余额信息
    :return:
    """
    format_product_list(shop_car)
    print(color.yellow('商品总价>>: %s\n帐户余额：%s' % (get_total_price(shop_car, shop_price), balance)))


def get_balance():
    """
    获取帐户余额
    :return:
    """
    global balance
    # 读不到余额文件就表示第一次登录，让用户存入金额
    balance = data_load(BALANCE_FILE) if os.path.isfile(BALANCE_FILE) else recharge_balance()


def go_shopping():
    """
    购物主界面
    :return:
    """
    global exit_flag, balance
    # 打印商品列表
    format_product_list(products, "商品列表")
    choice = input("\n【请选择你购买的商品编号：(0-%s); 查看消费记录:h ; 查看余额:l ; 查看购物车:s ; 退出:q】："
                   % (len(products)-1)).strip()

    # 判断输入为数字则选择商品并加入购物车
    if choice.isdigit():
        choice = int(choice)
        if choice < len(products):
            shop_car.append(products[choice])
            print(color.yellow("\n已添加商品<%s>到购物车\n" % products[choice]['name']))
        else:
            print(color.red("\n您输入的商品编号不存在，请重新输入："))

    # 查看余额
    elif choice == "l":
        print(color.green('\n您的余额为：%s\n' % balance))
        go_back = input(color.green('【按任意键返回】:')).strip()
        if go_back:
            pass

    # 查看购物车
    elif choice == "s":
        if shop_car:
            check_out(shop_car, shop_price)
        else:
            print(color.green('\n当前购物车为空，快去挑选商品吧\n'))

    # 查看消费记录
    elif choice == 'h':
        read_shop_log()

    # 退出
    elif choice == 'q':
        exit_flag = True

    # 其它无效选项
    else:
        print(color.red('\n没有这个选项，请重新选择\n'))


def main():
    """程序主入口"""
    global balance
    login()
    get_balance()
    get_exit_balance()
    while not exit_flag:
        go_shopping()
    else:
        data_dump('shop_car.json', shop_car)
        data_dump('balance.json', balance)
        print(color.green("\n您当前购物车与余额状态:\n"))
        shop_info()
        time.sleep(0.5)
        exit(color.yellow("\n欢迎下次光临"))


# 商品列表
products = [
    {"name": "电脑", "price": 1999},
    {"name": "鼠标", "price": 10},
    {"name": "游艇", "price": 20},
    {"name": "美女", "price": 998},
]

# 常量
SHOP_LOG_FILE = "shop_log.txt"
SHOP_CAR_FILE = "shop_car.json"
BALANCE_FILE = "balance.json"

# 变量
user_name = "jack"
pay_pass = "123456"
login_pass = "abc123"
shop_price = 0
balance = 0
shop_car = []
exit_flag = False


if __name__ == "__main__":
    color = Colored()
    main()