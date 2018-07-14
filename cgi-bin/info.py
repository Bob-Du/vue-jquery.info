#! /usr/bin/env python3

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

import pymongo
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

    r = redis.Redis(host='db.bobdu.cc', port=6379, decode_responses=True)

    if r.exists('cache'):
        resData = eval(r.get('cache'))
    else:
        mongoclient = pymongo.MongoClient('db.bobdu.cc', 27017)
        db = mongoclient.infoapp
        resData = list(db.info.find({},
            {'_id': 0, 'id': 1, 'name': 1, 'age': 1, 'email': 1}))
        r.setex('cache', resData, 3)

    print(json.dumps(resData))

def delData():
    # 删除一条数据

    mongocliet = pymongo.MongoClient('db.bobdu.cc', 27017)
    db = mongocliet.infoapp

    id2 = int(reqData['id'])
    db.info.remove({'id': id2})
    print(json.dumps({'status': 1}))


def insData():
    # 添加一条数据

    mongoclient = pymongo.MongoClient('db.bobdu.cc', 27017)
    db = mongoclient.infoapp

    newIdList = list(db.new.find())
    if newIdList:
        newId = newIdList[0]['newId']
        db.new.update(
            {'newId': newId},
            {
                '$set': {'newId': newId + 1}
            }
        )
    else:
        newId = 1
        db.new.insert({'newId': 2})

    del reqData['req']
    reqData['id'] = newId
    reqData['age'] = int(reqData['age'])
    db.info.insert(reqData)

    print(json.dumps({'status': 1}))


def updData1():
    # 更新一条数据 先获取内容

    mongoclient = pymongo.MongoClient('db.bobdu.cc', 27017)
    db = mongoclient.infoapp

    id2 = int(reqData['id'])
    resData = dict(db.info.find({'id': id2},
        {'_id': 0, 'id': 1, 'name': 1, 'age': 1, 'email': 1})[0])

    print(json.dumps(resData))


def updData2():
    # 更新一条数据 提交更新内容

    mongoclient = pymongo.MongoClient('db.bobdu.cc', 27017)
    db = mongoclient.infoapp

    id2 = int(reqData['id'])
    name = reqData['name']
    sex = reqData['sex']
    age = int(reqData['age'])
    email = reqData['email']

    db.info.update(
        {'id': id2},
        {
            '$set': {
                'name': name,
                'sex': sex,
                'age': age,
                'email': email
            }
        }
    )

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
