#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/25
# Location: DongGuang
# Desc:     商城


import os
import copy
import datetime
from conf import settings
from modules.colored import Colored
from modules import login
from modules import serialization
from modules.logger import log
from atm.core import repayment
from modules.login import password_auth

color = Colored()

def format_product_list(plist, title="购物车"):
    """
    格式化打印商品列表
    :param plist: 商品列表 或 购物车列表
    :param title: 商品列表 或 购物车
    :return: 格式化的列表
    """
    print(color.blue(title.center(30, '=')))
    for i, n in enumerate(plist):
        print(color.yellow("""{}. {}  {}""".format(i, n['name'], n['price'])))


def get_total_price(_shop_car):
    """
    计算选购商品总价
    :param _shop_car: 购物车
    :return: 购物车商品总价
    """
    total_price = 0
    for i, n in enumerate(_shop_car):
        total_price += n['price']
    return int(total_price)


def update_shop_car():
    """
    更新购物车
    :return:
    """
    while True:
        format_product_list(shop_car)
        num = input(color.blue('[请选择要从购物车删除的商品编号：(0-%s) ; 返回:b]：'.format(len(shop_car)-1))).strip()

        if num.isdigit() and int(num) < len(shop_car):
            num = int(num)
            print(color.yellow('已将商品<%s>从购物车删除!' % shop_car[num]['name']))
            del shop_car[num]
        elif num == "b":
            break
        else:
            print(color.red('您购物车中没有所选商品，请重试！'))

        # 购物车为空返回选购列
        if len(shop_car) < 1:
            print(color.red('\n购物车为空!!!\n'))
            break


def load_shop_car_status(file):
    """
    加载购物车与余额状态
    :param file: 文件路径
    :return:
    """
    global shop_car
    shop_car = serialization.load_account(file)
    print(color.yellow("### 上次退出时的购物车与余额状态:"))
    shop_info()
    input(color.blue('按任意键继续'))


def load_product():
    """加载商品数据"""
    global products
    db = r'{}\data\products.db'.format(settings.BASE_DIR)
    try:
        with open(db, 'r', encoding='utf8') as f:
            for line in f:
                products.append(eval(line))
            return products
    except FileNotFoundError:
        log(log_type, 'both').error('商品数据库文件[{}]不存在'.format(db))


def load_last_shop_record(file, lines):
    """
    加载最近消费记录
    :param file: 记录文件
    :param lines: 要查看的记录条数
    :return:
    """
    # linux可以调用tail命令取最后几条记录
    # records = subprocess.run('tail -n {} {}'.format(lines, file),stderr=subprocess.PIPE,stdout=subprocess.PIPE,
    #                         check=True, shell=True)
    try:
        with open(file, 'r', encoding='utf8') as f:
            all_records = f.readlines()
            last_records = all_records[-lines:] if len(all_records) > lines else all_records
            for i in last_records:
                if len(i) > 10:  # 避免文件中有空行导致报错
                    record = eval(i)
                    print('\n++++++++\n消费时间: [{}]; 消费金额: [{}]'.format(record['time'], record['price']))
                    print('购买商品:')
                    for p in record['list']:
                        print('{} {}'.format(p['name'], p['price']))
            input('按任意键返回商城>>:')
    except FileNotFoundError:
        print('您还没有消费记录')
        log(log_type, 'file').error('消费记录[{}]文件不存在'.format(file))


def shop_info():
    """
    打印当前购物车商品与余额信息
    :return:
    """
    format_product_list(shop_car)
    print(color.yellow('商品总价>>: {}\n帐户余额：{}'.format(get_total_price(shop_car), user_data['amount'])))


