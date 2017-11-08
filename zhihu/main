# code = python3
# encoding = utf-8
# wrote by Xie on 2017/11/7
# proxies, all users' follows.

import requests
import re
from time import sleep

from getProxies import redisCLI,ipTest,get66ip
from nosql_redis import redis2csv

headers = {
'authorization':'Bearer Mi4xcEpzcUFBQUFBQUFBRUVKVmJTSkhEQmNBQUFCaEFsVk5pUEVMV2dEcUFKV0xaQUp5QW9Talg5WlRtbV9nM1NTSk1R|1508140168|a5cc04d035818b42b088adfa011750eca648bcdc',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
}

def main(userToken,proxy,r):
    url = "https://www.zhihu.com/api/v4/members/{}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20".format(userToken)
    offset = 0
    while 1:
        response = ""
        try:
            response = requests.get(url, headers=headers, timeout=2, proxies=proxy).text
        except:
            proxy = ipTest(r)
            continue
        response = re.sub('false','" "',response)
        response = re.sub('true','" "',response)
        response = eval(response)
        users = response['data']
        totalFollower = response['paging']['totals']
        for userItem in users:
            answer_count = userItem['answer_count']
            headline = userItem['headline']
            articles_count = userItem['articles_count']
            name = userItem['name']
            follower_count = userItem['follower_count']
            url_token = userItem['url_token']
            id = userItem['id']
            info = "{0},{1},{2},{3},{4},{5},{6}\n".format(name,headline,answer_count,articles_count,follower_count,url_token,id)
            if not r.sismember('visited',url_token):
                r.sadd('info_list',info)
                r.sadd('user_list',url_token)

        if offset < totalFollower:
            offset += 20
            url = "https://www.zhihu.com/api/v4/members/{}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={}&limit=20".format(userToken, offset)
        else:
            break


if __name__ == '__main__':
    # get66ip()
    startUserToken = 'zhang-jia-wei'
    info = "用户名,简介,回答数,文章数,粉丝数,用户唯一认证,id\n"
    proxy = ipTest(redisCLI)
    main(startUserToken, proxy, redisCLI)
    while 1:
        sleep(3)
        try:
            userToken = redisCLI.spop('user_list')
            if not redisCLI.sismember('visited',userToken):
                redisCLI.sadd('visited',userToken)
                userToken = userToken.decode() #将bytes对象转换为str对象
                main(userToken, proxy, redisCLI)
        except:
            break
    redis2csv(info,'visited')
