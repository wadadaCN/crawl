# code = python3
# encoding = utf-8
# wrote by Xie on 2017/11/7

import requests
from lxml import etree
from time import sleep

from nosql_redis import get_redis
redisCLI = get_redis()
headers = {
"Host": "www.zhihu.com",
"Referer": "https://www.zhihu.com/",
"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"}

def get66ip():
    url = 'http://www.66ip.cn/nmtq.php?getnum=100&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=0&proxytype=1&api=66ip'
    count = 1
    while count < 10:
        r = requests.get(url)
        domTree = etree.HTML(r.text)
        rawIpList = domTree.xpath("//body/text()")
        ip_list = []
        for ip in rawIpList:
            ip_list.append(ip.strip() if ip.strip() else [])
        for ip in ip_list:
            if ip:
                ip = 'https://' + ip
                redisCLI.sadd('ip_list',ip)
        count += 1
        sleep(3)

def ipTest(redis):
    testURL = 'https://www.zhihu.com/'
    while 1:
        ip = redis.spop('ip_list').decode('utf-8')
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

if __name__ == '__main__':
    get66ip()
    # ipTest(redisCLI)