def go_shopping():
    """购物主界面"""
    global exit_flag, shop_car, products, user_data

    while not exit_flag:
        # 打印商品列表
        format_product_list(products, "红太阳购物中心")
        choice = input("\n[请选择你购买的商品编号：(0-%s); 查看消费记录:h ; 查看余额:l ; 查看购物车:s ; 退出:q]："
                       % (len(products)-1)).strip()

        # 判断输入为数字则选择商品并加入购物车
        if choice.isdigit():
            choice = int(choice)
            if choice < len(products):
                shop_car.append(products[choice])
                print(color.yellow("\n已添加商品<{}>到购物车\n".format(products[choice]['name'])))
            else:
                print(color.red("\n您输入的商品编号不存在，请重新输入："))

        # 查看余额
        elif choice.upper() == "L":
            print(color.green('\n您的余额为：{}\n'.format(user_data['amount'])))

        # 查看购物车
        elif choice.upper() == "S":
            if shop_car:
                shop_info()  # 列出购物车商品
                while True:
                    _pay = input(color.blue('\n[按任意键返回商品列表；结算请按:[p|P]:')).strip()

                    if _pay.upper() == 'P':  # 支付
                        # 检查余额
                        total_shop_price = get_total_price(shop_car)
                        if user_data['amount'] >= total_shop_price:
                            log(log_type, 'file').info('[{}]购买商品:[{}]; 花费金额:[{}]'.format(
                                user, shop_car, total_shop_price))

                            if password_auth(user, user_data, user_db_file):  # 支付接口
                                user_data['amount'] -= total_shop_price
                                serialization.dump_account(user_data, user_db_file)  # （扣款后）保存更改后的数据

                                # 打印日志
                                log(log_type, 'both').info('成功支付[{}],[{}]帐户余额为:[{}]'.format(
                                    total_shop_price, user, user_data['amount']))
                                shop_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
                                shop_record = {"time": shop_time, "list": shop_car, "price": total_shop_price}

                                # 保存消费记录
                                with open(records_file, 'a+', encoding='utf8') as f:
                                    f.write('{}\n'.format(str(shop_record)))
                                shop_car.clear()  # 支付成功后清空购物车
                                break
                        else:
                            # 余额不足=>提供充值与删除购物车商品选项
                            choice = input(color.yellow('余额不足：输入[r]还款充值; 输入[c]修改购物车商品>>: '))
                            if choice.upper() == 'R':
                                repayment.repayment_(user_data, user)  # 还款接口
                            elif choice.upper() == 'C':
                                update_shop_car()  # 修改购物车商品
                    else:
                        break

            else:
                print(color.green('\n当前购物车还没有商品，快去挑选商品吧\n'))

        # 查看消费记录
        elif choice.upper() == 'H':
            load_last_shop_record(records_file, 3)

        # 退出
        elif choice.upper() == 'Q':
            if shop_car:
                # 如果购物车不为空，则把数据序列化到硬盘
                serialization.dump_account(shop_car, status_file)
                log(log_type, 'file').info('当前购物车商品:{},已序列化到硬盘'.format(shop_car))
            log(log_type, 'both').info('[{}]退出商城,欢迎下次光临'.format(user))
            exit_flag = True

        # 其它无效选项
        else:
            print(color.red('\n没有这个选项，请重新选择\n'))


@login.auth('user')
def main(data, user_db):
    """程序主入口"""
    global user_data, user, shop_car, products, status_file, records_file, user_db_file, exit_flag, log_type
    exit_flag = False
    products = []
    log_type = 'mall'
    user_data = copy.deepcopy(data)
    user = os.path.basename(user_db).split('.')[0]
    user_db_file = user_db
    shop_car = []
    products = load_product()  # 加载商品数据
    status_file = r'{}\{}\{}_shop_car.json'.format(settings.BASE_DIR, settings.SHOP_CAR_STATUS_DIR, user)
    records_file = r'{}\{}\{}_records.txt'.format(settings.BASE_DIR, settings.CONSUMPTION_RECORDS_DIR, user)

    if os.path.isfile(status_file):
        load_shop_car_status(status_file)  # 列出上次退出时购物车中的商品
    else:
        log(log_type, 'file').error('购物车状态文件[{}]不存在'.format(user_db_file))

    while not exit_flag:
        go_shopping()
