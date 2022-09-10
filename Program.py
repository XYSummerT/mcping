import ping3
from ruamel import yaml
import os
import requests


# 用于检查相关文件是否存在
def CheckFile(file):
    fileFlag = os.path.isfile(file)
    return fileFlag


def CheckIP():
    if CheckFile("./ip.yaml"):
        return True
    else:
        return False


def CheckIPText():
    if CheckIP():
        return "存在"
    else:
        return "不存在"


def CheckOutPut():
    if CheckFile("./output.yaml"):
        return True
    else:
        return False
def mk_output():
    if CheckFile("./output.yaml") == False:
        open("./output.yaml", "x").close()


# 下载所需的ip文件
def Download():
    ipFile = requests.get("https://raw.githubusercontent.com/XYSummerT/mcping/main/ip.yaml", allow_redirects=True)
    open("./ip.yaml", "wb").write(ipFile.content)
    file = open('ip.yaml', 'r', encoding='utf-8')
    file.close()


#读取ip.yaml文件
def read_yaml(file):
    file = open(file, 'r', encoding='utf-8')
    ip = yaml.safe_load(file)
    return ip
#写入output
def write_yaml(pdic):
    with open('output.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(pdic, f, Dumper=yaml.RoundTripDumper)
    f.close()

#ping服务器
def ping_server(ip):
    u_time,t_tag = 0.0,0
    for t in range(2):
        f_time = ping3.ping(ip,timeout=1)
        if f_time != None :
            u_time += f_time
        else:
            t_tag = 1
    u_time = u_time/4
    return u_time,t_tag

#检测并写入文件
def ping_write():
    o_dic = {}
    dic_sess = read_yaml("./ip.yaml")
    ip_sessionserver = dic_sess["sessionserver"]
    for temp_ip in ip_sessionserver:
        a_time,t_tag = ping_server(temp_ip)
        if t_tag == 0:
            o_dic[temp_ip] = a_time
        else:
            o_dic[temp_ip] = 999.0

    p_dic = {}
    dic_auth = read_yaml("./ip.yaml")
    ip_authserver = dic_auth["authserver"]
    for temp_ip in ip_authserver:
        a_time, t_tag = ping_server(temp_ip)
        if t_tag == 0:
            p_dic[temp_ip] = a_time
        else:
            p_dic[temp_ip] = 999.0
    o_dic = sorted(o_dic.items(), key=lambda k: k[1])
    p_dic = sorted(p_dic.items(), key=lambda k: k[1])
    f_dic = {'sessionserver': o_dic, 'authserver': p_dic}  # 将结果写入同一个字典
    write_yaml(f_dic)

#读取output.yaml文件，并以字符串的方式返回
def read_return():
    file = open("./output.yaml","r")
    text = file.read()
    file.close()

    return text