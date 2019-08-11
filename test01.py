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

    conn = MySQLdb.connect(LOGIN)

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
    data = cur.fetchmany()
    for i in data:
        case_list.append(i)

    cur.close()
    conn.commit()            # 读取操作可以忽略改句，修改到数据库数据的必须使用
    conn.close()

    return case_list


def urlParam(param):  # param应该是一个dict
    '''
    组装请求路径
    '''

    url = ''
    for k, v in param.items:
        url = url + '?' + '%s=%s' % (k, v)
    return url


def counting():
    '''
    修改数据库中测试次数
    '''

    conn = MySQLdb.connect(LOGIN)

    cur = conn.cursor()

    flag = cur.execute("select * from counting")
    if flag == 0:   # 表中没有任何记录，则为第一次执行测试
        print(1)
        cur.execute("insert into counting (count) values (1)")
    elif flag == 1:   # 表中有记录，则不为第一次，需要从表中读取数据后，修改表中数据
        print(2)
        count = cur.fetchone()[1]
        print(count)
        cur.execute("update counting set count=%d" % (count+1))
    cur.close()
    conn.commit()
    conn.close()

    print('记录次数成功！')


def addLogs(test_case_id, is_success=1):
    '''
    记录测试用例执行日志，默认执行成功
    '''

    conn = MySQLdb.connect(LOGIN)

    create_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(create_at, type(create_at))

    cur = conn.cursor()
    cur.execute("select * from counting")
    # print(cur.fetchone())
    count = cur.fetchone()[1]
    cur.close()

    cur = conn.cursor()
    cur.execute("insert into logs (count, test_case_id, is_success, create_at) values (%d, %d, %d, '%s')" % (
        count, test_case_id, is_success, create_at))
    cur.close()
    conn.commit()
    conn.close()

    print('记录日志成功！')


def addBugLogs(param_list):
    '''
    记录bug
    '''

    conn = MySQLdb.connect(LOGIN)

    test_case_id = param_list[0]
    request_url = param_list[1]
    method = param_list[2]
    expect_result = param_list[3]
    response = param_list[4]
    result = param_list[5]

    create_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur = conn.cursor()
    cur.execute("select * from counting")
    count = cur.fetchone()[1]
    cur.close()

    cur = conn.cursor()
    cur.execute("insert into bug_logs (count, test_case_id, request_url, method, expect_result, response, result, create_at) values (%d, %d, %s, %s, %s, %s, %s, '%s')" % (
        count, test_case_id, request_url, method, expect_result, response, result, create_at))
    cur.close()
    conn.commit()
    conn.close()

    print('记录bug成功！')


def interfaceTest(case_list):
    request_urls = []
    for case in case_list:
        try:
            case_id = case[0]
            interface_name = case[1]
            host = HOSTS[case[2]]
            url = case[3]
            method = case[4]
            param = case[5]
            body = case[6]
            expect_result = json.loads(case[7])  # str转json，需要严格注意引号，单引号会报错
        except:
            return '测试用例格式不正确！'     # 测试用例格式不正确时，不再继续读取用例，结束测试

        if param in ('', None):
            new_url = 'https://' + host + url
        else:
            new_url = 'https://' + host + url + urlParam(param)

        # if method.upper() == 'GET':
        #     print(str(case_id) + new_url)
        #     headers =

        # if method.upper() == 'POST':

        if method.upper() == 'PUT':

            r = requests.put(new_url, headers=HEADERS, data=body)
            try:
                response = r.json()
            except json.decoder.JSONDecodeError:  # 即返回的状态码不为200
                e_result = "{'status_code': 200}"
                result = "{'status_code': %d}"% r.status_code
                addBugLogs([case_id, new_url, method, e_result, r.text, result])
                addLogs(case_id, interface_name, 0)
            else:
                if response['code'] != expect_result['code']: # 即响应内容与预期不符，目前只判断了响应中的code
                    addBugLogs([case_id, new_url, method, json.dumps(expect_result), r.text, response])
                    addLogs(case_id, interface_name, 0)
                else: # 即用例通过
                    addLogs(case_id, interface_name)


def doTest():
    counting()
    case_list = getCaseList()
    interfaceTest(case_list)


if __name__ == '__main__':
    doTest()
    print('Done!(*￣︶￣)')
