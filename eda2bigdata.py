#!/usr/bin/env python
# -*-coding:utf-8 -*-

import ftplib,os,Helper
import re
import logging
from mylog import spider_say
conStr={"host":'135.148.9.50',"user":'bigdata_jk',"password":'zte_hadoop2019'}
paths={'day':'/data02/jkfiles/ods_jk/bwt_day/',
       'mon':'/data02/jkfiles/ods_jk/bwt_mon/',
       'local_day':'E:/PUT_JT_DATA/The_BWT_Data/DayData_BAK/',
       'local_mon':'E:/PUT_JT_DATA/The_BWT_Data/MonthData_BAK/'
       }

def ftpconnect():
    ftpobj=None
    try:
        ftpobj=ftplib.FTP(conStr['host'])
        ftpobj.login(conStr['user'],conStr['password'])
        msg=ftpobj.getwelcome()
        spider_say(msg)
    except Exception as e:
        spider_say(e)
    return ftpobj

'''
ftpobj FTP对象
file_remote 远程名称
file_local 本地文件绝对路径
'''
def ftp_upload(ftpobj,file_remote,file_local):
    '''以二进制形式上传文件'''
    if ftpobj is not None:
        #获取当前路径
        ftpobj.cwd(paths["day"])
        bufsize = 1024  # 设置缓冲器大小
        fp = open(file_local, 'rb')
        ftpobj.storbinary('STOR ' + file_remote, fp, bufsize)
        ftpobj.set_debuglevel(0)
        fp.close()

#扫描生成目录
def scan_file(path,ftpobj):
    log="bigdata_day"+Helper.dateNow(0)+".log"
    files=fileValid(path)
    for file in files:
        absPath=path+file
        spider_say(absPath)
        # if read_log(file,log)==True:
        #     write_log(file,log)
        #     ftp_upload(ftpobj,file,absPath)

'''
#在扫描临时文件夹，将文件上传后放入备份文件
def backup_file(path,ftpobj):
    log="local_backup_"+Helper.dateNow(0)+".log"
    files=fileValid(path)
    for file in files:
        absPath=path+file
        if read_log(file,log)==True:
            write_log(file,log)
            bakDir=paths["backup"]+Helper.dateNow(0)
            if os.path.exists(bakDir)==False:
                os.mkdir(bakDir)
            ftp_upload(ftpobj,file,absPath)
            Helper.move(absPath,bakDir)
'''

#文件检查
def fileValid(path):
    fileStr=[]
    files=os.listdir(path)
    if len(files)!=0:
        for file in files:
            absPath=path+file
            if os.path.isfile(absPath)==True:
                if Helper.get_FileSize(absPath)>0:
                    if re.match('^.*?\.(CHECK|VAL|gz)$',file) is not None:
                        if dateValid(file)==True:
                            fileStr.append(file.strip())
    return fileStr


#写入日志
def write_log(file,log):
    with open(log,'a+') as f:
        f.write(file+"\n")
#读取日志
def read_log(file,log):
    flag=True
    readStr=[]
    if Helper.isExist(log)==False:
        f=open(log,"w")
        f.close()

    with open(log,'r') as f:
        line=f.readline()
        while line:
            readStr.append(line.strip())
            line=f.readline()
    if len(readStr)>0:
        for x in readStr:
            if file==x:
                flag=False
                break
    return flag

def dateValid(file):
    d1=file.split(".")[1]
    d2=file.split(".")[2]
    d3=Helper.dateNow(0)

    flag=False
    if Helper.dateOper(d3,d1)==0 and Helper.dateOper(d3,d2)==1:
        flag=True
    elif Helper.dateOper(d3,d1)==1 and Helper.dateOper(d3,d2)==1:
        flag=True
    return flag

def spider_say(msg):
    LOG_FORMAT = "%(process)d - %(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename="bigdata.log",filemode='a', level=logging.DEBUG, format=LOG_FORMAT)
    logging.info(msg)

if __name__ == '__main__':
    print("==================================================开始执行大数据日表上传")
    ftpobj=ftpconnect()
    try:
        scan_file(paths["local_day"],ftpobj)
    except Exception as e:
        spider_say(e)
    finally:
        ftpobj.quit()
        print("==================================================结束大数据日表上传")
