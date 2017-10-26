# code = python3
# encoding = utf-8
# wrote by Xie on 2017/10/21
# get the static website's form data, like the xicidaili.com.

import requests
from lxml import etree
import time

url = 'http://www.xicidaili.com/nn/'
headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

r = requests.get(url,headers=headers)
html = etree.HTML(r.text)
ip_list = html.xpath("//table[@id='ip_list']/tr")
contentList = []
title = ''
for i in range(2,11):
    title += (ip_list[0].xpath(".//th[%d]/text()"%i)[0] + ' ')
title += '\n'
contentList.append(title)
for temp in ip_list[1:]:
    content = ''
    for i in range(2,7):
        content += (str(temp.xpath(".//td[%d]/text()" %i)[0]).strip() + ' ')
    for i in range(7,9):
        content += (temp.xpath(".//td[%d]//div[starts-with(@class,'bar_inner')]/@style" %i)[0][6:] + ' ')
    for i in range(9,11):
        content += (temp.xpath(".//td[%d]/text()" % i)[0] + ' ')
    content += '\n'
    contentList.append(content)
init_url = 'http://www.xicidaili.com'
for count in range(9):
    next_url = init_url+''.join(html.xpath("//a[@class='next_page']/@href"))
    r = requests.get(next_url,headers=headers)
    html = etree.HTML(r.text)
    ip_list = html.xpath("//table[@id='ip_list']/tr")
    for temp in ip_list[1:]:
        content = ''
        for i in range(2, 7):
            content += (str(temp.xpath(".//td[%d]/text()" % i)[0]).strip() + ' ')
        for i in range(7, 9):
            content += (temp.xpath(".//td[%d]//div[starts-with(@class,'bar_inner')]/@style" % i)[0][6:] + ' ')
        for i in range(9, 11):
            content += (temp.xpath(".//td[%d]/text()" % i)[0] + ' ')
        content += '\n'
        contentList.append(content)
    time.sleep(3)
with open('result.txt','wb') as file:
    for item in contentList:
        file.write(item.encode('utf-8'))
