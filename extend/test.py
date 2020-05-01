#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/4/30
# Location: DongGuang
# Desc:     do the right thing

# 商品如下：li 允许用户添加商品 用户输入序号显示内容
# li = ["手机", "电脑", '鼠标垫', '游艇']
# choice_list = []
# exit_flag = False
# while not exit_flag:
#     print('商品列表'.center(30, '='))
#     for i, v in enumerate(li):
#         print("%s.\t%s" % (i, v))
#     choice = input("请输入商品编号选择商品[退出请按q] ：")
#     if choice.isdigit():
#         choice = int(choice)
#     if choice == 'q':
#         print('已添加的商品有：%s' % choice_list)
#         exit_flag = True
#     elif choice >= len(li):
#         print('编号不存在，请重新输入:')
#         continue
#     else:
#         choice_list.append(li[choice])
#         print('[%s]已添加' % li[choice])


# import time
# for n in (100000, 200000, 300000, 400000):
#     data = b'x'*n
#     start = time.time()
#     b = data
#     while b:
#         b = b[1:]
#     print('bytes', n, time.time()-start)
#
# for n in (100000, 200000, 300000, 400000):
#     data = b'x'*n
#     start = time.time()
#     b = memoryview(data)
#     while b:
#         b = b[1:]
#     print('memoryview', n, time.time()-start)

#
# assert [1,2,3],'is none'
#
# from math import sqrt
#
#
# def is_prime(n):
#     """判断素数的函数"""
#     assert n > 0
#     x = int(sqrt(n))  # 求n的平方根
#     # N = 根号N * 根号N
#     # N的因数除了根号N，其他都是成对存在的，且必定一个大于根号N一个小于根号N
#     # 假设N不是质数，有个因数大于根号N（不是N本身）
#     # 则N必定有一个与之对应的小于根号N的因数
#     # 也就是说，如果2到根号N都没有N的因数，那么对应的根号N到N - 1
#     # 都没有N的因数，N就是个质数
#     for factor in range(2, x + 1):
#         if n % factor == 0:
#             return False
#     return True if n != 1 else False
#
#
# def main():
#     file_names = ('a.txt', 'b.txt', 'c.txt')
#     fs_list = []
#     try:
#         for filename in file_names:
#             fs_list.append(open(filename, 'w', encoding='utf-8'))
#             # 同时打开多个文件的骚操作
#         for number in range(1, 10000):
#             if is_prime(number):
#                 if number < 100:
#                     fs_list[0].write(str(number) + '\n')
#                 elif number < 1000:
#                     fs_list[1].write(str(number) + '\n')
#                 else:
#                     fs_list[2].write(str(number) + '\n')
#     except IOError as ex:
#         print(ex)
#         print('写文件时发生错误!')
#     finally:
#         for fs in fs_list:
#             fs.close()
#     print('操作完成!')
#
#
# if __name__ == '__main__':
#     main()


# def summation(x, y):
#     """求传入参数的和"""
#     print('%s+%s= %s' % (x, y, x+y))
#
# summation(10, 23)


# def update_file(file, old_str, new_str):
#     """修改文件指定内容"""
#     try:
#         with open(file, 'r+', encoding='utf-8') as f:
#             data = f.read().replace(old_str, new_str)
#             f.seek(0)
#             f.truncate()
#             f.write(data)
#     except FileNotFoundError:
#         print('文件不存在')
#
# update_file('test.txt', '我心永恒', '以父之名')

# def check_none(data):
#     """检查某个对象(list,str,tuple)中是否有''空字符"""
#     for s in data:
#         if s == '' or s == ' ':
#             print('{}中有空字符'.format(data))
#             break
#
# a = 'Pony is CEO'
# b = ['a', '', 'b', 'd']
# c = ('', 2, 4, ' ')
# check_none(a)
# check_none(b)
# check_none(c)

# def change_dict_value(d):
#     """
#     检查传入字典的每一个value的长度,如果大于2，
#     那么仅保留前两个长度的内容，并将新内容返回给调用者
#     """
#     for k in d:
#         value = str(d[k])
#         if len(value) > 2:
#             d[k] = value[:2]
#     return d
#
# org_dict = {'name': 'Pony', 'password': 'abc123', 'dept': 'IT', 'age': 48}
# new_dict = change_dict_value(org_dict)
# print(new_dict)


