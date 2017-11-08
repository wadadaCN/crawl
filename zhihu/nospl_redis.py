# code = python3
# encoding = bytes
# wrote by Xie on 2017/11/7
# connected to the redis

import redis

def get_redis():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        print("成功连接redis数据库！")
        return r
    except:
        print('redis数据库连接失败！')

def redis2csv(startStr,nameStr):
    r = get_redis()
    with open('{}.csv'.format(nameStr), 'wb') as file:
        file.write(bytes(startStr,'utf-8'))
        while 1:

            item = r.spop('{}'.format(nameStr))
            if item != None:
                try: #某些字符写入不支持
                    file.write(item)
                except:
                    continue
            else:
                break

    print("写入完成")


if __name__ == '__main__':
    # r = get_redis()
    # r.sadd('test', '1s')
    # r.sadd('test', '2s')
    startStr = "start\n"
    redis2csv(startStr, 'info_list')
