from env_variables import HOSTS, token, LOGIN
import requests
import json
import MySQLdb



HEADERS = {
    # 'Host': HOSTNAME,
    'Authorization': token,
    'Content-Type': 'application/json'
}

def getCaseList(login_information):
    case_list = []

    # 连接数据库
    conn = MySQLdb.connect(
        host=login_information['mysql_host'],
        port=login_information['mysql_port'],
        user=login_information['mysql_user'],
        passwd=login_information['mysql_passwd'],
        db=login_information['db'],
        charset=login_information['charset']   # 这个参数决定python能否正常读取mysql中记录的中文
        )
    cur = conn.cursor()

    cur.execute("select * from test_casess")
    data = cur.fetchmany()
    for i in data:
        case_list.append(i)

    cur.close()
    conn.close()

    return case_list


def urlParam(param): # param应该是一个dict
    url = ''
    for k, v in param.items:
        url = url + '?' + '%s=%s'%(k,v)
    return url


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
            return '测试用例格式不正确！'

        if param in ('', None):
            new_url = 'https://' + host + url
        else:
            new_url = 'https://' + host + url + urlParam(param)

        # if method.upper() == 'GET':
        #     print(str(case_id) + new_url)
        #     headers = 

        # if method.upper() == 'POST':

        if method.upper() == 'PUT':


            print(str(case_id) + new_url)
            headers = HEADERS

            result = requests.put(new_url, headers=headers, data=body).json()
            # print(result['code'], type(result['code']))
            # print(expect_result['code'], type(expect_result['code']))
            if result['code'] != expect_result['code']:

                # 记录bug
                pass
            else:
                print('Test success!')


def doTest():
    case_list = getCaseList(LOGIN)
    interfaceTest(case_list)



if __name__ == '__main__':
    doTest()
    print('Done!(*￣︶￣)')