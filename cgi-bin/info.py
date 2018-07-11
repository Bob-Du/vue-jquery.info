"""
前后端交互接口规则定义:
前端请求使用get方法,所有请求必须携带req参数
reqData['req'] == 1:
    表示前端请求整体查询数据库刷新页面,将返回json格式数组
reqData['req'] == 2:
    表示请求删除一条记录,请求内容应包含reqData['id'],将返回json格式参数'status':1表示删除成功
reqData['req'] == 3:
    表示请求插入一条新的记录,请求内容中还应该包含
    reqData['name'] reqData['sex'] reqData['age'] reqData['email'] 等全部记录内容
    没有id值 id值由数据库层分配
    TODO 目前暂不支持有的字段内容为空 数据库支持 但后台程序现在写的不行 需要处理下 还在考虑前端处理还是后端处理
    将返回json格式参数'status':1表示插入成功
reqData['req'] == 4:
    需要更新一条记录 先把记录原有内容查询取出 请求内容包含 reqData['id']
    将返回json格式字典,包含这条记录全部键值对
reqData['req'] == 5:
    前端发回要更新记录全部内容
    将返回json格式参数'status':1表示修改成功
"""

import cgi
import cgitb
import json

import redis


cgitb.enable()

print("Content-Type: text/html")
print()

fs = cgi.FieldStorage()  # 接收请求报文携带的数据

reqData = {}  # data字典存储整理后的请求信息
for key in fs:
    reqData[key] = fs[key].value


def selData():
    # 请求查询全部数据

    r = redis.Redis(host='db.bobdu.cc', decode_responses=True)

    userList = r.keys()

    resData = []
    for user in userList:
        if user != 'id':
            oneData = r.hgetall(user)

            oneData['id'] = user
            resData.append(oneData)

            resData.sort(key=lambda x:int(x['id']))

    print(json.dumps(resData))


def delData():
    # 删除一条数据

    r = redis.Redis(host='db.bobdu.cc', decode_responses=True)
    id2 = reqData['id']

    r.delete(id2)

    print(json.dumps({'status': 1}))



def insData():
    # 添加一条数据

    r = redis.Redis(host='db.bobdu.cc', decode_responses=True)
    r.setnx('id', 0)
    r.incr('id')

    id2 = r.get('id')
    del reqData['req']
    r.hmset(id2, reqData)

    print(json.dumps({'status': 1}))


def updData1():
    # 更新一条数据 先获取内容

    r = redis.Redis(host='db.bobdu.cc', decode_responses=True)

    id2 = reqData['id']

    resData = r.hgetall(id2)
    resData['id'] = id2

    print(json.dumps(resData))


def updData2():
    # 更新一条数据 提交更新内容

    id2 = reqData['id']
    r = redis.Redis(host='db.bobdu.cc', decode_responses=True)

    del reqData['req'], reqData['id']

    r.hmset(id2, reqData)

    print(json.dumps({'status': 1}))


if reqData['req'] == '1':
    selData()
elif reqData['req'] == '2':
    delData()
elif reqData['req'] == '3':
    insData()
elif reqData['req'] == '4':
    updData1()
elif reqData['req'] == '5':
    updData2()
