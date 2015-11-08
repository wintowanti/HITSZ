# -*- coding: utf-8 -*-
from weibo import APIClient
import webbrowser#python内置的包
APP_KEY = '2825855918'#注意替换这里为自己申请的App信息
APP_SECRET = '59bf15cd9d3d8bddf23065241d333c11'
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'#回调授权页面
#利用官方微博SDK
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
print dir(client)
#得到授权页面的url，利用webbrowser打开这个url
url = client.get_authorize_url()
print url
webbrowser.open_new(url)
#获取code=后面的内容
print '输入url中code后面的内容后按回车键：'
code = raw_input()
#code = your.web.framework.request.get('code')
#client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
r = client.request_access_token(code)
access_token = r.access_token # 新浪返回的token，类似abc123xyz456
expires_in = r.expires_in
# 设置得到的access_token
client.set_access_token(access_token, expires_in)

#可以打印下看看里面都有什么东西
#print client.statuses__public_timeline()
print "-----------------------------------------------"
print dir(client)
dic = client.statuses.home_timeline.get()
statuses = dic["statuses"]
for item in statuses:
    print item.text
'''
#获取授权用户及其关注好友的微博信息并写入mongo数据库
pagenum=1#微博API返回的微博数据是分页形式的，在API中通过设置页码来读取数据
write_location=MongoClient('localhost',27017)['data']['weiboapi_test']#这里是我自己的mongo数据库，不用mongo存储可以注释掉
while(True):
	data=client.statuses.friends_timeline.get(page=pagenum)['statuses']
	if data:
		pagenum+=1#不断获取新的页面
		for i in range(len(data)):
			write_location.insert(data[i])#不用mongo存储可以注释掉，直接改为print data[i]打印微博数据
	else:#如果读取完数据则结束
		break
'''
