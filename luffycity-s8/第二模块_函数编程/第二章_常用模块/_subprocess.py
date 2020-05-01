#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/17
# Location: DongGuang
# Desc:     执行系统命令模块 subprocess


"""
我们经常需要通过Python去执行一条系统命令或脚本，
系统的shell命令是独立于你的python进程之外的，
每执行一条命令，就是发起一个新进程，
通过python调用系统命令或脚本的模块在python2有os.system，

三种执行命令的方法
    1、subprocess.run(*popenargs, input=None, timeout=None, check=False, **kwargs) #官方推荐
    2、subprocess.call(*popenargs, timeout=None, **kwargs) #跟上面实现的内容差不多，另一种写法
    3、subprocess.Popen() #上面各种方法的底层封装
"""


import subprocess



"""run()方法"""
# 命令与命令参数以列表形式传给subprosecc
# stderr : 从系统拿到调用命令时的标准错误信息
# stdout : 从系统拿到调用命令时的标准输出信息
# check : 为True是如果命令报错subprocess也会报错并退出
import subprocess
s = subprocess.run(['df','-h'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
print(s)
print(s.stdout)  # 标准输出
print(s.stderr)  # 标准错误
print(s.returncode)  # 命令执行返回码(0为成功)

# 直接将命令传给shell处理(带管道的命令行只能传给shell处理，不然无法解析)
# shell:  为True表示把命令行字符串直接交给shell处理
s1 = subprocess.run('df -h | grep sys',shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(s1)
print(s1.stdout)

# 直接将命令传给shell处理
s2 = subprocess.run('uname -a',shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(s2)
print(s2.stdout)



"""call()方法"""
# 执行命令，返回命令执行状态 ， 0 or 非0
retcode = subprocess.call(["ls", "-l"])

# 执行命令，如果命令结果为0，就正常返回，否则抛异常
subprocess.check_call(["ls", "-l"])

# 接收字符串格式命令，返回元组形式，第1个元素是执行状态，第2个是命令结果
subprocess.getstatusoutput('ls /bin/ls')
# (0, '/bin/ls')

# 接收字符串格式命令，并返回结果
subprocess.getoutput('ls /bin/ls')
# '/bin/ls'

# 执行命令，并返回结果，注意是返回结果，不是打印，下例结果返回给res
res = subprocess.check_output(['ls','-l'])
print(res)
# b'total 0\ndrwxr-xr-x 12 alex staff 408 Nov 2 11:05 OldBoyCRM\n'




"""Popen()方法"""
# 常用参数：
# args：shell命令，可以是字符串或者序列类型（如：list，元组）
# stdin, stdout, stderr：分别表示程序的标准输入、输出、错误句柄
# preexec_fn：只在Unix平台下有效，用于指定一个可执行对象（callable object），它将在子进程运行之前被调用
# shell：同上
# cwd：用于设置子进程的当前目录
# env：用于指定子进程的环境变量。如果env = None，子进程的环境变量将从父进程中继承。

# 下面这2条语句执行会有什么区别？
a = subprocess.run('sleep 10',shell=True,stdout=subprocess.PIPE)
a = subprocess.Popen('sleep 10',shell=True,stdout=subprocess.PIPE)
# 区别是Popen会在发起命令后立刻返回，而不等命令执行结果。
# 这样的好处是什么呢
# 如果你调用的命令或脚本 需要执行10分钟，你的主程序不需卡在这里等10分钟，可以继续往下走，干别的事情，每过一会，通过一个什么方法来检测一下命令是否执行完成就好了。
# Popen调用后会返回一个对象，可以通过这个对象拿到命令执行结果或状态等，该对象有以下方法
a.stdout.read()  # 读取进程标准输出
a.stderr.read()  # 读取进程标准错误
a.poll()  # 检查运行命令进程的返回值(运行结束会返回相应状态码，没结束为空)
a.wait()  # 等待命令运行进程结束
a.terminate()  # 终止所启动的进程Terminate the process with SIGTERM
a.kill()  # 杀死所启动的进程 Kill the process with SIGKILL
a.communicate()  # 与启动的进程交互(需要用户输入)，发送数据到stdin,并从stdout接收输出，然后等待任务结束
a = subprocess.Popen('python3 guess_age.py',stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE,shell=True)
a.communicate(b'22')  # 只能发送bytes类型数据
# (b'your guess:try bigger\n', b'')
import signal
a.send_signal(signal.SIGKILL)  # 发送系统信号
a.pid()  # 拿到所启动进程的进程号
