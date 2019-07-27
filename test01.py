import requests

HOSTNAME = ''

HEADERS = {
	'Host': HOSTNAME,
	'Connection': 'keep-alive',
	'Authorization': token,
	# 'Content-Type': 'application/json'

}

def urlParam(param): # param应该是一个dict
	url = ''
	for k, v in param.items:
		url += '?' + '%s=%s'%(k,v)
	return url


def interfaceTest(case_list):
	request_urls = []
	for case in case_list:
		try:
			case_id = case[0]
			interface_name = case[1]
			url = case[2]
			method = case[3]
			param = case[4]
			body = case[5]
			res_check = case[6]
		except:
			return '测试用例格式不正确！'

		if param in ('', 'null'):
			new_url = 'https://' + HOSTNAME + url
		else:
			new_url = 'https://' + HOSTNAME + urlParam(param)

		if method.upper() == 'GET':
			print(str(case_id) + new_url)
			headers = {

			}