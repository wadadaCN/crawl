# 2018.1.11

import requests
from lxml import etree

url = 'http://yjxt.bupt.edu.cn/'
# header1 is used on yjxt, header2 is used on auth
headers1 = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'Host':'yjxt.bupt.edu.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
headers2 = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'DNT':'1',
'Host':'auth.bupt.edu.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}

r = requests.get(url, headers=headers1, allow_redirects=False) #request header need last response header's info
tree = etree.HTML(r.text)
newUrl = tree.xpath("//a/@href")[0]

r = requests.get(newUrl, headers=headers2, allow_redirects=False) #get auth site response header and fulfil header2
Cookie = r.headers['Set-Cookie'].split(';')[0]
headers2['Referer'] = newUrl
headers2['Cookie'] = Cookie
headers2['Origin'] = 'http://auth.bupt.edu.cn'
tree = etree.HTML(r.text)
hiddenInput = tree.xpath("//input[@type='hidden']")
username = input('请输入账号：')
password = input('请输入密码：')
data = {'username':username,'password':password,'lt':hiddenInput[0].attrib['value'],'execution':hiddenInput[1].attrib['value'],'_eventId':hiddenInput[2].attrib['value'],'rmShown':hiddenInput[3].attrib['value']}

r = requests.post(newUrl, data=data, headers=headers2, allow_redirects=False) #submit data

headers1['Referer'] = newUrl
newUrl = r.headers['Location']

r = requests.get(newUrl, headers=headers1, allow_redirects=False) #get new cookie

newUrl = r.headers['Location']
Cookie = r.headers['Set-Cookie'].split(';')[0]
headers1['Cookie'] = Cookie
r = requests.get(newUrl, headers=headers1, allow_redirects=False) #test is whether success or not
if r.status_code == 200:
    status = True
else:
    status = False