# 写函数，返回一个扑克牌列表，里面有52项，每一项是一个元组
# 例如：[(Spade, A), (Heart, A), (Club, 2) ... (Diamond, K)]

# def make_poker():
#     """
#     生成一副扑克牌
#     :return poker_list: [(Spade, A), (Heart, A), (Club, 2) ... (Diamond, K)]
#     """
#     poker_suit = ['Spade', 'Heart', 'Club', 'Diamond']
#     poker_face = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
#     poker_list = []
#     for suit in poker_suit:
#         for face in poker_face:
#             poker_list.append((suit, face))
#     return poker_list
#
# print(make_poker())


### 写函数，传入n个数，返回字典{'max':最大值,'min':最小值}
# 例如:min_max(2,5,7,8,4)
# 返回:{'max':8,'min':2}

# def max_min(*args):
#     """找出传入参数中的最大值与最小值"""
#     data = {}
#     args_list = sorted(args)
#     data['max'] = args_list[-1]
#     data['min'] = args_list[0]
#     return data
#
# print(max_min(34,3,4,5,33,22,1))


### 写函数,专门计算图形的面积其中嵌套函数,计算圆的面积,正方形的面积和长方形的面积
# 调用函数area('圆形',圆半径) 返回圆的面积
# 调用函数area('正方形',边长) 返回正方形的面积
# 调用函数area('长方形',长,宽) 返回长方形的面积

# def area_calc(graph_type, *args):
#     """
#     根据传入参数计算相关图形面积
#     :param graph_type: 图形类型
#     :param args: 图形参数
#     :return: area : 面积
#     """
#     def roundness(radius):              # 圆形
#         print(pow(radius, 2) * 3.14)    # πr²
#
#     def square(len_side):               # 正方形
#         print(pow(len_side, 2))         # a*a or a²
#
#     def long_side(long, wide):          # 长方形
#         print(long * wide)              # a*b
#
#     if graph_type in ['roundness', 'square', 'long_side']:
#         if len(args) == 1:
#             locals()[graph_type](args[0])
#         elif len(args) == 2:
#             locals()[graph_type](args[0], args[1])
#     else:
#         print('不支持的图形类型：%s' % graph_type)
#
# area_calc('roundness', 10)
# area_calc('square', 12)
# area_calc('long_side', 5, 6)
# area_calc('long_side')
# area_calc('abc', 12)


### 写函数，传入一个参数n，返回n的阶乘
# 例如:cal(7)
# 计算7*6*5*4*3*2*1

# def cal(num):
#     """
#     计算传入参数的阶乘
#     计算公式：n! = n*(n-1)!
#     如：4! = 4 * 3!   展开： 4! = 4*3*2*1
#     """
#     if num == 1:
#         return 1
#     return num * cal(num-1)
#
# print(cal(10))


###  通过生成器写一个日志调用方法， 支持以下功能
# 根据指令向屏幕输出日志
# 根据指令向文件输出日志
# 根据指令同时向文件&屏幕输出日志
# 以上日志格式如下
# 2017-10-19 22:07:38 [1] test log db backup 3
# 2017-10-19 22:07:40 [2] user alex login success
# 注意：其中[1],[2]是指自日志方法第几次调用，每调用一次输出一条日志

# import time
#
# def logger(filename, channel='file'):
#     """
#     日志方法
#     :param filename: log filename
#     :param channel: 输出的目的地，屏幕(terminal)，文件(file)，屏幕+文件(both)
#     :return:
#     """
#     n = 0
#     while True:
#         msg = yield
#         n += 1     # 记录日志条数
#         log_msg = "{} [{}] {}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), n, msg)
#         if channel in ['file', 'both']:  # 写入文件
#             try:
#                 with open(filename, 'a', encoding='utf-8') as f:
#                     f.write('{}\n'.format(log_msg))
#             except FileNotFoundError:
#                 print('文件不存在')
#         if channel in ['terminal', 'both']:  # 打印到terminal
#             print(log_msg)
#
#
# log_obj = logger(filename="web.log",channel='both')  # 初始化
# log_obj.__next__()                                   # 唤醒生成器
# log_obj.send('user alex login success')              # 发送消息
# log_obj.send('user alex logout')                     # 发送消息
# log_obj.send('user jack login success')              # 发送消息


# name=['alex','wupeiqi','yuanhao','nezha']
# new_list = list(map(lambda n: '{}_sb'.format(n), name))
# print(new_list)


