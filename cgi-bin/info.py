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
        charset = 'utf8', cursorclass = pymysql.cursors.DictCursor)
    cursor = db.cursor()

    sql = 'select * from info'
    cursor.execute(sql)
    resData = cursor.fetchall()

    print(json.dumps(resData))
    db.close()


def delData():
    # 删除一条数据

    db = pymysql.connect('db.bobdu.cc', 'root', '123456', 'info_db',
        charset = 'utf8', cursorclass = pymysql.cursors.DictCursor)
    cursor = db.cursor()

    id2 = reqData['id']
    sql = f'delete from info where id = {id2}'
    cursor.execute(sql)
    db.commit()
    print(json.dumps(1))
    db.close()


def insData():
    # 添加一条数据

    db = pymysql.connect('db.bobdu.cc', 'root', '123456', 'info_db',
        charset = 'utf8', cursorclass = pymysql.cursors.DictCursor)
    cursor = db.cursor()

    name = reqData['name']
    sex = reqData['sex']
    age = reqData['age']
    email = reqData['email']
    sql = f'insert into info value (null, "{name}", {sex}, {age}, "{email}")'
    cursor.execute(sql)
    db.commit()
    print(json.dumps({'status':1}))
    db.close()

def updData1():
    # 更新一条数据 先获取内容

    db = pymysql.connect('db.bobdu.cc', 'root', '123456', 'info_db',
        charset = 'utf8', cursorclass = pymysql.cursors.DictCursor)
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
        charset = 'utf8', cursorclass = pymysql.cursors.DictCursor)
    cursor = db.cursor()

    id2 = reqData['id']
    name = reqData['name']
    sex = reqData['sex']
    age = reqData['age']
    email = reqData['email']
    sql = f'update info set name = "{name}", sex = {sex}, age = {age}, email = "{email}" where id = {id2}'
    cursor.execute(sql)
    db.commit()
    print(json.dumps({'status':1}))
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
