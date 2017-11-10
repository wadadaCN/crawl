import time
import requests

headers = {
'Cookie':'',

'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
'X-Requested-With':'XMLHttpRequest'}
timeStamp = int(time.time() * 1000)
url = 'https://www.amazon.cn/gp/deal/ajax/claimDeal.html/ref=gbps_atc_s-4_a9df_0d9799d2?nocache={}'.format(timeStamp)
data = {'dealId':'0d9799d2',
'itemId':'B00DU5H802',
'clientId':'goldbox_mobile_pc'}
response = requests.post(url, headers=headers, data=data)


print(1)
