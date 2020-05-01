#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/17
# Location: DongGuang
# Desc:     正则匹配模块 re


"""
常用表达式规则
'.'     默认匹配除\n之外的任意一个字符，若指定flag DOTALL,则匹配任意字符，包括换行
'^'     匹配字符开头，若指定flags MULTILINE,这种也可以匹配上(r"^a","\nabc\neee",flags=re.MULTILINE)
'$'     匹配字符结尾， 若指定flags MULTILINE ,re.search('foo.$','foo1\nfoo2\n',re.MULTILINE).group() 会匹配到foo1
'*'     匹配*号前的字符0次或多次， re.search('a*','aaaabac')  结果'aaaa'
'+'     匹配前一个字符1次或多次，re.findall("ab+","ab+cd+abb+bba") 结果['ab', 'abb']
'?'     匹配前一个字符1次或0次 ,re.search('b?','alex').group() 匹配b 0次
'{m}'   匹配前一个字符m次 ,re.search('b{3}','alexbbbs').group()  匹配到'bbb'
'{n,m}' 匹配前一个字符n到m次，re.findall("ab{1,3}","abb abc abbcbbb") 结果'abb', 'ab', 'abb']
'|'     匹配|左或|右的字符，re.search("abc|ABC","ABCBabcCD").group() 结果'ABC'
'(...)' 分组匹配， re.search("(abc){2}a(123|45)", "abcabca456c").group() 结果为'abcabca45'


'\A'    只从字符开头匹配，re.search("\Aabc","alexabc") 是匹配不到的，相当于re.match('abc',"alexabc") 或^
'\Z'    匹配字符结尾，同$
'\d'    匹配数字0-9
'\D'    匹配非数字
'\w'    匹配[A-Za-z0-9]
'\W'    匹配非[A-Za-z0-9]
's'     匹配空白字符、\t、\n、\r , re.search("\s+","ab\tc1\n3").group() 结果 '\t'

'(?P<name>...)' 分组匹配 re.search("(?P<province>[0-9]{4})(?P<city>[0-9]{2})(?P<birthday>[0-9]{4})","371481199306143242").groupdict("city") 结果{'province': '3714', 'city': '81', 'birthday': '1993'}
"""


import re

# 找出文件中所有电话号码
with open('account.txt', 'r', encoding='utf8') as f:
    data = f.read()
    print(re.findall('1[0-9]{10}', data))



"""
.group() 为匹配到的内容
.groups() 为匹配到的分组内容(元祖形式)
"""

# 从头开始匹配
print(re.match('he', 'hello world').group())  # 与 ^ 功能相同
# 'he'

# 根据模型去字符串中匹配指定内容，匹配单个
print(re.search('wor', 'hello world').group())
# 'wor'

# 把所有匹配到的字符放到以列表中的元素返回
# match and search均用于匹配单值，即：只能匹配字符串中的一个，
# 如果想要匹配到字符串中所有符合条件的元素，则需要使用 findall
print(re.findall('llo', 'hello world! hello china'))
# ['llo', 'llo']

# 以匹配到的字符当做列表分隔符
print(re.split('l', 'hello world'))
# ['he', '', 'o wor', 'd']

# 匹配字符并替换
print(re.sub('h', 'H', 'hello world'))
# 'Hello world'

# 全部匹配
# 整个字符串匹配成功就返回re object, 否则返回None
print(re.fullmatch('\w+@\w+\.(com|cn|edu)',"jack@alibaba.com").group())
# 'jack@alibaba.com'