# 用filter函数处理数字列表，将列表中所有的偶数筛选出来
# """
# filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回一个迭代器对象，如果要转换为列表，可以使用 list() 来转换。
# 该接收两个参数，第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判，
# 然后返回 True 或 False，最后将返回 True 的元素放到新列表中。
# """
# num = [1,3,5,6,7,8]
#
# def is_even_number(n):
#     return n % 2 == 0
#
# new_num = list(filter(is_even_number, num))  # python2 中直接返回列表；python3 中返回迭代器对象
# print(new_num)


# 如下，每个小字典的name对应股票名字，shares对应多少股，price对应股票的价格
# portfolio = [
#     {'name': 'IBM', 'shares': 100, 'price': 91.1},
#     {'name': 'AAPL', 'shares': 50, 'price': 543.22},
#     {'name': 'FB', 'shares': 200, 'price': 21.09},
#     {'name': 'HPQ', 'shares': 35, 'price': 31.75},
#     {'name': 'YHOO', 'shares': 45, 'price': 16.35},
#     {'name': 'ACME', 'shares': 75, 'price': 115.65}
# ]
#
# # a.计算购买每支股票的总价
# stock_price = map(lambda d:(d['name'],d['shares']*d['price']), portfolio)
# print(list(stock_price))
#
# # b.用filter过滤出，单价大于100的股票有哪些
# price_gt_100 = filter(lambda d:d['price']>100, portfolio)
# print(list(price_gt_100))


# 5、有如下列表,请将以字母“a”开头的元素的首字母改为大写字母；
# li = ['alex', 'egon', 'smith', 'pizza', 'alen']
# for i in range(len(li)):
#     if li[i][0] == 'a':
#         li[i] = li[i].capitalize()
#     else:
#         continue
# print(li)


##### 7、有如下列表,请以列表中每个元素的第二个字母倒序排序；
# li = ['alex', 'egon', 'smith', 'pizza', 'alen']
# li = sorted(li, key=lambda l:l[1], reverse=True)
# print(li)


##### 8、有名为poetry.txt的文件，其内容如下，请删除第三行；
# 昔人已乘黄鹤去，此地空余黄鹤楼。
# 黄鹤一去不复返，白云千载空悠悠。
# 晴川历历汉阳树，芳草萋萋鹦鹉洲。
# 日暮乡关何处是？烟波江上使人愁。

# import os
# file = 'poetry.txt'
# new_file = '{}.new'.format(file)
#
# with open(file, 'r', encoding='utf8') as of, open(new_file, 'w', encoding='utf8') as nf:
#     n = 1
#     for line in of:
#         if n != 3:
#             nf.write(line)
#         else:
#             nf.write('')
#         n += 1
#
# os.replace(new_file, file)


# import os
#
# account_file = 'user_info.txt'
# delete_id = '100003'
# temp_file = '{}.new'.format(account_file)
#
# with open(account_file, 'r+', encoding='utf8') as of, open(temp_file, 'w', encoding='utf8') as nf:
#     for line in of:
#         if line.split(',')[1].strip() == delete_id:
#             nf.write('')
#         else:
#             nf.writelines(line)
# os.replace(temp_file, account_file)


# import time
#
# def run_time(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         func(*args)
#         end_time = time.time()
#         print('Run time: {}'.format(end_time - start_time))
#     return wrapper
#
# @run_time
# def foo(user):
#     time.sleep(0.5)
#     print('Hi: [{}],this is foo'.format(user))
#
# foo('Jack Ma')


# 文件名my.cnf
"""
[DEFAULT]

[client]
port = 3306
socket = /data/mysql_3306/mysql.sock

[mysqld]
explicit_defaults_for_timestamp = true
port = 3306
socket = /data/mysql_3306/mysql.sock
back_log = 80
basedir = /usr/local/mysql
tmpdir = /tmp
datadir = /data/mysql_3306
default-time-zone = '+8:00'
"""
#
# import configparser
#
# conf_file = 'my.ini'
# config = configparser.ConfigParser()
# config.read(conf_file)
#
#
# print(config.sections())
# # 1、修改时区default-time-zone = '+8:00' 为校准的全球时间 +00:00
# print(config['mysqld']['default-time-zone'])
# config.set('mysqld', 'default-time-zone', '+00:00')
# with open(conf_file, 'w', encoding='utf8') as cf:
#     config.write(cf)
#
# # 2、删除explicit_defaults_for_timestamp = true
# config.remove_option('mysqld', 'explicit_defaults_for_timestamp')
# with open(conf_file, 'w', encoding='utf8') as cf:
#     config.write(cf)
#
# # 3、为DEFAULT增加一条character-set-server = utf8
# config.set('DEFAULT', 'character-set-server', 'utf8')
# with open(conf_file, 'w', encoding='utf8') as cf:
#     config.write(cf)


