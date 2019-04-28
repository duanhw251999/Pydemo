#!/usr/bin/env python
# -*-coding:utf-8 -*-

import re
import os
from class_jt import Fileinfo
import jt
import Helper,time,threading

'''
日期: 2019-04-21
作者: 段宏伟
'''

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


# paths={"hs_day":'E:/PUT_JT_DATA/The_Temp_Data/The_TEST_Data/DAY/'
#        ,"ods_day":'E:/PUT_JT_DATA/The_Temp_Data/The_TEST_Data/MONTH/'
#        ,"jt_day":'E:/PUT_JT_DATA/The_Temp_Data/The_TEST_Data/DayData/'
#        ,'day_err':'E:/PUT_JT_DATA/The_Temp_Data/The_TEST_Data/err/'}
paths={"hs_day":'D:/personal/DUANHW/test/A/'
,"ods_day":'D:/personal/DUANHW/test/B/'
,"jt_day":'D:/personal/DUANHW/test/C/'
,"hs_month":''
,"ods_month":''
,"bonc_month":''
,"kdgc_month":''
,"jt_month":''
,"day_err":'D:/personal/DUANHW/test/error/'
,"month_err":''}



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
3.删除大小为 0 的文件
4. 删除名称不符合配置文件
5.精准日期控制
        20190421.20190419  如果账期是20190419,且是华盛数据,通过；如果账期是20190419，但不是华盛数据，不通过；
        20190420.20190419  如果账期是20190419，通过  1
        20190419.20190419  如果账期是20190419，通过  0
        20190420.20190418  判断是否是华盛数据，如果是，判断账期是否是20190419，如果账期合适通过，如果账期不合适，不通过

2019/04/22  05:21                57 DAPD_COMBO_SUM_CNT.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:21                61 DAPD_DIM_MAPPING_OFFER.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:21                58 DAPD_DIM_MAPPING_PD.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:21                55 DAPD_DIM_PO_SPEC.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:21                54 DAPD_DIM_REGION.20190421.20190421.00.000.000.862.CHECK
2019/04/22  05:21                56 DAPD_DIM_SUM_TYPE.20190421.20190421.00.000.000.862.CHECK
2019/04/22  05:21                53 DAPD_EVT_TRMNL.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:21                66 DAPD_POINT_MANAGE_CUST_DVLP.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:21                56 DAPD_PRD_ITV_INST.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:21               605 DAPD_PRD_PD_INST.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:23                58 DAPD_PRD_PD_INST_WB.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:23             1,155 DAPD_PRD_PO_INST.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:26             1,140 DAPD_PRD_PO_MEMBER.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:21                53 DAPD_PR_BDM_PA.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:21                53 DAPD_PR_BDM_PM.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:21                53 DAPD_PR_BDM_PP.20190422.20190421.00.000.000.862.CHECK
2019/04/22  05:21                53 DAPD_PR_BDM_PS.20190422.20190421.00.000.000.862.CHECK
DAPD_EVT_CPT_USER.20190422.20190420.00.000.000.862.CHECK.RPT
DAPD_EVT_CPT_BEH.20190422.20190420.00.000.000.862.CHECK.RPT


DAPD_POINT_MANAGE_CUST_DVLP.20190328.20190327.00.000.000.862.CHECK.ERR
DAPD_POINT_MANAGE_CUST_DVLP.20190328.20190327.00.001.001.862.DAT.gz.CON.ERR
DAPD_PRD_PO_MEMBER.20180906.20180905.00.001.002.862.ERR

