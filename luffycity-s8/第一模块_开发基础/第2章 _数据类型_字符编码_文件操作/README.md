# 第一模块 开发基础
## 第二章 数据类型_字符编码_文件操作
    
### 练习
___
#### 1、代码实现：利用下划线将列表的每一个元素拼接成字符串，li＝['alex', 'eric', 'rain']
```python
li = ['alex', 'eric', 'rain']
'_'.join(li)
```

#### 2、查找列表中元素，移除每个元素的空格，并查找以a或A开头并且以c结尾的所有元素。
```python
li = ["alec ", " aric", "Alex", "Tony", "rain"]
s_li = []
for i in li:
    li[i] = i.strip()
    if i.startswith('a') or i.startswith('A') and i.endswith('c'):
        s_li.append(i)
print("各元素去除空格:", li)
print("以a或A开头并且以c结尾的所有元素:", s_li)
```

#### 3、写代码，有如下列表li，按照要求实现每一个功能
```python
li = ['alex', 'eric', 'rain']

##### 计算列表长度并输出
print(len(li))

##### 列表中追加元素“seven”，并输出添加后的列表
li.append('seven')
print(li)

##### 请在列表的第1个位置插入元素“Tony”，并输出添加后的列表
li.insert(0, 'Tony')
print(li)

##### 请修改列表第2个位置的元素为“Kelly”，并输出修改后的列表
li[1] = 'Kelly'
print(li)

##### 请删除列表中的元素“eric”，并输出修改后的列表
li.remove('eric')
print(li)

##### 请删除列表中的第2个元素，并输出删除的元素的值和删除元素后的列表
print("将要删除的元素：", li[1])
del li[1]
print(li)

##### 请删除列表中的第3个元素，并输出删除元素后的列表
del li[3]
print(li)

##### 请删除列表中的第2至4个元素，并输出删除元素后的列表
del li[1:4]
print(li)

##### 请将列表所有的元素反转，并输出反转后的列表
li.reverse()
print(li)

##### 请使用for、len、range输出列表的索引
for index in range(len(li)):
    print(index)
    
##### 请使用enumrate输出列表元素和序号（序号从100开始）
for index,v in enumerate(li):
    print(index+100, v)
    
##### 请使用for循环输出列表的所有元素
for i in li:
    print(i)
```


#### 4、写代码，有如下列表，请按照功能要求实现每一个功能
```python
li = ["hello", 'seven', ["mon", ["h", "kelly"], 'all'], 123, 446]

##### 请根据索引输出“Kelly”
print(li[2][1][1])

##### 请使用索引找到'all'元素并将其修改为“ALL”，如：li[0][1][9]...
li[2][2] = "ALL"
```
#### 5、写代码，有如下元组，请按照功能要求实现每一个功能
```python
tu = ('alex', 'eric', 'rain')

##### 计算元组长度并输出
print(len(tu))

##### 获取元组的第2个元素，并输出
print(tu[1])

##### 获取元组的第1-2个元素，并输出
print(tu[0:2])

##### 请使用for输出元组的元素
for i in tu:
    print(i)
    
##### 请使用for、len、range输出元组的索引
for i in range(len(tu)):
    print(i)

##### 请使用enumrate输出元祖元素和序号（序号从10开始）
for index,v in enumerate(tu):
    print(index+10, v)

```


#### 6、有如下变量，请实现要求的功能
```python
tu = ("alex", [11, 22, {"k1": 'v1', "k2": ["age", "name"], "k3": (11,22,33)}, 44])

##### 讲述元祖的特性
#   1.可存放多个值
#   2.不可变
#   3.按照从左到右的顺序定义元组元素，下标从0开始顺序访问，有序

##### 请问tu变量中的第一个元素“alex”是否可被修改？
#   不可以，元祖是不可变数据类型

##### 请问tu变量中的"k2"对应的值是什么类型？是否可以被修改？如果可以，请在其中添加一个元素“Seven”
type(tu[1][2].get('k2'))
#   通过type方法可以知道，k2对应的值是一个列表，列表类型是可变的，所以可以修改
tu[1][2].get('k2').append('Seven')

##### 请问tu变量中的"k3"对应的值是什么类型？是否可以被修改？如果可以，请在其中添加一个元素“Seven”
type(tu[1][2].get('k3'))
#   通过type方法可以知道，k3对应的值是一个元祖，元祖类型是不可变的，所以不可以修改
```


#### 7、字典
```python
dic = {'k1': "v1", "k2": "v2", "k3": [11,22,33]}

##### 请循环输出所有的key
for k in dic:
    print(k)
    
##### 请循环输出所有的value
for k in dic:
    print(dic.get(k))
    
##### 请循环输出所有的key和value
for k in dic:
    print(k, dic.get(k))
    
##### 请在字典中添加一个键值对，"k4": "v4"，输出添加后的字典
dic['k4'] = "v4"
print(dic)

##### 请在修改字典中“k1”对应的值为“alex”，输出修改后的字典
dic['k1'] = 'alex'
print(dic)

##### 请在k3对应的值中追加一个元素44，输出修改后的字典
dic['k3'].append(44)
print(dic)

##### 请在k3对应的值的第1个位置插入个元素18，输出修改后的字典
dic['k3'].insert(0, 18)
print(dic)
```