# 写一个6位随机验证码程序（使用random模块), 要求验证码中至少包含一个数字、一个小写字母、一个大写字母.
# import random
# import string
#
# code_len = 6
# code_list = [random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase), random.choice(string.digits)]
#
# while True:
#     if len(code_list) < code_len:
#         code_list.append(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits))
#     else:
#         break
#
# verification_code = ''.join(code_list)
# print(verification_code)


##### 11、利用正则表达式提取到 luffycity.com ，内容如下
# import re
# text = """"
# <!DOCTYPE html>
# <html lang="en">
# <head>
#    <meta charset="UTF-8">
#    <title>luffycity.com</title>
# </head>
# <body>
# </body>
# </html>
# """
# print(re.search('<title>(.*)</title>', text).groups()[0])


# 文件：1234.json
# 文件内容：{"expire_date": "2021-01-01", "id": 1234, "status": 0, "pay_day": 22, "password": "abc"}
# 用户名为json文件名，密码为 password。
# 判断是否过期，与expire_date进行对比。
# 登陆成功后，打印“登陆成功”，三次登陆失败，status值改为1，并且锁定账号。
# 把第12题三次验证的密码进行hashlib加密处理。即：json文件保存为md5的值，然后用md5的值进行验证。

# import json
# import hashlib
# import time
#
#
# def load_account(file):
#     """
#     加载帐户信息
#     :param file: 帐号文件
#     :return:
#     """
#     with open(file, 'r', encoding='utf8') as f:
#         data = json.load(f)
#         print(data)
#     return data
#
# def dump_account(data, file):
#     """
#     序列化json数据
#     :param data: 要序列化的数据
#     :param file: 序列化文件
#     :return:
#     """
#     with open(file, 'w', encoding='utf8') as f:
#         json.dump(data, f)
#
#
# def make_md5(user_pass):
#     """
#     检测md5
#     :param user_pass: 用户明文密码
#     :return: user_pass_md5
#     """
#     _md5 = hashlib.md5()
#     _md5.update(user_pass.encode('utf-8'))
#     user_pass_md5 = _md5.hexdigest()
#     return user_pass_md5
#
#
# def main():
#     """主函数"""
#     global exit_flag
#     while not exit_flag:
#         u_name = input('User>>>: ')
#         if u_name == user_name:
#             if account_data['status'] == 1:
#                 print('该帐号已被锁定')
#                 return False
#             expire_date = account_data['expire_date']
#             expire_strptime = time.mktime(time.strptime(expire_date, '%Y-%m-%d'))
#             if expire_strptime > time.mktime(time.localtime()):
#                 p = 0
#                 while p < max_retry:
#                     u_pass = input('Password>>>: ')
#                     if make_md5(u_pass) == account_data['password']:
#                         print('登陆成功')
#                         return True
#                     else:
#                         print('密码错误，请重试')
#                     p += 1
#                 else:
#                     account_data['status'] = 1
#                     print('重试次数过多，帐号已被锁定')
#                     exit_flag = True
#             else:
#                 print('帐号已过期')
#                 exit_flag = True
#         else:
#             print('帐号不存在')
#             exit_flag = True
#     dump_account(account_data, account_file)
#
#
# if __name__ == "__main__":
#     account_file = '1234.json'
#     account_data = load_account(account_file)
#     exit_flag = False
#     user_name = account_file.split('.')[0]
#     max_retry = 3
#     main()


##### 13、最近luffy买了个tesla，通过转账的形式，并且支付了5%的手续费，tesla价格为75万。文件为json，请用程序实现该转账行为。

"""
需求如下：
目录结构为
.
├── account
│   ├── luffy.json
│   └── tesla.json
└── bin
    └── start.py

当执行start.py时，出现交互窗口

------- LuffyBank - --------
1.账户信息
2.转账

选择1 账户信息 显示luffy的当前账户余额。
选择2 转账 直接扣掉75万和利息费用并且tesla账户增加75万
"""

# import json
#
# luffy_db = 'luffy.json'
# tesla_db = 'tesla.json'


