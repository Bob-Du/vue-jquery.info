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

import pymysql


cgitb.enable()

print("Content-Type: text/html")
print()

fs = cgi.FieldStorage()  # 接收请求报文携带的数据

reqData = {}  # data字典存储整理后的请求信息
for key in fs:
    reqData[key] = fs[key].value


def selData():
    # 请求查询全部数据

    db = pymysql.connect('db.bobdu.cc', 'root', '123456', 'info_db',
                         charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()

    sql = 'select * from info'
    cursor.execute(sql)
    resData = cursor.fetchall()

    print(json.dumps(resData))
    db.close()


def delData():
    # 删除一条数据

    db = pymysql.connect('db.bobdu.cc', 'root', '123456', 'info_db',
                         charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()

    id2 = reqData['id']
    sql = f'delete from info where id = {id2}'
    cursor.execute(sql)
    db.commit()
    print(json.dumps({'status': 1}))
    db.close()


def insData():
    # 添加一条数据

    db = pymysql.connect('db.bobdu.cc', 'root', '123456', 'info_db',
                         charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()

    name = reqData['name']
    sex = reqData['sex']
    age = reqData['age']
    email = reqData['email']
    sql = f'insert into info value (null, "{name}", {sex}, {age}, "{email}")'
    cursor.execute(sql)
    db.commit()
    print(json.dumps({'status': 1}))
    db.close()


def updData1():
    # 更新一条数据 先获取内容

    db = pymysql.connect('db.bobdu.cc', 'root', '123456', 'info_db',
                         charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()

    id2 = reqData['id']
    sql = f'select * from info where id = {id2}'
    cursor.execute(sql)
    resData = cursor.fetchone()

    print(json.dumps(resData))
    db.close()


def updData2():
    # 更新一条数据 提交更新内容

    db = pymysql.connect('db.bobdu.cc', 'root', '123456', 'info_db',
                         charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()

    id2 = reqData['id']
    name = reqData['name']
    sex = reqData['sex']
    age = reqData['age']
    email = reqData['email']
    sql = f'update info set name = "{name}", sex = {sex}, age = {age}, email = "{email}" where id = {id2}'
    cursor.execute(sql)
    db.commit()
    print(json.dumps({'status': 1}))
    db.close()


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
