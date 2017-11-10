import time
import requests
import re
import json
import sys

headers = {
'Cookie':'',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
'X-Requested-With':'XMLHttpRequest'}
timeStamp = int(time.time() * 1000)
url = 'https://www.amazon.cn/gp/goldbox/ref=nav_cs_top_nav_gb27?nocache={}'.format(timeStamp)
data = {"requestMetadata":{},"dealTargets":[{"dealID":"74a82029"},{"dealID":"af921176"},{"dealID":"b673dc0b"}],"responseSize":"STATUS_ONLY","itemResponseSize":"DEFAULT_WITH_PREEMPTIVE_LEAKING"}
response = requests.post(url, headers=headers, data=data)

string = response.text
sortedDealIDs = eval(re.findall(r'"sortedDealIDs.*?\[.*?\]', string, re.S)[0].strip().split(':')[1]) #获取dealID
# file = open('data.txt','w')
# sys.stdout = file
print('现价 原价 折扣 好评度 评论数 dealID itemID')
for i in range(0,len(sortedDealIDs),5):
    timeStamp = int(time.time() * 1000)
    url = 'https://www.amazon.cn/xa/dealcontent/v2/GetDeals?nocache={}'.format(timeStamp)
    dealID = sortedDealIDs[i:i+5]
    data = {"requestMetadata": {},
     "dealTargets": [{"dealID": "{}".format(dealID[0])}, {"dealID": "{}".format(dealID[1])}, {"dealID": "{}".format(dealID[2])}, {"dealID": "{}".format(dealID[3])}, {"dealID": "{}".format(dealID[4])}], "responseSize": "STATUS_ONLY",
     "itemResponseSize": "DEFAULT_WITH_PREEMPTIVE_LEAKING"}
    data = json.dumps(data) # 需要传入json格式的数据
    time.sleep(3)
    response = requests.post(url, headers=headers, data=data)
    dealDetails = json.loads(response.text) #获取传入的5个id的详情
    for item in dealDetails['dealDetails']:
        if dealDetails['dealStatus'][item]['dealState'] == 'AVAILABLE':
            itemDict = dealDetails['dealDetails'][item]
            title = itemDict['title']
            # print(title)
            # for kind in itemDict['items']:
            if len(itemDict['items']) > 0:
                print(title)
                kind = itemDict['items'][0]
                dealPrice = kind['dealPrice']
                currentPrice = kind['currentPrice']
                itemID = kind['itemID']
                discountPercent = str(int(dealPrice * 100/currentPrice)) + '%'
                rating = str(kind['reviewRating'])[:3]
                totalReviews = kind['totalReviews']
                print(dealPrice, currentPrice, discountPercent, rating, totalReviews, item,itemID,sep=' ')
                # break



# file.close()
print(1)