# import json
#
# with open('1234.txt', 'r', encoding='utf8') as f:
#     # data = json.load(f)
#     for i in f:
#         for k in eval(i):
#             print(k, eval(i)[k])
#
# a = {"price": 89, "time": "2019-05-28 15:46:45", "list": [{"price": 89, "name": "鼠标"}]}
#
# with open('1234.txt', 'a', encoding='utf8') as f:
#     f.write('{}\n'.format(str(a)))


# with open('a.txt', 'a', encoding='utf8') as f:
#     a = f.read()
#     print(a)

# li = [1,2,3,4,5,6,7,8,9,10]
# a = [i*2 for i in filter(lambda x:x>5, range(10))]
# print(a)

# s = slice(-1, 3, -2)
# s2 = slice(0, 12, 2)
# s3 = slice(None, None, 2)
# print(li[s])
# print(li[s2])
# print(li[s3])

# a = 10
# b = 20
# c = 30
# g = {'a': 6, 'b': 8}
# t = {'b':100, 'c': 10}
# print(eval('a+b', g))
# print(eval('a+b+c', g, t))

# a = [1, 2, 3]
# b = [4, 5, 6]
# c = [7, 8, 9]
# zz = zip(a, b, c)
# print(zz)
# x, y, z = zip(*zz)
# print(x)
# print(y)
# print(z)

# ret = ['{}{}{}'.format(x,y,z) for x in range(1,7) for y in range(1,7) for z in range(1,7)]
# print(ret)
# print(len(ret))
#
# ret = [x*2 for x in range(10) if x > 5]
# print(ret)
# import os
# print(os.listdir('.'))

# def triangles():
#     p = [1]
#     while True:
#         yield p
#         p = [1] + [p[x] + p[x+1] for x in range(len(p)-1)] + [1]
#
# ret = triangles()
#
# n = 0
# for i in ret:
#     print(i)
#     n += 1
#     if n == 10:
#         break
#
#
# # [1]
# # [1,1]
# # [1,2,1]
# # [1,3,3,1]
# # [1,4,6,4,1]

from functools import reduce

# def str2float(s):
#     for a in s:
#         if a == '.': continue
#         try:
#             float(a)
#         except ValueError:
#             exit('{}中的{}不是一个数字'.format(s, a))
#     num_map = dict(list(zip(map(str, range(10)), range(10))))
#     return num_map[s]
#
#
# print('str2float(\'123.456\') =', str2float('123.456'))
# if abs(str2float('123.456') - 123.456) < 0.00001:
#     print('测试成功!')
# else:
#     print('测试失败!')


# import sys
# import pickle
#
# data = 'admin|admin|manager'
#
# class save:
#     def dump(self):
#         with open('test.pk', 'wb') as f:
#             pickle.dump(data, f)
#             pickle.dump(data, f)
#             pickle.dump(data, f)
#
#     def load(self):
#         with open('test.pk', 'rb') as f:
#             count = 0
#             while True:
#                 count += 1
#                 try:
#                     obj = pickle.load(f)
#                     print(count, obj)
#                 except EOFError:
#                     break
#
# for i in sys.modules[__name__]:
#     print(i)

#
# class foo:
#     print('in the foo')
#
# class bar:
#     print('in the bar')
# data = {'foo': foo, 'bar': bar}
#
# for num, key in enumerate(data, 1):
#     print(num, key)
#     data[key]()
#
# import pickle
# # data = {'admin':{'pwd':'admin', 'type':'Manager'}}
# with open('1.pk', 'wb') as f:
#     pickle.dump(data, f)
#
# with open('1.pk', 'rb') as f:
#     d = pickle.load(f)
#     print(d)


# alist = [2,4,5,6,8,7]
#
# i = 0
# for var in alist:
#     i += 1
#     if var % 2 == 0:
#         alist.remove(var)
#     print(i)
# print(alist)


# li = [1,2,3,5]
# def temp_lambda():
#     temp = [lambda x:i*x for i in range(4)]
#     return temp
#
# for some_lambda in temp_lambda():
#     print(some_lambda(2))

# def temp_lambda():
#     temp = []
#     for i in li:
#         temp.append(lambda x:x+i)
#         yield temp
#
# for la in temp_lambda():
#     for l in la:
#         print(l(2))

#
# class Foo:
#     def __init__(self, name):
#         self.name = name
#
#     def echo(self):
#         print('echo {}'.format(self.name))
#
# obj1 = Foo('jack')
# obj2 = Foo('jack')
# print(obj1, obj2)
# print(id(obj1), id(obj2))
# print(obj1 is obj2)

