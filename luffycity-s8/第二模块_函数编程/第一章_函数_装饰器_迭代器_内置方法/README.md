# 第二模块 函数编程
## 第一章 函数 装饰器 迭代器 内置方法

### 一、文件处理相关
#### 1、编码问题
    a、请说明 python2 与 python3 中的默认编码是什么？
        Python2：ASCII
        Python3: UTF-8
    
    b、为什么会出现中文乱码？你能列举出现乱码的情况有哪几种？
        1> Python 解释器默认编码与文件源编码不一致
        2> Python 解释器编码与 terminal(系统)编码不一致
        ---
        #coding:utf-8 #.py文件是什么编码就需要告诉python用什么编码去读取这个.py文件。
        sys.stdout.encoding，默认就是locale的编码，print会用sys.stdout.encoding去encode()成字节流，交给terminal显示。所以locale需要与terminal一致，才能正确print打印出中文。
        sys.setdefaultencoding(‘utf8’)，用于指定str.encode() str.decode()的默认编码，默认是ascii。
        以下几种(local 为软件运行时的语言环境):
         终端为UTF-8，locale为zh_CN.GBK
         终端为UTF-8，locale为zh_CN.UTF-8
         终端为GBK，locale为zh_CN.GBK
         终端为GBK，locale为zh_CN.UTF-8
            
    c、如何进行编码转换?
        字符串在python内部中是采用unicode的编码方式，所以其他语言先decode转换成unicode编码，再encode转换成utf8编码
        Unicode -> encode 编码 -> GBK/UTF-8
        GBK/UTF-8 -> decode 解码 -> Unicode
    
    d、#-*-coding:utf-8-*- 的作用是什么?
        用以告诉 Python 解释器本程序文件中的代码字符串以 UTF-8 格式进行编码 

    e、解释 Python2 bytes vs Python3 bytes 的区别
         Python 2 将 strings 处理为原生的 bytes 类型，而不是 unicode(python2 str == bytes)，
         Python 3 所有的 strings 均是 unicode 类型(python3 中需要通过 unicode )
         string -> encode  -> bytes
         bytes -> decode  -> string
    
#### 2、文件处理
    a、r和rb的区别是什么？
        r 是只读方式打开文件,并会按encoding指定的编码格式断句，再转成Unicode
        rb 是以二进制只读方式打开文件, 直接读取的是文件的原生二进制
        
    b、解释一下以下三个参数的分别作用
        open(f_name,'r',encoding="utf-8")
        1> f_name: 要打开的文件
        2> r: 以只读的方式打开
        3> encoding: 将文件内容以utf-8格式进行编码
        

