# code = python3
# encoding = utf-8
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


if __name__ == '__main__':
    r = get_redis()
    r.sadd('test', '1')
    r.sadd('test', '2')
