#!/usr/bin/env python
# -*-coding:utf-8 -*-

import re
import os,shutil
from class_jt import Fileinfo
import time,datetime
import jt


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
paths={"hs_day":r'D:\personal\DUANHW\test\A\\',"ods_day":r'D:\personal\DUANHW\test\B\\',"jt_day":r'D:\personal\DUANHW\test\C\\'
    ,"hs_month":'',"ods_month":'',"bonc_month":'',"kdgc_month":'',"jt_month":''}


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
    flag_c=0
    flag_v=0
    files=os.listdir(path)  #读取目录中的所有文件
    if len(files)!=0: #如果目录中有文件
        print("=====扫描到 %s 个文件" %(len(files)))
        for f in files:
            if re.match('^.*?\.(CHECK|VAL|gz)$',f) is not None: #匹配只匹配CHECK VAL gz 三类文件
               if os.path.splitext(f)[1]==".CHECK" : #如果是CHECK文件
                   vals=readCheck(path+f) #读取check文件 并且拼接出val文件
                   temp=len(vals)#文件个数
                   for v in vals:
                       if isExist(path+v)==False: #如果val文件不存在
                            break
                       else:#如果val文件存在
                            obj=readVal(path+v)#通过方法返回对象并赋值给新对象
                            datPath=path+obj.getDatName()+".gz" #gz文件名称拼接
                            temp2=0
                            if isExist(datPath)==True:#如果数据文件存在
                                if obj.getDatName().split(".")[2]==obj.getDatDate():#如果数据文件和校验文件中的账期一致
                                    if dateOper(obj.getDatName().split(".")[1],obj.getDatName().split(".")[2])==1:
                                        temp2=temp2+2
                            else:
                                break
                   if temp*2==temp2:
                       move2(path)

    else:
        print("=====扫描到 %s 个文件" %(len(files)))
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
   查找文件是否存在
'''
def isExist(path):
    boolean=True
    [dirname,filename]=os.path.split(path)
    if os.path.exists(path)==True:
        print("%s文件存在" % (filename))
    else:
        print("%s文件不存在" % (filename))
        boolean=False

    return boolean

'''
@file 文件名称 带路径
@toPath 将要移动的目录
'''
def move(file,toPath):
    [dirname,filename]=os.path.split(file)

    if not os.path.isfile(file):
        print("%s 不是一个文件" %(file))
    else:
        if not os.path.exists(toPath):
            os.mkdir(toPath)
        if os.path.exists(toPath+filename)==False:
            print("%s-->%s" %(file,shutil.move(file,toPath)))
        else:
            print("%s 文件已经存在，不能再传" % (toPath+filename))







# 字节数
def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    print(round(fsize,3))
    return round(fsize,3)


# 获取文件大小
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        print( formatSize(size))
    except Exception as err:
        print(err)

# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"

    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%fG" % (G)
        else:
            return "%fM" % (M)
    else:
        return "%fkb" % (kb)


'''
日期加减操作
cdate 创建日期
ddate  数据账期
'''
def dateOper(cdate,ddate):
    day=0
    d1 = datetime.datetime.strptime(cdate, '%Y%m%d')
    d2 = datetime.datetime.strptime(ddate, '%Y%m%d')
    day = d1 - d2
    return day.days

                        # |*日文件共 19 个 当前已上传 2 个
                        # |---DAPD_DIM_MAPPING_PD 已上传 共(3)个文件 CHECK(1); VAL(1);DAT(1);
                        # |------DAPD_DIM_MAPPING_PD.20190318.20190317.00.000.000.862.CHECK
                        # |------DAPD_DIM_MAPPING_PD.20190318.20190317.00.001.001.862.VAL
                        # |------DAPD_DIM_MAPPING_PD.20190318.20190317.00.001.001.862.DAT.gz
def log():
    day=jt.getDAPX("day")
    print("|*日文件共%d个 当前已上传%d" %(len(day),2))


def move2(path):
    files=os.listdir(path)  #读取目录中的所有文件
    if len(files)!=0: #如果目录中有文件
        print("=====扫描到 %s 个文件" %(len(files)))
        for f in files:
            if re.match("^"+f.split(".")[0]+"([.]\d{8}){2}([.]\d{2,3})+\d+\.(CHECK|VAL|DAT)(\.gz)?$",f) is not None:
                move(path+f,"D:/personal/DUANHW/test/C/")

if __name__ == '__main__':
    try:
        for (k,v) in paths.items():
            if(k=="hs_day"):
                getFiles(v)
    except Exception as e:
        print(e)




