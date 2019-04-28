#!/usr/bin/env python
# -*-coding:utf-8 -*-
import multiprocessing
from multiprocessing import Pool
import time



def run_process(*arr):
        for t in arr:
            time.sleep(0.1)
            print(t,"    %s,%s" % (multiprocessing.current_process().pid,multiprocessing.current_process().name))

if __name__ == '__main__':

    pool=Pool(3)
    pool.map(run_process,[i for i in range(100)])
    pool.close()
    pool.join()