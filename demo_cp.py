#!/usr/bin/env python
# -*-coding:utf-8 -*-

def copy(path,path2):
    file1=open(path,"r")#原文件
    file2=open(path2,"w+")#新的文件

    try:
        line=file1.readline()
        while line:
            file2.write(line)
            line=file1.readline()
    except Exception as e:
        print("------------------ 1 -------------------------")
        print(e)
    finally:
        file2.close() #后打开的先关闭
        file1.close()

'''
    大文件复制，不区分文本文件和二进制文件
'''
def copy2(path,path2):
    file1=open(path,"r")#原文件
    file2=open(path2,"w+")#新的文件

    try:
        while True:
            line=file1.read(3)
            if not line:
                break
            file2.write(line)
    except Exception as e:
        print("------------------ 1 -------------------------")
        print(e)
    finally:
        file2.close() #后打开的先关闭
        file1.close()


if __name__=="__main__":
   # copy("D:/本机账号.txt.txt","D:/a.txt")
    copy2("D:/personal/DUANHW/Core/survey/src/com/exam/action/Flow(1).java","D:/personal/DUANHW/Core/survey/src/com/exam/action/a.java")