### 二、函数基础：
```python
### 1、写函数，计算传入数字参数的和。（动态传参）
def summation(x, y):
    """求传入参数的和"""
    print('%s+%s= %s' % (x, y, x+y))

summation(10, 23)
```
```python
### 2、写函数，用户传入修改的文件名，与要修改的内容，执行函数，完成整个文件的批量修改操作
def update_file(file, old_str, new_str):
    """修改文件指定内容"""
    try:
        with open(file, 'r+', encoding='utf-8') as f:
            data = f.read().replace(old_str, new_str)
            f.seek(0)
            f.truncate()
            f.write(data)
    except FileNotFoundError:
        print('文件不存在')

update_file('test.txt', '我心永恒', '以父之名')
```
```python
### 3、写函数，检查用户传入的对象（字符串、列表、元组）的每一个元素是否含有空内容。
def check_none(data):
    """检查某个对象(list,str,tuple)中是否有''空字符"""
    for s in data:
        if s == '' or s == ' ':
            print('{}中有空字符'.format(data))
            break

a = 'Pony is CEO'
b = ['a', '', 'b', 'd']
c = ('', 2, 4, ' ')
check_none(a)
check_none(b)
check_none(c)
```
```python
### 4、写函数，检查传入字典的每一个value的长度,如果大于2，那么仅保留前两个长度的内容，并将新内容返回给调用者。
def change_dict_value(d):
    """
    检查传入字典的每一个value的长度,如果大于2，
    那么仅保留前两个长度的内容，并将新内容返回给调用者
    """
    for k in d:
        value = str(d[k])
        if len(value) > 2:
            d[k] = value[:2]
    return d

org_dict = {'name': 'Pony', 'password': 'abc123', 'dept': 'IT', 'age': 48}
new_dict = change_dict_value(org_dict)
print(new_dict)
```
    ### 5、解释闭包的概念
    概念：闭包(closure)是函数式编程的重要的语法结构。函数式编程是一种编程范式 (而面向过程编程和面向对象编程也都是编程范式)。
    在面向过程编程中，我们见到过函数(function)；在面向对象编程中，我们见过对象(object)。
    函数和对象的根本目的是以某种逻辑方式组织代码，并提高代码的可重复使用性(reusability)。
    闭包也是一种组织代码的结构，它同样提高了代码的可重复使用性。
    ---
    说明：关于闭包，即函数定义和函数表达式位于另一个函数的函数体内(嵌套函数)。
    而且，这些内部函数可以访问它们所在的外部函数中声明的所有局部变量、参数。
    当其中一个这样的内部函数在包含它们的外部函数之外被调用时，就会形成闭包。
    也就是说，内部函数会在外部函数返回后被执行。而当这个内部函数执行时，它仍然必需访问其外部函数的局部变量、参数以及其他内部函数。
    这些局部变量、参数和函数声明（最初时）的值是外部函数返回时的值，但也会受到内部函数的影响。
    ---
    意义：返回的函数对象，不仅仅是一个函数对象，在该函数外还包裹了一层作用域，这使得，该函数无论在何处调用，优先使用自己外层包裹的作用域
    

### 三、函数进阶：

##### 1、写函数，返回一个扑克牌列表，里面有52项，每一项是一个元组,例如：[(Spade, A), (Heart, A), (Club, 2) ... (Diamond, K)]
```python
def make_poker():
    """
    生成一副扑克牌
    :return poker_list: [(Spade, A), (Heart, A), (Club, 2) ... (Diamond, K)]
    """
    poker_suit = ['Spade', 'Heart', 'Club', 'Diamond']
    poker_face = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    poker_list = []
    for suit in poker_suit:
        for face in poker_face:
            poker_list.append((suit, face))
    return poker_list

print(make_poker())
```

##### 2、写函数，传入n个数，返回字典{‘max’:最大值,’min’:最小值}
```python
# 例如:min_max(2,5,7,8,4)
# 返回:{'max':8,'min':2}
def max_min(*args):
    """找出传入参数中的最大值与最小值"""
    data = {}
    args_list = sorted(args)
    data['max'] = args_list[-1]
    data['min'] = args_list[0]
    return data

print(max_min(34,3,4,5,33,22,1))
```

##### 3、写函数,专门计算图形的面积其中嵌套函数,计算圆的面积,正方形的面积和长方形的面积
```python
# 调用函数area('圆形',圆半径) 返回圆的面积
# 调用函数area('正方形',边长) 返回正方形的面积
# 调用函数area('长方形',长,宽) 返回长方形的面积
def area_calc(graph_type, *args):
    """
    根据传入参数计算相关图形面积
    :param graph_type: 图形类型
    :param args: 图形参数
    :return: area : 面积
    """
    def roundness(radius):              # 圆形
        print(pow(radius, 2) * 3.14)    # πr²

    def square(len_side):               # 正方形
        print(pow(len_side, 2))         # a*a or a²

    def long_side(long, wide):          # 长方形
        print(long * wide)              # a*b

    if graph_type in ['roundness', 'square', 'long_side']:
        if len(args) == 1:
            locals()[graph_type](args[0])
        elif len(args) == 2:
            locals()[graph_type](args[0], args[1])
    else:
        print('不支持的图形类型：%s' % graph_type)

area_calc('roundness', 10)
area_calc('square', 12)
area_calc('long_side', 5, 6)
area_calc('long_side')
area_calc('abc', 12)

```

