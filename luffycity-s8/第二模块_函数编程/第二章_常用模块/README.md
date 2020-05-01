# 第二模块 函数编程
## 第二章 常用模块

##### 1、logging模块有几个日志级别?
    debug, info, warning, error, critical
    
##### 2、请配置logging模块，使其在屏幕和文件里同时打印以下格式的日志
    # 2017-10-18 15:56:26,613 - access - ERROR - account [1234] too many login attempts
```python
import logging

logger = logging.getLogger('access')  # 创建logger对象
logger.setLevel(logging.INFO)   # 设置全局日志级别
log_h = logging.StreamHandler()    # 生成handler对象
# 设置日志格式
log_f = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s [%(thread)d] %(message)s')
logger.addHandler(log_h)   # 将handler绑定到logger
log_h.setFormatter(log_f)   # 给handler设置日志格式

logger.info('too many login attempts')
```

##### 3、json、pickle、shelve三个区别是什么?
    首先，这三个模块都是序列化工具
     1. json是所有语言的序列化工具,优点跨语言、体积小.只能序列化一些基本的数据类型。int\str\list\tuple\dict
     pickle是python语言特有序列化工具，所有数据都能序列化。只能在python中使用，存储数据占空间大.
     shelve模块是一个简单的k,v将内存数据通过文件持久化的模块，可以持久化任何pickle可支持的python数据格式。
     2. 使用方式，json和pickle用法一样，shelve是f = shelve.open('shelve_test')
     
     
##### 4、json的作用是什么?
    json的作用是序列化数据
    序列化是指把内存里的数据类型转变成字符串，以使其能存储到硬盘或通过网络传输到远程，因为硬盘或网络传输时只能接受bytes

##### 5、subprocess执行命令方法有几种?
    a、subprocess.run(*popenargs, input=None, timeout=None, check=False, **kwargs) #官方推荐
    b、subprocess.call(*popenargs, timeout=None, **kwargs) #跟上面实现的内容差不多，另一种写法
    c、subprocess.Popen() #上面各种方法的底层封装
    
#### 6、为什么要设计好目录结构?
    a、可读性高: 不熟悉这个项目的代码的人，一眼就能看懂目录结构，知道程序启动脚本是哪个，测试目录在哪儿，配置文件在哪儿等等。从而非常快速的了解这个项目。
    b、可维护性高: 定义好组织规则后，维护者就能很明确地知道，新增的哪个文件和代码应该放在什么目录之下。这个好处是，随着时间的推移，代码/配置的规模增加，项目结构不会混乱，仍然能够组织良好。

##### 7、打印出命令行的第一个参数。例如：
```python
import sys
print(sys.argv[1])
```

##### 8、代码如下
```python
# Linux当前目录/usr/local/nginx/html/
# 文件名：index.html

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(index.html)))
print(BASE_DIR)

# a、打印的内容是什么?
# /usr/local/nginx

# b、os.path.dirname和os.path.abspath含义是什么?
# os.path.dirname 是取指定文件路径中文件的上一层目录
# os.path.abspath 是取指定文件的绝对路径
```


##### 9、通过configparser模块完成以下功能

    # 文件名my.cnf
    
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
    
```python
import configparser

conf_file = 'my.ini'
config = configparser.ConfigParser()
config.read(conf_file)

# 1、修改时区default-time-zone = '+8:00' 为校准的全球时间 +00:00
config.set('mysqld', 'default-time-zone', '+00:00')

# 2、删除explicit_defaults_for_timestamp = true
config.remove_option('mysqld', 'explicit_defaults_for_timestamp')

# 3、为DEFAULT增加一条character-set-server = utf8
config.set('DEFAULT', 'character-set-server', 'utf8')

# 保存以上修改
with open(conf_file, 'w', encoding='utf8') as cf:
    config.write(cf)
```


