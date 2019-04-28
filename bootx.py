#!/usr/bin/env python
# -*-coding:utf-8 -*-

import re
import os
from class_jt import Fileinfo
import jt
import Helper


'''
hs_day  华盛日目录
ods_day ods日目录
jt_day 集团日目录
hs_month 华盛月目录
ods_month ods月目录
bonc_month 东方国信月目录
kdgc_month 科大月目录
jt_month 集团月目录
'''

paths={"hs_day":'E:/PUT_JT_DATA/The_Temp_Data/The_TEST_Data/DAY/',"ods_day":'E:/PUT_JT_DATA/The_Temp_Data/The_TEST_Data/MONTH/',"jt_day":'E:/PUT_JT_DATA/The_Temp_Data/The_TEST_Data/DayData/'}


'''
集团数据校验过程：
1.读取目录中的文件，如果有文件，分别查看CHECK VAL gz文件
    读出CHECK文件中的内容 拼接校验文件名称
        通过拼接出的名称去当前目录查找文件，
            VAL文件存在 文件大小不为0 通过
                读取VAL文件,得到dat.gz文件名称，大小，行数，账期 时间戳
                   如果大小为0 行数为0 报异常
                   否则，查看dat.gz文件是否存在，且账期是否与VAL文件中的账期是否一致，如果一致 通过
                    通过即可对该数据进行上传，并对上传过程做好日志：
                        |*日文件共 19 个 当前已上传 2 个
                        |---DAPD_DIM_MAPPING_PD 已上传 共(3)个文件 CHECK(1); VAL(1);DAT(1);
                        |------DAPD_DIM_MAPPING_PD.20190318.20190317.00.000.000.862.CHECK
                        |------DAPD_DIM_MAPPING_PD.20190318.20190317.00.001.001.862.VAL
                        |------DAPD_DIM_MAPPING_PD.20190318.20190317.00.001.001.862.DAT.gz
            VAL文件不存在 不做任何操作
2.如果目录中没有文件 不做任何操作
'''
def getFiles(path):
    files=os.listdir(path)  #读取目录中的所有文件
    if len(files)!=0: #如果目录中有文件
        print("=====扫描到 %s 个文件" %(len(files)))
        for f in files:
            absPath=path+f
            if Helper.isExist(absPath)==True:
                if Helper.get_FileSize(absPath)!=0:
                       if re.match('^.*?\.(CHECK|VAL|gz)$',f) is not None:
                            if os.path.splitext(f)[1]==".CHECK" : #如果是CHECK文件
                               checkFileOper(absPath)
                else:#如果文件大小为0 挪入错误文件夹
                    Helper.move(absPath,paths["day_err"])
    else:
        print("=====扫描到 %s 个文件" %(len(files)))


def checkFileOper(absPath):
    [dirname,filename]=os.path.split(absPath)
    datName=filename.split('.')[0]
    if findDay(datName)[0]==True:
        vals=readCheck(absPath)
        count_check=len(vals)#文件个数 根据check文件中的记录行数计算得出
        count_valngz=0
        for val in vals:
            absValPath=dirname+"\\"+val
            if Helper.isExist(absValPath)==True: #如果val文件存在
                obj=readVal(absValPath)#通过方法返回对象并赋值给新对象
                if obj!=None:
                    dayCha=valFileOper(obj,dirname)
                    if dayCha==1 or dayCha==0:
                        count_valngz=count_valngz+2
                    if dayCha==2:
                        if findDay(obj.getDatName().split(".")[0])[1]== "DAPD_EVT_CPT_BEH" or findDay(obj.getDatName().split(".")[0])[1]== "DAPD_EVT_CPT_USER":
                           count_valngz=count_valngz+2
            else:
                break
        if count_check*2==count_valngz:
            move2(filename.split(".")[0],dirname)


def valFileOper(obj,dirname):
    dayCha=0
    datName=obj.getDatName()
    datPath=dirname+"\\"+datName+".gz" #gz文件名称拼接
    if Helper.isExist(datPath)==True:#如果数据文件存在
        dateVal=datName.split(".")[2]#校验文件中 文件名称部分中的账期
        dateVal2=obj.getDatDate()#校验文件中的账期
        if dateVal==dateVal2:#如果数据文件和校验文件中的账期一致
            dayCha=Helper.dateOper(datName.split(".")[1],datName.split(".")[2])#日期差
    return dayCha


'''
读取CHECK文件内容
'''
def readCheck(file):
    vals=[]  #通过CHECK文件的读取，得出VAL文件的数量和名称
    #datas=[] #通过CHECK文件的读取，得出data文件的数量和名称 注意，是压缩文件

    #如果读取的文件是CHECK文件
    if os.path.splitext(file)[1]==".CHECK" :
        with open(file,"r") as f:
            line=f.readline()
            while line:
                l=line.rstrip('\n')

                vals.append(l.replace("DAT","VAL"))
                #datas.append(l+".gz")
                line=f.readline()
    return vals

'''
 读取VAL文件
'''
def readVal(file):
    #如果读取的文件是VAL文件
    obj=Fileinfo()
    if os.path.splitext(file)[1]==".VAL":
        with open(file,"r") as f:
            line=f.readline()
            obj.setDatName(line.split("")[0])
            obj.setSize(line.split("")[1])
            obj.setRow(line.split("")[2])
            obj.setDatDate(line.split("")[3])
            obj.setTime(line.split("")[4])

        if obj.getRow()=="0" or obj.getSize()=="0":
            print("文件有误不能上传--记录数为0或文件大小为0")

    return obj



'''
name 数据文件的名字 如DAPD_DIM_MAPPING_PD

'''
def move2(name,path):
    files=os.listdir(path)  #读取目录中的所有文件
    if len(files)!=0: #如果目录中有文件
        for f in files:
            if re.match("^"+name+"([.]\d{8}){2}([.]\d{2,3})+\d+\.(CHECK|VAL|DAT)(\.gz)?$",f) is not None:
                Helper.move(path+"\\"+f,paths["jt_day"])

''' 如果文件的名字和配置文件中的名称相同 '''
def findDay(name):
    flag=False
    day=""
    days=jt.getDAPX("day")
    for d in days:
        if name==d :
            flag=True
            day=d
            break
    return flag,day


if __name__ == '__main__':

    getFiles(paths["hs_day"])







