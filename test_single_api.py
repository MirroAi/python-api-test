# -*- coding: utf-8 -*-
# @Author: MirrorAi
# @Date:   2019-08-17 19:56:54
# @Last Modified by:   MirroAi
# @Last Modified time: 2019-08-17 20:34:59


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
        charset=login_information['charset']   # 这个参数决定python能否正常读取mysql中记录的中文
    )
    return conn


def getCaseList():
    '''
    从数据库中读取测试用例
    '''

    conn = connectMySQL(LOGIN)

    case_list = []

    # 连接数据库
    # conn = MySQLdb.connect(
    #     host=login_information['mysql_host'],
    #     port=login_information['mysql_port'],
    #     user=login_information['mysql_user'],
    #     passwd=login_information['mysql_passwd'],
    #     db=login_information['db'],
    #     charset=login_information['charset']    这个参数决定python能否正常读取mysql中记录的中文
    #     )
    cur = conn.cursor()

    cur.execute("select * from test_case")
    data = cur.fetchall()
    for i in data:
        case_list.append(i)

    # print(case_list)

    cur.close()
    conn.commit()            # 读取操作可以忽略改句，修改到数据库数据的必须使用
    conn.close()

    return case_list


def urlParam(param):  # param应该是一个dict
    '''
    组装请求路径
    '''

    url = ''
    flag = 0
    for k, v in param.items():
        flag += 1
        if flag == 1:
            url += '?'
        else:
            url += '&'
        url += '%s=%s' % (k, v)
    return url


def counting():
    '''
    修改数据库中测试次数
    '''

    conn = connectMySQL(LOGIN)

    cur = conn.cursor()

    flag = cur.execute("select * from counting")
    if flag == 0:   # 表中没有任何记录，则为第一次执行测试
        cur.execute("insert into counting (type, count) values (0, 1)")
    elif flag == 1:   # 表中有记录，则不为第一次，需要从表中读取数据后，修改表中数据
        # 这里需要修改，改了counting表
        count_num = cur.fetchone()[1]
        cur.execute("update counting set count=%d" % (count_num+1))
    cur.close()
    conn.commit()
    conn.close()

    print('记录次数成功！')


def addLogs(test_case_id, test_case_name, is_success=1):
    '''
    记录测试用例执行日志，默认执行成功
    '''

    conn = connectMySQL(LOGIN)

    create_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(create_at, type(create_at))

    cur = conn.cursor()
    cur.execute("select * from counting")
    count_num = cur.fetchone()[1]
    cur.close()

    insert_string = '''
    insert into logs (
        count, 
        test_case_id, 
        test_case_name, 
        is_success, 
        create_at) 
    values (
        %d, 
        %d, 
        '%s', 
        %d, 
        '%s')''' % (
        count_num, 
        test_case_id, 
        test_case_name, 
        is_success, 
        create_at)

    cur = conn.cursor()
    cur.execute(insert_string)
    cur.close()
    conn.commit()
    conn.close()

    print('记录日志成功！')


def addBugLogs(param_list):
    '''
    记录bug
    '''

    conn = connectMySQL(LOGIN)

    test_case_id = param_list[0]
    test_case_name = param_list[1]
    request_url = param_list[2]
    method = param_list[3]
    expect_result = param_list[4]
    response = param_list[5]
    result = param_list[6]

    create_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur = conn.cursor()
    cur.execute("select * from counting")
    count_num = cur.fetchone()[1]
    cur.close()

    insert_string = '''
    insert into bug_logs (
        count, 
        test_case_id, 
        test_case_name, 
        request_url, 
        method, 
        expect_result, 
        response, 
        result, 
        create_at) 
    values (
        %d, 
        %d, 
        '%s', 
        '%s', 
        '%s', 
        '%s', 
        '%s', 
        '%s', 
        '%s')''' % (
        count_num, 
        test_case_id, 
        test_case_name, 
        request_url, 
        method, 
        expect_result, 
        response, 
        result, 
        create_at)

    cur = conn.cursor()
    cur.execute(insert_string)
    cur.close()
    conn.commit()
    conn.close()

    print('记录bug成功！')


def assertSth(r, param_list):  # r为request对象， param_list为list
    '''
    每种方法目前使用的断言以及记录流程是一样的
    '''
    case_id = param_list[0]
    interface_name = param_list[1]
    new_url = param_list[2]
    method = param_list[3]
    expect_result = param_list[4]


    try:    # 目前只判断了状态码和约定功能正常的状态码
        response = r.json()
    except json.decoder.JSONDecodeError:
        e_result = '{"status_code": 200}'
        result = '{"status_code": %d}' % r.status_code
        addLogs(case_id, interface_name, 0)
        addBugLogs([case_id, interface_name, new_url, method, e_result, r.text, result])
    else:
        if response['code'] != expect_result['code']:
            addLogs(case_id, interface_name, 0)
            addBugLogs([case_id, interface_name, new_url, method, json.dumps(expect_result), r.text, r.text])
        else:
            addLogs(case_id, interface_name)


