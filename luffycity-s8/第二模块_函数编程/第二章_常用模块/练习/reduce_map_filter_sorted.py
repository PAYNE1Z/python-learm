#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/30
# Location: DongGuang
# Desc:     高阶函数：四大金刚 [reduce, map, filter, sorted]


from functools import reduce
# map, filter, sorted 已内置有py编译器

"""
1. map()函数接收两个参数，
    一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回
    map(func, Iterable)
    sample: list(map(lambda x:x*2, [1,2,3,4,5])  # 列表元素自乘 
            map将列表中的每个素传给lambda函数处理并反加结果给map, 最后list将map里的值转成列表：[1,4,9,16,25]

2. reduce()把一个函数作用在一个序列[x1, x2, x3, ...]上，
    这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
    reduce(func, Iterable)
    sample: ret = reduce(lambda x,y:x*y, range(1,6))  # 计算5的阶乘
            reduce将列表中的前两个值传给lambda处理将返回结果覆盖列表前两个值：del l[0:2]; l.insert(0,返回结果) ..

3. filter()也接收一个函数和一个序列。
    和map()不同的是，filter()把传入的函数依次作用于每个元素，
    然后根据返回值是True还是False决定保留还是丢弃该元素
    filter(func, Iterable)
    sample: list(filter(lambda x:x%2, range(101))  # 取0-100中的所有奇数
    sample: list(filter(lambda x:not x%2, range(101))  # 取0-100中的所有偶数数
    sample: list(filter(lambda x:x, ['A', 'b', '', None, '12', 1, ' ']))  # 过滤列表中的所有空字符
            filter将列表中的每个元素传给lambda函数得到返回值True或False
            如果是True就把元素留下，如果是False则丢弃
            
4. sorted()函数也是一个高阶函数，它还可以接收一个key函数来实现自定义的排序
    sorted(Iterable, key=func)
    sample: sorted([36, 5, -12, 9, -21], key=abs)  # 将列表元素按绝对值排序
            sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower) # 忽略大小定排序
            sorted会将可迭代对象中的元素交给key函数处理，并按照对应关系返回list相应的元素进行排序
            keys排序结果 => [5, 9,  12,  21, 36]
                            |  |    |    |   |
            最终结果     => [5, 9, -12, -21, 36]
            指定sorted参数reverse=True, 将会进行反向排序
"""


# 使用 map 与 reduce 实现把一个字符串类型的数字，如：'123.456' 转换在数字类型: 123.456
def str2num(s):
    num_map = dict(list(zip(map(str, range(10)), range(10))))  # 生成 {'1':1, '2':2, '3':3,...} 格式的字典

    def char2num(n):   # 将接收的数字字符串n根据num_map对应表，将n换成int类型的n, 并返回
        return num_map[n]

    if '.' in s:  # 判断是否有小数点
        s1,s2 = s.split('.')    # s1 = '123'; s2 = '456'   # 有小数点的以小数点切片分开处理 123整数部分 与 456小数部分
        s1_list, s2_list = map(char2num, s1), map(char2num, s2)
        # map函数 把s1 '123'中的字符串一个一个的传给char2num函数并接收返回值 生成列表: [1,2,3]
        # 分解： map '1' -> char2num -> 1 -> s1_list.append[1] -> [1]
        #       map '2' -> char2num -> 2 -> s1_list.append[2] -> [1,2]
        #       map '3' -> char2num -> 3 -> s1_list.append[3] -> [1,2,3]  s1迭代结束. done

        return reduce(lambda x, y: x*10+y, s1_list) + reduce(lambda x, y: x*10+y, s2_list) / pow(10, len(s2))
        # reduce函数 把s1_list[1,2,3]中的前两个值传给 lambda函数进行计算
        # 分解：reduce 1,2 -> lambda x*10+y -> [12,3] -> reduce 12,3 -> lambda x*10+y -> [123] -> 列表只有一个元素. done
        # 1 reduce 把 s1_list 中的前面两个值：1,2
        #   传给lambda, 根据规则x*10+y 计算结果：1*10 + 2 = 12 并把结果12 替换s1_list的前面两个值： [12,3]
        # 2 reduce 把新 s1_list 中的前面两个值：12,3
        #   传给lambda, 根据规则x*10+y 计算结果，并与上次的结果相加：12*10 + 3 = 123 并把结果123替换s1_list的前面两个值：[123]
        # 3 直到s1_list中变成一个值后返回该值 123
        #
        # 后面的小数456是一样的流程，只不过需要将reduce得到的结果除以 10的位数的次方 转换成小数  eg. 456 / 10**3 -> 0.456
    else:
        s_list = map(char2num, s)
        return reduce(lambda x, y: x*10+y, s_list)
        # 上面两条可以写成一条：
        # return reduce(lambda x, y: x*10+y, map(char2num, s))

