# -*- coding: utf-8 -*-


from ruamel import yaml
from ping3 import ping
import os
import requests



#检测相关文件是否存在
def Flag(file):
    fileFlag = os.path.isfile(file)
    return fileFlag
if Flag("./ip.yaml"):
    file = open('ip.yaml', 'r', encoding='utf-8')
    ip = yaml.safe_load(file)
else:
    userInput = input("是否自动下载ip文件\nyes or no\n")
    if userInput == "yes":
        print("正在尝试下载，若下载失败请尝试手动下载")
        print("下载地址:https://raw.githubusercontent.com/XYSummerT/mcping/main/ip.yaml")
        ipFile = requests.get("https://raw.githubusercontent.com/XYSummerT/mcping/main/ip.yaml",allow_redirects=True)
        open("./ip.yaml","wb").write(ipFile.content)
        file = open('ip.yaml', 'r', encoding='utf-8')
        ip = yaml.safe_load(file)
    else:
        print("请手动下载")
        print("下载地址:https://raw.githubusercontent.com/XYSummerT/mcping/main/ip.yaml")
        exit()
if Flag("./output.yaml"):
    def write_yaml(pdic):
        with open('output.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(pdic, f, Dumper=yaml.RoundTripDumper)
else:
    open("./output.yaml","x")
    def write_yaml(pdic):
        with open('output.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(pdic, f, Dumper=yaml.RoundTripDumper)




#ping服务器
def ping_server(ip):
    uTime,tTag = 0.0,0
    for t in range(2):
        fTime = ping(ip,timeout=1)
        if fTime != None :
            uTime += fTime
        else:
            tTag = 1
    uTime = uTime/4
    return uTime,tTag











time = 0





#询问用户
qlist = ['help','ping','exit','print']
answer = str(input("本程序将会帮您配置hosts，以下是命令帮助：\nhelp:帮助\nping:测试延迟\nprint:打印出延迟记录\nexit:退出\n"))
while answer != 'exit':#检测用户输入
    while answer not in qlist:
        answer = input('请输入正确的指令:\nhelp:帮助\nping:测试延迟\nprint:打印出延迟记录\nexit:退出\n')
    else:
        if answer == 'help':
            answer = input('help:帮助\nping:测试延迟\nprint:打印出延迟记录\nexit:退出\n')
        elif answer == "ping":
           time += 1
           print("请稍等")
           ips = ip['sessionserver']
           print("正在ping sessionserver")
           odic = {}
           for ipss in ips:#循环ping服务器
               atime,ttag = ping_server(ipss)
               if ttag == 0:
                   odic[ipss] = atime
               else:
                   odic[ipss] = 999.0
               print(ipss,atime,ttag)
           print("正在ping authserver")
           ips = ip['authserver']
           pdic = {}
           for ipss in ips:
               atime,ttag = ping_server(ipss)
               if ttag == 0:
                   pdic[ipss] = atime
               else:
                   pdic[ipss] = 999.0
               print(ipss, atime, ttag)
           odic = sorted(odic.items(),key = lambda k:k[1])
           pdic = sorted(pdic.items(), key=lambda k: k[1])
           fdic = {'sessionserver':odic,'authserver':pdic}#将结果写入同一个字典
           write_yaml(fdic)
           print(fdic)
           answer = input("结果已保存到output.yaml\n请输入指令\n")


        else:
            if time >= 1:
                for oip in fdic:
                    for ptime in fdic[oip]:
                        print(oip,ptime)
                    answer = 'help'


            else:
                print("请至少ping一次后使用此功能")
                answer = 'help'
else:
    pass