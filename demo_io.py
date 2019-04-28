#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
得到当前工作目录，即当前Python脚本工作的目录路径: os.getcwd()

返回指定目录下的所有文件和目录名:os.listdir()

函数用来删除一个文件:os.remove()

删除多个目录：os.removedirs（r“c：\python”）

检验给出的路径是否是一个文件：os.path.isfile()

检验给出的路径是否是一个目录：os.path.isdir()

判断是否是绝对路径：os.path.isabs()

检验给出的路径是否真地存:os.path.exists()

返回一个路径的目录名和文件名:os.path.split()     eg os.path.split('/home/swaroop/byte/code/poem.txt') 结果：('/home/swaroop/byte/code', 'poem.txt')

分离扩展名：os.path.splitext()

获取路径名：os.path.dirname()

获取文件名：os.path.basename()

运行shell命令: os.system()

读取和设置环境变量:os.getenv() 与os.putenv()

给出当前平台使用的行终止符:os.linesep    Windows使用'\r\n'，Linux使用'\n'而Mac使用'\r'

指示你正在使用的平台：os.name       对于Windows，它是'nt'，而对于Linux/Unix用户，它是'posix'

重命名：os.rename（old， new）

创建多级目录：os.makedirs（r“c：\python\test”）

创建单个目录：os.mkdir（“test”）

获取文件属性：os.stat（file）

修改文件权限与时间戳：os.chmod（file）

终止当前进程：os.exit（）

获取文件大小：os.path.getsize（filename）
'''
'''
'''

'''
  以下为标准写法
'''
def standard():
    try:
        c=open("D:\personal\DUANHW\待办.txt","r")
        print(c.read()) #使用此方法，如果文件超过10G 会填满内存造成内存严重不足，内存溢出等问题
    except FileNotFoundError as e:
        print (e)
    finally:
        if c:
            c.close()

'''
  进阶写法
'''

def upgrad():
    try:
        with open("D:\personal\DUANHW\待办.txt","r") as f:
            print(f.read())
    except FileNotFoundError as e:
        print(e)

def loop():
        try:
            with open("D:\personal\DUANHW\待办.txt","r") as f:
                line=f.readline()
                while line:
                    print(line)
                    line=f.readline()
        except FileNotFoundError as e:
            print(e)
def loop2():
        try:
            with open("D:\personal\DUANHW\待办.txt","r") as f:
                line=f.readlines()
                for l in line:
                    print(l.rstrip('\n'))#rstrip('\n') 剔除本方法自动为每行读取的内容添加的换行符

        except FileNotFoundError as e:
            print(e)

def readBiny():
        try:
            with open("D:\personal\DUANHW\医院系统\QQ截图20181214093252.png","rb") as f:
                for l in f.readlines():
                    print(l.strip())

        except FileNotFoundError as e:
            print(e)

def read_CharCoding():
        try:
            with open("D:\personal\DUANHW\待办.txt","r",encoding="gbk") as f:
                for l in f.readlines():
                    print(l.strip())

        except FileNotFoundError as e:
            print(e)


def demo_StringIO():
        from io import StringIO  # 妈的这种写法很骚

        f=StringIO()
        f.write("hello")
        f.write(" duanhw")
        print (f.getvalue())  #getvalue()方法用于获得写入后的str。

def demo_StringIO2():
    from io import StringIO  # 妈的这种写法很骚

    f=StringIO("Hello,\nlook one's best")
    while 1==1:
        s=f.readline()
        if s=='':
            break
        print (s.strip())

def demo_BytesIO():
        from io import BytesIO  # 妈的这种写法很骚
        f=BytesIO()
        f.write("中文".encode("utf-8"))
        print (f.getvalue())

        print(BytesIO(b'\xe4\xb8\xad\xe6\x96\x87').read())

demo_BytesIO()