num = '123.456'
print('{}是否带小数:'.format(num), isinstance(str2num(num),float))
print('str2num执行结果: {}, 类型: {}'.format(str2num(num), type(str2num(num))))




# 用filter求素数
"""
计算素数的一个方法是埃氏筛法，它的算法理解起来非常简单：

首先，列出从2开始的所有自然数，构造一个序列：
2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, ...

取序列的第一个数2，它一定是素数，然后用2把序列的2的倍数筛掉：
3, 4x, 5, 6x, 7, 8x, 9, 10x, 11, 12x, 13, 14x, 15, 16x, 17, 18x, 19, 20x, ...

取新序列的第一个数3，它一定是素数，然后用3把序列的3的倍数筛掉：
5, 6x, 7, 8, 9x, 10, 11, 12x, 13, 14, 15x, 16, 17, 18x, 19, 20, ...

取新序列的第一个数5，然后用5把序列的5的倍数筛掉：
7, 8, 9, 10x, 11, 12, 13, 14, 15x, 16, 17, 18, 19, 20x, ...

不断筛下去，就可以得到所有的素数。
"""

# 用Python来实现这个算法，可以先构造一个从3开始的奇数序列：
def _odd_iter():
    p = 1
    while True:
        p = p + 2
        yield p
        # 注意这是一个生成器，并且是一个无限序列。

# 然后定义一个筛选函数：
def _not_divisible(y):
    return lambda x: x % y > 0

# 最后，定义一个生成器，不断返回下一个素数：
def primes():
    yield 2
    it = _odd_iter()  # 初始序列
    while True:
        n = next(it)  # 返回序列的第一个数
        yield n
        # 构造新序列
        # 此时的 it是Iterable,
        # 将里面的元素传给_not_divisible中的lambda函数判断是否能整除迭代对象中的前一个元素
        # 如果不能整除则保留元素，并将新的元素加到it中
        it = filter(_not_divisible(n), it)

# 这个生成器先返回第一个素数2，然后，利用filter()不断产生筛选后的新的序列。

# 由于primes()也是一个无限序列，所以调用时需要设置一个退出循环的条件：
# 打印10以内的素数:
p_list = []
for n in primes():
    if n < 10:
        p_list.append(n)
    else:
        break

print('10以内的所有素数:', p_list)
# 注意到Iterator是惰性计算的序列，所以我们可以用Python表示“全体自然数”，“全体素数”这样的序列，而代码非常简洁。




# 用 sorted 函数对数据进行排序
# 假设我们用一组tuple表示学生名字和成绩：
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

# 按名字排序
def by_name(t):
    return t[0].lower()

# 按分数高到低排序
def by_score(t):
    return t[1]
    # return -t[1]
    # 把正数变成负数，那么最大的就变成了最小的，以次类推; 就相当于是倒序了.sorted就不用再指定reverse参数了

# 注意 key参数传递的是函数对象，所有不要加()
print('按名字排序:', sorted(L, key=by_name))
print('按名字排序:', sorted(L, key=lambda x:x[0].lower()))
print('按分数高到低排序:', sorted(L, key=by_score, reverse=True))
print('按分数高到低排序:', sorted(L, key=lambda x:x[1], reverse=True))

print(sorted(L, key=lambda x: (x[1],str.lower(x[0]))))




##### 1-100求和
ret = reduce(lambda x,y:x+y, range(1,101))
print('1-100的和: ', ret)

##### 1-100奇数求和
ret = reduce(lambda x,y:x+y, filter(lambda x:x%2, range(1,101)))
print('1-100奇数的和: ', ret)

##### 1-100偶数求和
ret = reduce(lambda x,y:x+y, filter(lambda x:not x%2, range(1,101)))
print('1-100偶数的和: ', ret)