def interfaceTest(case_list):
    # request_urls = []
    for case in case_list:
        try:
            case_id = case[0]
            interface_name = case[1]
            host = HOSTS[case[2]]
            url = case[3]
            method = case[4]
            param = case[5]
            body = case[6]
            expect_result = json.loads(case[7])  # str转json，得到一个dict，需要严格注意引号，单引号会报错，空字符串也会报错
        except:
            return '测试用例格式不正确！'     # 测试用例格式不正确时，不再继续读取用例，结束测试

        if param in ('', None):
            new_url = 'https://' + host + url
        else:
            new_url = 'https://' + host + url + urlParam(json.loads(param))


        if method.upper() == 'GET':
            print('sending get request...')
            
            r = requests.get(new_url, headers=HEADERS, params=param)
            # try:
            #     response = r.json()
            # except json.decoder.JSONDecodeError:
            #     e_result = '{"status_code": 200}'
            #     result = '{"status_code": %d}' % r.status_code
            #     addLogs(case_id, interface_name, 0)
            #     addBugLogs([case_id, interface_name, new_url, method, e_result, r.text, result])
            # else:
            #     if response['code'] != expect_result['code']:
            #         addLogs(case_id, interface_name, 0)
            #         addBugLogs([case_id, interface_name, new_url, method, json.dumps(expect_result), r.text, r.text])
            #     else:
            #         addLogs(case_id, interface_name)
            assertSth(r, [case_id, interface_name, new_url, method, expect_result])

        if method.upper() == 'POST':
            print('sending post request...')

            r = requests.post(new_url, headers=HEADERS, data=body)
            # try:
            #     response = r.json()
            # except json.decoder.JSONDecodeError:
            #     e_result = '{"status_code": 200}'
            #     result = '{"status_code": %d}' % r.status_code
            #     addLogs(case_id, interface_name, 0)
            #     addBugLogs([case_id, interface_name, new_url, method, e_result, r.text, result])
            # else:
            #     if response['code'] != expect_result['code']:
            #         addLogs(case_id, interface_name, 0)
            #         addBugLogs([case_id, interface_name, new_url, method, json.dumps(expect_result), r.text, r.text])
            #     else:
            #         addLogs(case_id, interface_name)
            assertSth(r, [case_id, interface_name, new_url, method, expect_result])

        if method.upper() == 'PUT':
            print('sending put request...')

            r = requests.put(new_url, headers=HEADERS, data=body)
            # try:
            #     response = r.json() 
            # except json.decoder.JSONDecodeError:  # 即返回的状态码不为200
            #     e_result = '{"status_code": 200}'
            #     result = '{"status_code": %d}' % r.status_code
            #     addLogs(case_id, interface_name, 0)
            #     addBugLogs([case_id, interface_name, new_url, method, e_result, r.text, result])
            # else:
            #     if response['code'] != expect_result['code']:  # 即响应内容与预期不符，目前只判断了响应中的code
            #         addLogs(case_id, interface_name, 0)
            #         addBugLogs([case_id, interface_name, new_url, method, json.dumps(expect_result), r.text, r.text])
            #     else:  # 即用例通过
            #         addLogs(case_id, interface_name)
            assertSth(r, [case_id, interface_name, new_url, method, expect_result])


        if method.upper() == 'DELETE':
            print('sending delete request...')

            r = requests.delete(new_url, headers=HEADERS, data=body)
            # try:
            #     response = r.json()
            # except json.decoder.JSONDecodeError:
            #     e_result = '{"status_code": 200}'
            #     result = '{"status_code": %d}' % r.status_code
            #     addLogs(case_id, interface_name, 0)
            #     addBugLogs([case_id, interface_name, new_url, method, e_result, r.text, result])
            # else:
            #     if response['code'] != expect_result['code']:
            #         addLogs(case_id, interface_name, 0)
            #         addBugLogs([case_id, interface_name, new_url, method, json.dumps(expect_result), r.text, r.text])
            #     else:
            #         addLogs(case_id, interface_name)
            assertSth(r, [case_id, interface_name, new_url, method, expect_result])


def doTest():
    counting()
    case_list = getCaseList()
    interfaceTest(case_list)


if __name__ == '__main__':
    doTest()
    print('Done!(*￣︶￣)')
