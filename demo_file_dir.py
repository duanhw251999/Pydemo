#!/usr/bin/env python
# -*-coding:utf-8 -*-

import os

path="D:/personal/DUANHW/Core/survey/src/com/exam/action/"

files=os.listdir(path)

for f in files:
        print(path+f)