##### 4、写函数，传入一个参数n，返回n的阶乘
```python
# 例如:cal(7)
# 计算7*6*5*4*3*2*1
def cal(num):
    """
    计算传入参数的阶乘
    计算公式：n! = n*(n-1)!
    如：4! = 4 * 3!   展开： 4! = 4*3*2*1
    """
    if num == 1:
        return 1
    return num * cal(num-1)

print(cal(10))
```

#####　5、编写装饰器，为多个函数加上认证的功能（用户的账号密码来源于文件），要求登录成功一次，后续的函数都无需再输入用户名和密码
![认证功能装饰器](.\装饰器\decorate2.py)


### 四、生成器和迭代器
##### 1、生成器和迭代器的区别?
    对于list、string、tuple、dict等这些容器对象,使用for循环遍历是很方便的。
    在后台for语句对容器对象调用iter()函数。iter()是python内置函数。
    iter()函数会返回一个定义了 next()方法的迭代器对象，它在容器中逐个访问容器内的
    元素。next()也是python内置函数。在没有后续元素时，next()会抛出
    一个StopIteration异常，通知for语句循环结束。
    迭代器是用来帮助我们记录每次迭代访问到的位置，当我们对迭代器使用next()函数的
    时候，迭代器会向我们返回它所记录位置的下一个位置的数据。实际上，在使用next()函数
    的时候，调用的就是迭代器对象的_next_方法（Python3中是对象的_next_方法，
    Python2中是对象的next()方法）。所以，我们要想构造一个迭代器，
    就要实现它的_next_方法。但这还不够，python要求迭代器本身也是可迭代的，
    所以我们还要为迭代器实现_iter_方法，而_iter_方法要返回一个迭代器，
    迭代器自身正是一个迭代器，所以迭代器的_iter_方法返回自身self即可。
    
##### 2、生成器有几种方式获取value?
    for 循环
    next() 方法
    
##### 3、通过生成器写一个日志调用方法， 支持以下功能
```python
# 根据指令向屏幕输出日志
# 根据指令向文件输出日志
# 根据指令同时向文件&屏幕输出日志
# 以上日志格式如下
# 2017-10-19 22:07:38 [1] test log db backup 3
# 2017-10-19 22:07:40 [2] user alex login success 
# 注意：其中[1],[2]是指自日志方法第几次调用，每调用一次输出一条日志
import time

def logger(filename, channel='file'):
    """
    日志方法
    :param filename: log filename
    :param channel: 输出的目的地，屏幕(terminal)，文件(file)，屏幕+文件(both)
    :return:
    """
    n = 0
    while True:
        msg = yield
        n += 1     # 记录日志条数
        log_msg = "{} [{}] {}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), n, msg)
        if channel in ['file', 'both']:  # 写入文件
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write('{}\n'.format(log_msg))
            except FileNotFoundError:
                print('文件不存在')
        if channel in ['terminal', 'both']:  # 打印到terminal
            print(log_msg)


log_obj = logger(filename="web.log",channel='both')  # 初始化
log_obj.__next__()                                   # 唤醒生成器
log_obj.send('user alex login success')              # 发送消息
log_obj.send('user alex logout')                     # 发送消息
log_obj.send('user jack login success')              # 发送消息
```


### 五、内置函数
##### 1、用map来处理字符串列表,把列表中所有人都变成sb,比方alex_sb
```python
name=['alex','wupeiqi','yuanhao','nezha']
new_list = list(map(lambda n: '{}_sb'.format(n), name))
print(new_list)
```
##### 2、用filter函数处理数字列表，将列表中所有的偶数筛选出来
```python
"""
filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回一个迭代器对象，如果要转换为列表，可以使用 list() 来转换。
该接收两个参数，第一个为函数，第二个为序列，序列的每个元素作为参数传递给函数进行判，
然后返回 True 或 False，最后将返回 True 的元素放到新列表中。
"""
num = [1,3,5,6,7,8]

def is_even_number(n):
    return n % 2 == 0

new_num = list(filter(is_even_number, num))  # python2 中直接返回列表；python3 中返回迭代器对象
print(new_num)
```

