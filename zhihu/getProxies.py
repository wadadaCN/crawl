# code = python3
# encoding = utf-8
# created by Xie on 2017/11/7

import requests
from lxml import etree
from time import sleep
from tomorrow import threads

from nosql_redis import get_redis
redisCLI = get_redis()


@threads(5)
def download(url, headers):
    return requests.get(url,headers=headers)

def res2tree(urlList):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
    responseList = [download(url,headers) for url in urlList]
    domTreeList = [etree.HTML(r.text) for r in responseList]
    return domTreeList

def get66ip():
    url = 'http://www.66ip.cn/nmtq.php?getnum=100&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=0&proxytype=1&api=66ip'
    urlList = [url] * 5
    count = 1
    while count < 10:
        domTreeList = res2tree(urlList)
        rawIpList2D = [domTree.xpath("//body/text()") for domTree in domTreeList]
        ip_list = []
        for rawIpList in rawIpList2D:
            for i in range(len(rawIpList)):
                for ip in rawIpList[i]:
                    ip_list.append(ip.strip() if ip.strip() else [])
        for ip in ip_list:
            if ip:
                ip = 'https://' + ip
                redisCLI.sadd('ip_list',ip)
        count += 1
        sleep(3)

def getxici():
    initUrl = 'http://www.xicidaili.com/nn/{}'
    for j in range(1,101,5):
        urlList = [initUrl.format(i) for i in range(j,j+5)]
        domTreeList = res2tree(urlList)
        for domTree in domTreeList:
            ipList = domTree.xpath("//table[@id='ip_list']/tr/td[2]/text()")
            portList = domTree.xpath("//table[@id='ip_list']/tr/td[3]/text()")
            httpList = domTree.xpath("//table[@id='ip_list']/tr/td[6]/text()")
            for i in range(len(ipList)):
                try:
                    if httpList[i].lower()[4] == 's':
                        ip = 'https://' + ipList[i] + ':' + portList[i]
                except IndexError:
                    ip = 'http://' + ipList[i] + ':' + portList[i]
                redisCLI.sadd('ip_list', ip)
        sleep(3)
    print('当次ip获取成功！')

def ipTest(redis):
    testURL = 'https://www.zhihu.com/'
    headers = {
        "Host": "www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"}
    while 1:
        ip = redis.spop('ip_list')
        if ip != None:
            ip = ip.decode()
            if ip[4] == 's':
                proxy = {'https': ip}
            else:
                proxy = {'http': ip}
            try:
                r = requests.get(testURL,proxies = proxy, timeout=2, headers=headers)
                if r.status_code == 200:
                    return proxy
            except:
                print("%s无效"%proxy)
        else:
            get66ip()

if __name__ == '__main__':
    # get66ip()
    getxici()
    # ipTest(redisCLI)
