import time
import requests
import re
import json
import sys

headers = {
'Cookie':'at-main=Atza|IwEBIF5KqooPDlyjroswlawJW-DKqQBS-RZs8ssb8h5YSj7u4xHolDC0GfpSnSG5PmWxrAnitgG626bGo3t_1aTtSfB6e5Mj3gP70Abeq91oY59n5YwI2ntrPcnSWFcT4WjlUNlswhM306iPq6LG-GczrzDUReuE900JRkLY8moU0KbTFcs6025iQUfvN_qh9noqIGPxleSUnUo754JHd2N_arRqcxgsbAMkWHdxW8pp_ahxWuk6FlHZ6OP0RBCE1kOk6duWOa6HSAWJfnLfri_Rbq2hviE2Q1LvJhBWgt4h7y5w2PVFK88mIf_BF5yYT7_IG0Ychr_0WSo52uFChbkghsisRwMRx5qrbmM3YlYYqcEE65oEeof-JX_wpFJsHA2jRwoxfmAC8de0-8sadSzDaJdhODtpcl7L9UfFJ8f55vbskxN2dmJC2aK0u24Abbj4qjE; x-wl-uid=1U/F2W1jdIyrO6zC/gXLaMSmw2JBjWLOL2e+3Ho5NAN0XPAw2v6yFVi0lRfI48lPxdjmMpI6YH8BL+XyIKgqCrqRkCvy4yjEVl5yiLwvPT7N69dGhNU2oGJgpKBvxLVukp5Gx+4uFpPQ=; x-acbcn="vIepWL0zJn37Pp8U1Di2f?e3Phh1N5Pe?2z@qOhQ4rucaJo68ZvpwUjIwWG6W?o9"; session-token="l6747EcUB6Q55nkTJd5aSqYpqznvjnrr0pw3JITxAQjFTKR83vQDMcSY43kG1dL/+G6dwGe/ljFWrbYFu4mrQeKWuNWwYD0YcJnKIYUiEPbp8BF0GxVsB70DJu4dYMcqnLJc6anK3f5SHIEY9BTRcZVuy7KKC8exAFSMemyw65QVxKTUA1t+xc/+RSdA8C6XgaXSVIRiBtmOpMpuwrsPytw7Iu+qwrb5HCO68abPzKl7Z7Gg3okG67q7YYYOvfli5tcrCOG+0Wo="; lc-acbcn=zh_CN; csm-hit=344YXEN3SWVM86C1JQXH+b-MPAR10SXJ57M6XDAC0VH|1510227939913; ubid-acbcn=458-3810591-1096205; session-id-time=2082729601l; session-id=457-3724616-1143400',

'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
'X-Requested-With':'XMLHttpRequest'}
timeStamp = int(time.time() * 1000)
url = 'https://www.amazon.cn/gp/goldbox/ref=nav_cs_top_nav_gb27?nocache={}'.format(timeStamp)
data = {"requestMetadata":{"marketplaceID":"AAHKV2X7AFYLW","clientID":"goldbox_mobile_pc","customerID":"AGM2VH52NQ2N5","sessionID":"457-3724616-1143400"},"dealTargets":[{"dealID":"74a82029"},{"dealID":"af921176"},{"dealID":"b673dc0b"}],"responseSize":"STATUS_ONLY","itemResponseSize":"DEFAULT_WITH_PREEMPTIVE_LEAKING"}
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
    data = {"requestMetadata": {"marketplaceID": "AAHKV2X7AFYLW", "clientID": "goldbox_mobile_pc",
                         "customerID": "AGM2VH52NQ2N5", "sessionID": "457-3724616-1143400"},
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