##### 3、用filter函数处理以下字典

    
```python
# a.计算购买每支股票的总价
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
    {'name': 'FB', 'shares': 200, 'price': 21.09},
    {'name': 'HPQ', 'shares': 35, 'price': 31.75},
    {'name': 'YHOO', 'shares': 45, 'price': 16.35},
    {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
stock_price = map(lambda d:(d['name'],d['shares']*d['price']), portfolio)
print(list(stock_price))



# b.用filter过滤出，单价大于100的股票有哪些
price_gt_100 = filter(lambda d:d['price']>100, portfolio)
print(list(price_gt_100))
```
    
    
   
##### 4、请分别介绍文件操作中不同的打开方式之间的区别：
    模式	含义
    r	    文本只读模式
    rb	    二进制只读模式
    r+	    文本读写模式(如果先进行读操作可以读到原内容，如果先写，写的内容会覆盖原等长内容，并从覆盖后的内容尾端刚始读取)
    rb+	    二进制读写模式
    w	    文本只写模式
    wb	    二进制只写模式
    w+	    文本写读模式(先写后读，会清空原来的内容再写入，读也只能读到新写入的内容(并且要seek到开头才能读到)
    wb+	    二进制写读模式
    a	    文本追加模式,不能读
    ab	    二进制追加模式,不能读
    a+	    文本追加模式,可以读，seek位置为文件尾部
    ab+     二进制追加模式
    

##### 5、有如下列表,请将以字母“a”开头的元素的首字母改为大写字母；
```python
li = ['alex', 'egon', 'smith', 'pizza', 'alen']
for i in range(len(li)):
    if li[i][0] == 'a':
        li[i] = li[i].capitalize()
    else:
        continue
print(li)
```


##### 6、有如下程序, 请给出两次调用show_num函数的执行结果，并说明为什么：
```python
num = 20
def show_num(x=num):
   print(x)
show_num()
num = 30 
show_num()
# 两次返回都是 20
# 原因：  
# 如果函数收到的是一个不可变对象（比如数字、字符或者元组）的引用(x=num时,就是x=20，这就跟a=20,b=a,a=30,print(b)结果为20是一样的道理)
# 就不能直接修改原始对象，相当于通过“传值’来传递对象，
# 此时如果想改变这些变量的值，可以将这些变量申明为全局变量。
```  

##### 7、有如下列表,请以列表中每个元素的第二个字母倒序排序；
```python
li = ['alex', 'egon', 'smith', 'pizza', 'alen']
li = sorted(li, key=lambda l:l[1], reverse=True)
print(li)
```
##### 8、有名为poetry.txt的文件，其内容如下，请删除第三行； 
```python
""" 
昔人已乘黄鹤去，此地空余黄鹤楼。
黄鹤一去不复返，白云千载空悠悠。
晴川历历汉阳树，芳草萋萋鹦鹉洲。
日暮乡关何处是？烟波江上使人愁。
"""
import os
file = 'poetry.txt'
new_file = '{}.new'.format(file)
delete_line = 3

with open(file, 'r', encoding='utf8') as of, open(new_file, 'w', encoding='utf8') as nf:
    n = 1
    for line in of:
        if n != delete_line:
            nf.write(line)
        else:
            nf.write('')
        n += 1

os.replace(new_file, file)
``` 
      
       
##### 9、有名为username.txt的文件，其内容格式如下，写一个程序，判断该文件中是否存在"alex", 如果没有，则将字符串"alex"添加到该文件末尾，否则提示用户该用户已存在；
```python
"""  
pizza
alex
egon
"""
account_file = 'username.txt'
check_name = 'alex'

with open(account_file, 'r+', encoding='utf8') as f:
    for name in f:
       if name.strip() == check_name:
           print('{} is already exist'.format(check_name))
           break
    else:
        f.write('\n{}'.format(check_name))
```    
     
##### 10、有名为user_info.txt的文件，其内容格式如下，写一个程序，删除id为100003的行；
```python
"""
pizza,100001
alex, 100002
egon, 100003
"""
import os

account_file = 'user_info.txt'
delete_id = '100003'
temp_file = '{}.new'.format(account_file)

with open(account_file, 'r+', encoding='utf8') as of, open(temp_file, 'w', encoding='utf8') as nf:
    for line in of:
        if line.split(',')[1].strip() == delete_id:
            nf.write('')
        else:
            nf.write(line)
os.replace(temp_file, account_file)
```   

##### 11、有名为user_info.txt的文件，其内容格式如下，写一个程序，将id为100002的用户名修改为alex li；
```python
"""
pizza,100001
alex, 100002
egon, 100003
"""
import os

account_file = 'user_info.txt'
change_id = '100002'
change_name = 'Alex Li'
temp_file = '{}.new'.format(account_file)

with open(account_file, 'r+', encoding='utf8') as of, open(temp_file, 'w', encoding='utf8') as nf:
    for line in of:
        if line.split(',')[1].strip() == change_id:
            line = '{},{}'.format(change_name, change_id)
        nf.write(line)
      
os.replace(temp_file, account_file)
```

##### 12、写一个计算每个程序执行时间的装饰器；
```python
import time

def run_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args)
        end_time = time.time()
        print('Run time: {}'.format(end_time - start_time))
    return wrapper

@run_time
def foo(user):
    time.sleep(0.5)
    print('Hi: [{}],this is foo'.format(user))

foo('Jack Ma')
```

##### 13、lambda是什么？请说说你曾在什么场景下使用lambda？
    lambda函数就是可以接受任意多个参数(包括可选参数)并且返回单个表达式值得函数
    好处：
        1.lambda函数比较轻便，即用即扔，适合完成只在一处使用的简单功能
        2.匿名函数，一般用来给filter，map这样的函数式编程服务
        3.作为回调函数，传递给某些应用，比如消息处理
        
        
##### 14、题目：写一个摇骰子游戏，要求用户压大小，赔率一赔一。
```python
# 要求：三个骰子，摇大小，每次打印摇骰子数

import random

def make_dice(num, dice_count=None):
    """
    生成色子点数
    :param dice_count: 色子点数列表
    :param num: 色子个数
    :return: dice_count
    """
    for i in range(0, num):
        dice_count.append(random.randint(1, 6))
    return dice_count

def start_game():
    global exit_flag
    init_money = 1000
    while not exit_flag:
        dice_count = []
        user_point = input("Big[B] or Small[S]; Quit[q]>>>: ")
        bet_amount = int(input("Bet amount>>>: "))
        if init_money >= 0:
            if bet_amount > init_money:
                exit('你输完了')
            dice_point_list = make_dice(dice_num, dice_count)
            dice_point_sum = sum(dice_point_list)
            if user_point in ['q', 'Q']:
                exit_flag = True
            if user_point in ['s', 'S'] and dice_point_sum <= 10:
                print('YOU WINNING\nDice Point Total Is Big: [{}]: {}\n'.format(dice_point_sum, dice_point_list))
                init_money += bet_amount
                print('你的余额: [{}]'.format(init_money))
            elif user_point in ['b', 'B'] and dice_point_sum > 10:
                print('YOU WINNING\nDice Point Total Is Small: [{}]: {}\n'.format(dice_point_sum, dice_point_list))
                init_money += bet_amount
                print('你的余额: [{}]'.format(init_money))
            else:
                print('YOU LOSE\nDice Point Total Is Small: [{}]: {}\n'.format(dice_point_sum, dice_point_list))
                init_money -= bet_amount
                print('你的余额: [{}]'.format(init_money))
        else:
            print('你没钱了')
            exit_flag = True

if __name__ == "__main__":
    dice_num = 3
    exit_flag = False
    start_game()
```
    