#### 8、各数据类型之间的转换
```python
s = 'alex'
li = ['alex', 'seven']
tu = ('Alex', 'seven')

##### 将字符串s = "alex"转换成列表
s_list = list(s)

##### 将字符串s = "alex"转换成元祖
s_tuple = tuple(s)

##### 将列表li = ["alex", "seven"]转换成元组
li_tuple = tuple(li)

##### 将元祖tu = ('Alex', "seven")转换成列表
tu_list = list(tu)

##### 将列表li = ["alex", "seven"] 转换成字典且字典的key按照10开始向后递增
li_2 = [i for i in range(10, len(li)+10)]
dict(zip(li_2, li))
```

#### 9、元素分类
```python
##### 有如下值集合，将所有大于66的值保存至字典的第一个key中，将小于66的值保存至第二个key的值中。
##### 即：{'k1':大于66的所有值, 'k2':小于66的所有值}
li = [11, 22, 33, 44, 55, 66, 77, 88, 99, 90]
dic = {'k1': [], 'k2': []}
for i in li:
    if i > 66:
        dic['k1'].append(i)
    elif i < 66:
        dic['k2'].append(i)
print(dic)
```


#### 10、输出商品列表，用户输入序号，显示用户选中的商品
```python
# 商品如下：li 允许用户添加商品 用户输入序号显示内容
li = ["手机", "电脑", '鼠标垫', '游艇']
choice_list = []
exit_flag = False
while not exit_flag:
    print('商品列表'.center(30, '='))
    for i, v in enumerate(li):
        print("%s.\t%s" % (i, v))
    choice = input("请输入商品编号选择商品[退出请按q] ：")
    if choice.isdigit():
        choice = int(choice)
    if choice == 'q':
        print('已添加的商品有：%s' % choice_list)
        exit_flag = True
    elif choice >= len(li):
        print('编号不存在，请重新输入:')
        continue
    else:
        choice_list.append(li[choice])
        print('[%s]已添加' % li[choice])
```


#### 11、列举布尔值是False的所有值
    布尔值是False的有： [] () {} 0 False "" 等
    
    
#### 12、有两个列表如下，做相应集合操作
```python
l1 = [11,22,33]
l2 = [22,33,44]
# 先把两个列表转换成set集合
set1 = set(l1)
set2 = set(l2)

##### 获取内容相同的元素列表(交集)
set1.intersection(set2)
# or
set1 & set2

##### 获取li或l2中出现过的所有元素(合集/并集）
set1.union(set2)
# or
set1 | set2

##### 获取l1中有，l2中没有的元素列表(差集)
set1.difference(set2)
# or
set1 - set2

##### 获取l2中有，l3中没有的元素列表(差集)
set2.difference(set1)
# or
set2 - set1

##### 获取l1和l2中内容都不同的元素(对称差集)
set1.symmetric_difference(set2)
# or
set1 ^ set2
```

#### 13、利用For循环和range输出
```python
##### For循环从大到小输出 100 - 1
for i in range(0, 100):
    print(100 - i)
    
##### For循环从小到到输出 1 - 100
for i in range(1, 101):
    print(i)

##### While循环从大到小输出 100 - 1
count = 0
while count < 100:
    print(100 - count)
    count += 1
    
##### While循环从小到到输出 1 - 100
count = 1
while count <= 100:
    print(count)
    count += 1

```


#### 14、在不改变列表数据结构的情况下找最大值 li = [1,3,2,7,6,23,41,243,33,85,56]
```python
li = [1, 3, 2, 7,6, 23, 41, 243, 33, 85, 56]
max_n = li[0]
for i in li:
    if i > max_n:
        max_n = i
print(max_n)
```


#### 15、在不改变列表中数据排列结构的前提下，找出以下列表中最接近最大值和最小值的平均值的数
```python
li = [-100, 1, 3, 2, 7, 6, 120, 121, 140, 23, 411, 99, 243, 33, 85, 56]
max_n = min_n = li[0]
for i in li:
    if i > max_n:
        max_n = i
    elif i < min_n:
        min_n = i
avg_n = (max_n + min_n) / 2
print('最大值是：%s, 最小值是：%s, 最大与最小值的平均值是: %s' % (max_n, min_n, avg_n))

avg_like = li[0]
for i in li:
    if abs(avg_n - i) < abs(avg_n - avg_like):
        avg_like = i
print("最接近平均值的元素是：%s" % avg_like)
```


#### 16、利用for循环和range输出9 * 9乘法表
```python
for x in range(1, 10):
    for y in range(1, x + 1):
        print("%d*%d=%2s" % (y, x, (y * x)), end=' ')
    print('\n')
# or
print('\n'.join([' '.join(["%d*%d=%2s" % (y, x, x * y) for y in range(1, x + 1)]) for x in range(1, 10)]))
```


#### 17、求100以内的素数和。（编程题）
```python
# 素数又称为质数，它指的是只能被1和它本身整除的整数。其中，1不是素数，任何时候都不用考虑1。
max_num = 100
prime_num = []
for i in range(2, max_num + 1):  # 0,1 除外，循环从2开始
    prime_flag = True            # 设置是质数的标志位为True
    for n in range(2, i):        # 子循环计算i 是否可以被比它小的数据整除
        if not i % n:            # 只要有一个能整除，就说明i 不是质数，设置prime_flag为False
            prime_flag = False
            break                # 退出当前循环
    if prime_flag:
        prime_num.append(i)
print("%s内是的质数有：%s" % (max_num, prime_num))
print("%s内所有质数的和是：%s" % (max_num, sum(prime_num)))

```