'''

def arthropoda(path):
    # 0.查看回执文件
    checkRPT(paths["re_day"])
    # 1. 删除大小为0的空文件
    Helper.deleteEmpty(path,paths["day_err"])
    # 2. 剔除名称不属于配置的文件
    Helper.notConf(path,paths["day_err"])
    # 3. 剔除名称不符合规范的文件
    Helper.formatError(path,paths["day_err"])
    # 4. 剔除非账期的文件
    datDate(path)

    files=os.listdir(path)  #读取目录中的所有文件
    if len(files)!=0: #如果目录中有文件
        print("=====扫描到 %s 个文件" %(len(files)))
        for f in files:
            absPath=path+f
            if Helper.isExist(absPath)==True:
               if re.match('^.*?\.(CHECK|VAL|gz)$',f) is not None:
                    if os.path.splitext(f)[1]==".CHECK" : #如果是CHECK文件
                       checkFileOper(absPath)
    else:
        print("=====扫描到 %s 个文件" %(len(files)))


def checkFileOper(absPath):
    [dirname,filename]=os.path.split(absPath)
    if valCheckDate(filename)==1:
        vals=readCheck(absPath)
        count_check=len(vals)#文件个数 根据check文件中的记录行数计算得出
        count_valngz=0
        for val in vals:
            absValPath=dirname+"\\"+val
            if Helper.isExist(absValPath)==True: #如果val文件存在
                obj=readVal(absValPath)#通过方法返回对象并赋值给新对象
                if obj!=None:
                    if validObj(obj,dirname)==True:
                            count_valngz=count_valngz+2
            else:
                break
        if count_check*2==count_valngz:
            move2(filename.split(".")[0],dirname)
#检查CHECK文件的日期与当期日期以及账期是否符合要求
def valCheckDate(filename):
    # d1 生成日期 d2 数据账期 d3 当前日期
    (d1,d2,d3)=(filename.split('.')[1],filename.split('.')[2],Helper.dateNow(0))
    dtflag=0
    if Helper.dateOper(d1,d2)==2:
       if Helper.dateOper(d1,d3)==0 and Helper.dateOper(d3,d2)==2:
           dtflag=1
    elif Helper.dateOper(d1,d2)==1 or Helper.dateOper(d1,d2)==0:
           dtflag=1
    return dtflag
'''
读取CHECK文件内容
'''
def readCheck(file):
    vals=[]  #通过CHECK文件的读取，得出VAL文件的数量和名称
    #如果读取的文件是CHECK文件
    if os.path.splitext(file)[1]==".CHECK" :
        with open(file,"r") as f:
            line=f.readline()
            while line:
                l=line.rstrip('\n')
                vals.append(l.replace("DAT","VAL"))
                line=f.readline()
    return vals

'''处理从校验文件中获取的对象，符合条件的对象返回真否则反之'''
def validObj(obj,dirname):
    flag=False
    Helper.prn_obj(obj) #打印每个val文件中的内容
    absgzName=dirname+"\\"+obj.getDatName()+".gz"
    if Helper.isExist(absgzName)==True:
        if obj.getDatName().split(".")[2]==obj.getDatDate() :
            flag=True
    return flag

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
                Helper.move(path+"/"+f,paths["jt_day"])

''' 如果文件的名字和配置文件中的名称相同 '''
def findDay(name):
    flag=False
    day=""
    days=jt.getDAPX("day")
    if name in days:
        flag=True
    return flag

'''
    DAPD_DIM_MAPPING_PD.20190318.20190317.00.001.001.862.VAL
    d1------------------20190318
    d2------------------20190317
    dc=d1-d2
'''
def datDate(path):
    files=os.listdir(path)
    for f in files:
        absPath=path+f
        dn=f.split('.')[0]
        d1=f.split('.')[1]
        d2=f.split(".")[2]
        dc=Helper.dateOper(d1,d2)
        if dc==1 or dc==0:
            if Helper.dateNow(-1)==d2:
                pass
                # print("%s--当前账期是%s,文件的账期是%s ,[%s],文件可以上传" %(f,Helper.dateNow(-1),d2,dc))
                # Helper.move(absPath,paths["jt_day"])
        elif dc==2:
            if dn in jt.getDAPX("hs_data"):
                #pass
                # print("%s--当前账期是%s,文件的账期是%s ,[%s],华盛可以上传" %(f,Helper.dateNow(-1),d2,dc))
                # Helper.move(absPath,paths["jt_day"])
                d3=Helper.dateNow(0)#当前日期
                if Helper.dateOper(d1,d3)==1 and Helper.dateOper(d3,d2)==1:
                    pass #这种情况，仅做保留，不做挪动，也不上传
                elif Helper.dateOper(d1,d3)==0 and Helper.dateOper(d3,d2)==2:
                    pass #这种情况，直接上传
            else:
                print("%s--非合理账期内数据，将被移动到错误目录"%f)
                Helper.move(absPath,paths["day_err"])
        else:
            print("%s--非合理账期内数据，将被移动到错误目录"%f)
            Helper.move(absPath,paths["day_err"])
#回执文件的查找
def checkRPT(path):
    narmal={}
    files=os.listdir(path)
    if len(files)!=0:
        for file in files:
            absPath=path+file
            if Helper.dateOper(Helper.getFileCreateTime(absPath),Helper.dateNow(0))==0:#只搜索当前日期的回执文件
                if re.match("\w*([.]\d+)+([.]\d+)+([.]\w+)+\.(RPT|ERR)$",file)is not None: #只搜索rpt和err文件
                    if file.split(".")[0] in jt.getDAPX("day"):#只搜索与属于配置文件的
                        #print("%s--%s---%s"%(file,Helper.getFileCreateTime(absPath),os.path.splitext(file)[1]))
                        if file.split(".")[0] not in narmal.keys():
                            if os.path.splitext(file)[1]==".RPT":
                                narmal[file.split(".")[0]]="正常"
                            else:
                                narmal[file.split(".")[0]]="异常"

    if len(narmal)==len(jt.getDAPX("day")):
        for (k,v) in narmal.items():
            print(k+"---"+v)

        ncount=0
        fcount=0
        for v in narmal.values():
            if v=="正常":
                ncount=ncount+1
            if v=="异常":
                fcount=fcount+1
        print("%d个回执全部收到，其中正常[%d],异常[%d]"%(len(narmal),ncount,fcount))

if __name__ == '__main__':
    try:
        while True:
            print('%s 进程号 %s ... /\/\(**<o>**)/\/\\' % ("代号:蜘蛛", os.getpid()))
            print ("Start : %s" % time.ctime())
            time.sleep(15)
            arthropoda(paths["hs_day"])
            print ("End : %s" % time.ctime())
    except Exception  as e:
            print(e)


'''
  把日志做出来
  回执检查
'''