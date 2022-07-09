# coding=utf-8

import pyotp
import pymysql
from sshtunnel import SSHTunnelForwarder
import random

"""
1. 解决otp身份宝随机生成验证码
2. 解决通过跳板机隧道连接mysql数据库
3. 解决数据库查询，根据传入不同参数自动查询对应数据库的数据

"""


'''MySQL配置'''
ssh_username = '2018xxxx'  # 堡垒机or跳板机账号
ssh_password = 'xxxxx123456'

mysqlconf = [{"test":"10.8.32.x", "port":3306, "username":"test", "password":"xxxxc6MNpeTxxx"},
             {"uat":"10.8.32.x", "port":3306, "username":"uat_devquery", "password":"xxxxc6MNpeTxxx"},
             {"basedata_prod":"10.8.32.x", "port":3306, "username":"prod_query", "password":"OfKsdxxxxxPMA1lf"},
             {"order_prod":"10.8.32.x", "port":3306, "username":"prod_query", "password":"OfKsdxxxxxPMA1lf"},
             {"store_prod":"10.8.32.x", "port":3306, "username":"prod_query", "password":"OfKsdxxxxxPMA1lf"},
             {"finance_prod":"10.8.32.x", "port":3306, "username":"prod_query", "password":"OfKsdxxxxxPMA1lf"}]


"""
   env=1标识，test环境DB配置（所有模块）
   env=2标识，uat环境DB配置（所有模块）
   env=3,db=0标识，正式环境基础数据DB配置
   env=3,db=1&db=4标识，正式环境采购-销售-价格DB配置
   env=3,db=2 标识，正式环境门店运营DB配置
   env=3,db=5 标识，正式环境门店财务管理配置
   
"""

def getdbconf(db=None):
    with open('url_tag.txt','r') as file:
        env = int(file.read())
        print(env)
    if env == 1:
        return mysqlconf[0]
    elif env == 2:
        return mysqlconf[1]
    if (env == 3 and db == 0):
        return mysqlconf[2]
    elif (env == 3 and db == 1) or (env == 3 and db == 4):
        return mysqlconf[3]
    elif (env == 3 and db == 2):
        return mysqlconf[4]
    elif (env == 3 and db == 5):
        return mysqlconf[5]
    else:
        print('输入参数env={}或db={}匹配不到对应数据库'.format(env, db))

# print(getdbconf())

# 随机生成一次性密码
def totp():
    secret_key = 'M2FFMWSOMDPOWDRXH65GVHTYJBTT72QK' # 堡垒机秘钥
    otp = pyotp.TOTP(secret_key).now() # 生成基于当前时间随机密码30s
    return otp

    # print(pyotp.TOTP.verify(158044))验证是否与手机动态码一致

def sqlQuery(sql,row:int=0,column:int=0,db=None):
    config = list(getdbconf(db).values())
    with SSHTunnelForwarder(
            ssh_address_or_host=('xx.xxxx.com.cn', 60022),  # 堡垒机or跳板机IP与端口
            ssh_username=ssh_username,  # 堡垒机账号
            ssh_password=ssh_password + totp(),  # 堡垒机密码+身份宝随机密码
            remote_bind_address=(config[0],config[1])
    ) as  server:
        database = pymysql.connect(
            host='127.0.0.1',  # 必须是本地IP
            port=server.local_bind_port,  # 绑定本地端口属性
            user=config[2],  # 数据库账号
            password=config[3],  # 数据库密码
            # database='xxxorder' # 数据名称
        )

        cur = database.cursor()
        cur.execute(sql)
        # [row]几行 [column]列
        return cur.fetchall()[row][column]