##### 10、写一个6位随机验证码程序（使用random模块),要求验证码中至少包含一个数字、一个小写字母、一个大写字母.
```python
import random
import string

code_len = 6
code_list = [random.choice(string.ascii_lowercase), random.choice(string.ascii_uppercase), random.choice(string.digits)]

while True:
    if len(code_list) < code_len:
        code_list.append(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits))
    else:
        break

verification_code = ''.join(code_list)
print(verification_code)
```


##### 11、利用正则表达式提取到 luffycity.com ，内容如下
```python
import re

text = """"
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <title>luffycity.com</title>
</head>
<body>
</body>
</html>
"""
print(re.search('<title>(.*)</title>', text).groups()[0])

```


##### 12、写一个用户登录验证程序，文件如下
    文件：1234.json
    文件内容：{"expire_date": "2021-01-01", "id": 1234, "status": 0, "pay_day": 22, "password": "abc"}
    用户名为json文件名，密码为 password。
    判断是否过期，与expire_date进行对比。
    登陆成功后，打印“登陆成功”，三次登陆失败，status值改为1，并且锁定账号。
    把第12题三次验证的密码进行hashlib加密处理。即：json文件保存为md5的值，然后用md5的值进行验证。
```python
import json
import hashlib
import time


def load_account(file):
    """
    加载帐户信息
    :param file: 帐号文件
    :return:
    """
    with open(file, 'r', encoding='utf8') as f:
        data = json.load(f)
        print(data)
    return data

def dump_account(data, file):
    """
    序列化json数据
    :param data: 要序列化的数据
    :param file: 序列化文件
    :return:
    """
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f)


def make_md5(user_pass):
    """
    检测md5
    :param user_pass: 用户明文密码
    :return: user_pass_md5
    """
    _md5 = hashlib.md5()
    _md5.update(user_pass.encode('utf-8'))
    user_pass_md5 = _md5.hexdigest()
    return user_pass_md5


def main():
    """主函数"""
    global exit_flag
    while not exit_flag:
        u_name = input('User>>>: ')
        if u_name == user_name:
            if account_data['status'] == 1:
                print('该帐号已被锁定')
                return False
            expire_date = account_data['expire_date']
            expire_strptime = time.mktime(time.strptime(expire_date, '%Y-%m-%d'))
            if expire_strptime > time.mktime(time.localtime()):
                p = 0
                while p < max_retry:
                    u_pass = input('Password>>>: ')
                    if make_md5(u_pass) == account_data['password']:
                        print('登陆成功')
                        return True
                    else:
                        print('密码错误，请重试')
                    p += 1
                else:
                    account_data['status'] = 1
                    print('重试次数过多，帐号已被锁定')
                    exit_flag = True
            else:
                print('帐号已过期')
                exit_flag = True
        else:
            print('帐号不存在')
            exit_flag = True
    dump_account(account_data, account_file)


if __name__ == "__main__":
    account_file = '1234.json'
    account_data = load_account(account_file)
    exit_flag = False
    user_name = account_file.split('.')[0]
    max_retry = 3
    main()
```


##### 13、最近luffy买了个tesla，通过转账的形式，并且支付了5%的手续费，tesla价格为75万。文件为json，请用程序实现该转账行为。
    需求如下：
    目录结构为
     .
     ├── account
     │   └── luffy.json
     ├── bin
     │   └── start.py
     └── core
     |   └── withdraw.py
     └── logs
         └── bank.log
    当执行start.py时，出现交互窗口
    
      ------- Luffy Bank ---------
      1.  账户信息
      2.  转账
      3.  提现
    选择1 账户信息 显示luffy的当前账户余额。
    选择2 转账 直接扣掉75万和利息费用并且tesla账户增加75万
    选择3 提现 提现金额应小于等于信用额度，利息为5%，提现金额为用户自定义。
    尝试把上一章的验证用户登陆的装饰器添加到提现和转账的功能上
    对用户转账、登录、提现操作均通过logging模块记录日志,日志文件位置如下
    
    
    本题目请见: luffycity-s8\第二模块_函数编程\第二章_常用模块\练习\tesla
    


。