# with open('test.txt', 'w', encoding='utf8') as f:
#     f.write('hello'*50)
#
# with open('test.txt', 'r+', encoding='utf8') as f:
#     f.truncate()
#     data = f.read()
#     print(data)

#
# import struct
# import json
#
# d = {"a":200,"b":300}
# d_json = json.dumps(d)
# print('d_json: ', d_json)
# d_bytes = bytes(d_json, encoding='utf8')
# print('d_bytes: ', d_bytes)
# a = struct.pack('i', len(d_bytes))
# print(a, type(a), len(a))
#
# b = struct.unpack('i', a)
# b_json


# def multipliers():
#     return [lambda x : i * x for i in range(4)]
# print([m(2) for m in multipliers()])
#
# num = 5
# def func():
#     num = 10
#     print('func', num)
#
# def func2():
#     print('func2', num)
# func()
# func2()
#
# import time
#
# def timer(fun):
#     def run(n):
#         print(n)
#         s = time.time()
#         fun(n)
#         e = time.time()
#         print(s,e)
#         r = e - s
#         print('{} run time: {}'.format(fun.__name__, r))
#     return run
#
#
# @timer
# def func(num):
#     s = 'first'
#     for i in range(num):
#         s += 'luffy'
#         print(id(s))
#     print(s)
#
# @timer
# def func2(num):
#     s = 'first'
#     print(s + 'luffy' * num)
#
# func(10)
# func2(10)

# import time
# for i in range(101):
#     time.sleep(0.1)
#     mark = '#'*int(i/10)
#     print(mark, end='\r')


# 1 在不改变列表中数据排列结构的前提下，找出以下列表中最接近最大值和最小值的平均值 的数
li = [-100, 1, 3, 2, 7, 6, 120, 121, 140, 23, 411, 99, 243, 33, 85, 56]

# 2 写一个configparser模块的应用小示例
# 文件名my.cnf
"""
[DEFAULT]

[client]
port = 3306
socket = /data/mysql_3306/mysql.sock

[mysqld]
explicit_defaults_for_timestamp = true
port = 3306
socket = /data/mysql_3306/mysql.sock
back_log = 80
basedir = /usr/local/mysql
tmpdir = /tmp
datadir = /data/mysql_3306
default-time-zone = '+8:00'
"""


# import configparser
#
# conf_file = 'my.ini'
# config = configparser.ConfigParser()
# config.read(conf_file)
#
# # 1、修改时区default-time-zone = '+8:00' 为校准的全球时间 +00:00
# config.set('mysqld', 'default-time-zone', '+00:00')
#
# # 2、删除explicit_defaults_for_timestamp = true
# config.remove_option('mysqld', 'explicit_defaults_for_timestamp')
#
# # 3、为DEFAULT增加一条character-set-server = utf8
# config.set('DEFAULT', 'character-set-server', 'utf8')
#
# # 保存以上修改
# with open(conf_file, 'w', encoding='utf8') as cf:
#     config.write(cf)


# 3 利用random模块写一个6位的随机验证码，验证码内包含字母、数字（随机出现）

#
# def calc(a, b, c, d=1, e=2):
#     return (a+b)*(c-d)+e
#
# print(calc(1, 2, 3, 4, 5))
# print(calc(1, 2, 3))
# # print(calc(1, 2))
# print(calc(1, 2, 3, e=4))
# print(calc(e=4,c=5, a=2, b=3))
# print(calc(1, 2, 3, d=5, 4))
# def func(a):
#     print(a)
#     print(b)
#     b=9			# 如果这一行注释了会发生什么？为什么？
#
# b = 6
# func(3)

# class Student:
#     """学生类"""
#     count = 0
#
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#         Student.count += 1
#
#     def __str__(self):
#         return f'My name is {self.name}, {self.age} years old'
#
#     @classmethod
#     def get_count(cls):
#         return {cls.count}
#
#
# s1 = Student('Jack', 53)
# s2 = Student('Pony', 45)
# s3 = Student('Robin', 47)
# print(Student.get_count())


# class Dog(object):
#
#     def __init__(self, name):
#         self.name = name
#
#     @property
#     def eat(self):
#         return f'{self.name} is eating'
#         # print(" %s is eating" % self.name)
#
#
# d = Dog("dog")
# print(d.eat)

