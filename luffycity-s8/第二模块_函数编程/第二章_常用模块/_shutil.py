#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
#
# Author:   Payne Zheng <zzuai520@live.com>
# Date:     2019/5/15
# Location: DongGuang
# Desc:     shutil/zipfile/tarfile 模块 文件打包与压缩


import shutil
import zipfile
import tarfile


# 1、将文件内容拷贝到另一个文件中（目标文件要存在)
f1 = open('test.txt', 'r', encoding='utf8')
f2 = open('test_new.txt', 'w', encoding='utf8')
shutil.copyfileobj(fsrc=f1, fdst=f2, length=1024)
# fsrc: 源文件
# fdst: 目标文件
# length: 以多少大小的块进行copy（每次1024字节，直到拷贝完)



# 2、拷贝文件(目标文件无需存在, 并且无需打开文件)
shutil.copyfile(src='test.txt', dst='test_new_1.txt')



# 3、仅拷贝文件的权限(内容、组、用户均不变) 目标文件必需存在
shutil.copymode(src='test.txt', dst='test_new.txt')



# 4、仅拷贝文件的stat信息(mode,atime,ctime,mtime...) 目标文件必需存在
shutil.copystat(src='test.txt', dst='test_new.txt')



# 5、拷贝文内容和权限
shutil.copy(src='test.txt', dst='test_new_2.txt')



# 6、拷贝文件内容与stat信息
shutil.copy2(src='test.txt', dst='test_new_3.txt')



# 7、拷贝文件夹(递归)
shutil.copytree(src='D:\Payne\python-workdir\luffycity-s8',
                dst='D:\Payne\python-workdir\luffycity-s10',
                symlinks=False,
                ignore=shutil.ignore_patterns('test.txt', '_*.py')
                )
# src: 要拷贝的源文件夹
# dst: 拷贝后的目标文件夹名(带路径会拷贝到相应路径下，不带路径拷贝到当前目录下
# symlinks: 是否拷贝软链接文件
# ignore: 要忽略不拷贝的文件(支持正则匹配)



# 8、删除文件夹(递归)
shutil.rmtree(path='D:\Payne\python-workdir\luffycity-s9', ignore_errors=False, onerror=None)
# path: 要删除文件晓夹
# ignore_errors: 是否忽略错误消息 True为忽略



# 9、移动文件夹(递归)
shutil.move(src='D:\Payne\python-workdir\luffycity-s10', dst='luffycity-s8')
# src: 源文件夹
# dst: 目标文件名(未带路径则移动到当前目录；只指定路径没指定文件夹名，则为原文件夹名



# 10、文件打包(创建压缩包并返回文件路径)
ret = shutil.make_archive(base_name='D:\Payne\python-workdir\luffycity', format='gztar', root_dir='luffycity-s8')
print(ret)  # D:\Payne\python-workdir\luffycity.tar.gz
# base_name： 压缩包的文件名，也可以是压缩包的路径。只是文件名时，则保存至当前目录，否则保存至指定路径，
# 如： data_bak     => 保存至当前路径
# 如：/tmp/data_bak => 保存至/tmp/
#
# format： 压缩包种类，“zip”, “tar”, “bztar”，“gztar”
# root_dir： 要压缩的文件夹路径（默认当前目录）
# owner： 用户，默认当前用户
# group： 组，默认当前组
# logger： 用于记录日志，通常是logging.Logger对象



# 11、shutil 对压缩包的处理是调用 ZipFile 和 TarFile 两个模块来进行的
# zipfile 压缩与解压

# zipfile.ZipFile(file[, mode[, compression[, allowZip64]]])
# 1.参数file表示文件的路径或类文件对象(file-like object);
# 2.参数mode指示打开zip文件的模式，默认值为'r'，表示读已经存在的zip文件，
#   也可以为'w'或'a'，w'表示新建一个zip文档或覆盖一个已经存在的zip文档，'a'表示将数据附加到一个现存的zip文档中;
# 3.参数compression表示在写zip文档时使用的压缩方法，它的值可以是zipfile. ZIP_STORED 或zipfile. ZIP_DEFLATED。
#   如果要操作的zip文件大小超过2G，应该将allowZip64设置为True。

# 压缩
z = zipfile.ZipFile('zipfile.zip', 'w')  # w: 压缩； r: 解压缩； a: 追加压缩
z.write('luffycity-s8\README.md', 'README.md')  # 加第二个参数(文件名)，则压缩包中不会带文件路径，反之会带路径
z.write(r'D:\Payne\python-workdir\test\t.py', 't.py')
z.close()

# 读取压缩文件
file_dir = 'zipfile.zip'
zipFile = zipfile.ZipFile(file_dir)
# 获取zip文档内所有文件的信息，返回一个zipfile.ZipInfo的列表
print(zipFile.infolist())
# 获取zip文档内所有文件的名称列表
print(zipFile.namelist())
# 将zip文档内的信息打印到控制台上
print(zipFile.printdir())

# 解压
# ZipFile.extract(member[, path[, pwd]])  将zip文档内的指定文件解压到当前目录
# ZipFile.extractall([path[, members[, pwd]]])  将zip文档内所有文件解压到当前目录
# member: 指定要解压的文件名称或对应的ZipInfo对象；
# path: 指定了解析文件保存的文件夹；
# pwd: 为解压密码。下面一个例子将保存在程序根目录下的text.zip内的所有文件解压到D:/Work目录：
z = zipfile.ZipFile('zipfile.zip')
z.extract(member='t.py')  # 解压压缩包中的t.py 文件到当前目录
z.extractall(path=r'D:\Payne\python-workdir\nginx_502')  # 解压压缩包中的所有文件到 D:\Payne\python-workdir\nginx_502 目录
z.close()



# 12、tarfile 打包与解包
# 打包及重命名文件
# 以w模式创建文件
tar = tarfile.open('tar_file.tar', 'w')
# 添加一个文件，arcname可以重命名文件, 示指定arcname打包文件中将包含文件路径
tar.add('test.txt', arcname='tar_test.txt')
tar.add(r'luffycity-s8\README.md', arcname='tar_readme.txt')
# 添加一个目录
tar.add(r'D:\tmp\test')
# 关闭
tar.close()

# 查看文件列表
tar = tarfile.open('tar_file.tar', 'r')
# 获取包内的所有文件列表
print(tar.getmembers())
# [<TarInfo 'tar_test.txt' at 0x296b3e99d90>, <TarInfo 'tar_readme.txt' at 0x296b3e99f20>]

# 追加
# 以a模式创建文件
tar = tarfile.open('tar_file.tar', 'a')
tar.add('test_new.txt')
tar = tarfile.open('tar_file.tar', 'r')

# 解压全部文件
tar = tarfile.open('tar_file.tar', 'r')
tar.extractall()
tar.close()

# 解压单个文件
# 如果我们的压缩包很大的情况下，就不能够一次性解压了，那样太耗内存了，可以通过下面的方式进行解压，其原理就是一个文件一个文件的解压。
tar = tarfile.open('tar_file.tar', 'r')
for n in tar.getmembers():
    tar.extract(n, "/tmp")
tar.close()
