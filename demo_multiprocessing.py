#!/usr/bin/env python
# -*-coding:utf-8 -*-

import multiprocessing
import time,os


'''
  time类的用法
'''
def time_Useage():
    i=20
    while i>0:
        print("--------- 1 ----------------")
        time.sleep(10)
        i=i-1

'''
   本方法中 写了两个循环，每次执行这个方式时，第一个循环总是被先执行，第二个循环后执行
'''
def narmal_process():
    i=20
    while i>0:
        print("    %s,%s" %(multiprocessing.current_process().name,multiprocessing.current_process().pid))
        time.sleep(0.2)
        i=i-1
if __name__ == '__main__':
    print(os.getpid(),"主进程开始...")
    p1=multiprocessing.Process(target=narmal_process)
    p2=multiprocessing.Process(target=narmal_process)

    '''
      以下代码 p1 p2 两个子进程会交替执行，也就是异步执行
        p1.start()
        p2.start()
        p1.join()
        p2.join()
    '''

    '''以下代码两个子进程会按照先后顺序执行，也就是同步执行'''
    p1.start()
    p1.join()
    p2.start()
    p2.join()

    print(os.getpid(),"主进程结束...")