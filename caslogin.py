
# coding=utf-8

import requests
import re
#import pymysql
# from sshtunnel import SSHTunnelForwarder
"""
实现API接口不同环境不同cookie的自动登陆配置功能
根据传入的参数，实现自动获取对应模版的url，并自动返回对应模块的cookie

"""

''' 账号配置 '''
username = '2018xxxxx'
password = 'xxx123456'


''' API地址配置 '''
test_dict = {
    "test":  "http://test.xxxx.com.cn"}


uat_dict = {
    "basedata": "http://uat.xxxx.com.cn",
    "sale": "http://uat.xxxx.com.cn",
    "store": "http://uat.xxxx.com.cn",
    "stock": "http://uat.xxxx.com.cn",
    "price": "http://uat.xxxx.com.cn"}

pro_dict = {
    "basedata":"http://prod.xxxx.com.cn",
    "sale":"http://prod.xxxx.com.cn",
    "store":"http://prod.xxxx.com.cn",
    "stock":"http://prod.xxxx.com.cn",
    "price": "http://prod.xxxx.com.cn"}


""" 1:test | 2:uat | 3:prod """
def get_cas_url(env):

    if env == 1:
        url = 'https://test.xxxx.com.cn/caslogin'
        return url
    elif env == 2:
        url = 'https://uat.xxxx.com.cn/caslogin'
        return url
    elif env == 3:
        url = 'https://prod.xxxx.com.cn/caslogin'
        return url
    else:
        print('输入参数{}匹配不到登录地址！'.format(env))




switchs = {
        0: "basedata",
        1: "sale",
        2: "store",
        3: "stock",
        4: "price"}


def get_env(env=None, mode=None):
    try:
        if env == 1:
            return test_dict['test']
        elif env == 2 and mode == 0:
            return uat_dict['basedata']
        elif env == 2 and mode == 1:
            return uat_dict['sale']
        elif env == 2 and mode == 2:
            return uat_dict['store']
        elif env == 2 and mode == 3:
            return uat_dict['stock']
        elif env == 2 and mode == 4:
            return uat_dict['price']
        elif env == 3 and mode == 0:
            return pro_dict['basedata']
        elif env == 3 and mode == 1:
            return pro_dict['sale']
        elif env == 3 and mode == 2:
            return pro_dict['store']
        elif env == 3 and mode == 3:
            return pro_dict['stock']
        elif env == 3 and mode == 4:
            return pro_dict['price']
        else:
            print('输入参数env={}或mode={}匹配不到模块地址'.format(env,mode))
    finally:
        with open('url_tag.txt', 'w') as file:
            file.write(str(env))



def get_cookies():

    with open('url_tag.txt', 'r') as file:
        tag = file.read()

    session = requests.Session()
    response = session.get(get_cas_url(int(tag)))
    # 获取execution的value
    get_execution = re.search('name="execution" value="(.*?)"/>', response.content.decode("utf-8"), re.S)
    form_data = {"username": username,
                "password": password,
                "authenticationType": "usernamePassword",
                "execution": get_execution.group(1),
                "_eventId": "submit"}
    # 单点登录
    s = session.post(get_cas_url(int(tag)), data=form_data)
    print(s.cookies)


    if int(tag) == 1:
        cookie = 'TEST_JSESSIONID=' + session.cookies['JSESSIONID']
        return (cookie)


    elif int(tag) == 2:
        cookie = 'UAT_JSESSIONID=' + session.cookies['UAT_JSESSIONID']
        return (cookie)


    elif int(tag) == 3:
        cookie = 'PROD_JSESSIONID=' + session.cookies['PROD_JSESSIONID']
        return (cookie)

    else:
        print('输入参数{}匹配不到对应cookie'.format(tag))




