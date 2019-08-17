# -*- coding: utf-8 -*-
# @Author: MirrorAi
# @Date:   2019-08-17 20:00:57
# @Last Modified by:   MirroAi
# @Last Modified time: 2019-08-17 20:04:26

from env_variables import HOSTS, token, LOGIN
import requests
import json
import MySQLdb
import datetime


HEADERS = {
    'Authorization': token,
    'Content-Type': 'application/json'
}

def connectMySQL(login_information):
    '''
    连接数据库
    '''

    conn = MySQLdb.connect(
        host=login_information['mysql_host'],
        port=login_information['mysql_port'],
        user=login_information['mysql_user'],
        passwd=login_information['mysql_passwd'],
        db=login_information['db'],
        charset=login_information['charset']
    )
    return conn

    