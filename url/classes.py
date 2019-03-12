from flask import Blueprint
from flask import Flask,render_template,redirect,request,session,make_response,send_from_directory  #make_response存cookie用
# from .shujuku import db,cursor
import pymysql
import json
import hashlib
import datetime
import xlrd
classes=Blueprint("classes",__name__)
@classes.route("/shangchuan",methods=["POST"])
def shangchuan():
    file=request.files["file"]
    file.save("classes.xlsx")
    workbook = xlrd.open_workbook(r'classes.xlsx')
    sheet1 = workbook.sheet_by_index(0)
    datas = []
    for item in range(1, sheet1.nrows):
        con = sheet1.row_values(item)
        if(isinstance(con[0],float)):   #判断是否为浮点型，是返回True
            con[0]=int(con[0])          #将浮点型转化为整形
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='03145658159shen',
                             db='youyike',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        cursor.execute("select cid from course where cname=%s",(con[1]))   #查询对应课程方向的cid
        result=cursor.fetchone()
        cursor.close()
        db.close()
        # db = pymysql.connect(host='localhost',       另一种快速查找cid的方法,避开了循环
        #                      user='root',
        #                      password='03145658159shen',
        #                      db='youyike',
        #                      charset='utf8mb4')      去掉了一字典的形式返回结果的设置，为了下面dict的使用
        # cursor = db.cursor()
        # cursor.execute("select cname,cid from course")
        # result = cursor.fetchall()
        # result = dict(result)                 dict(arr)   arr=[("a",1),("b",2)]  arr=[["a",1],["b",2]]    转化成字典形式
        # cid=result[con1]
        # cursor.close()
        # db.close()
        con[1]=result["cid"]
        con[2]=xlrd.xldate_as_datetime(con[2], 0).strftime("%Y-%m-%d %H:%M:%S")   #datime处理时间对象
        con[3] = xlrd.xldate_as_datetime(con[3], 0).strftime("%Y-%m-%d %H:%M:%S")
        datas.append(con)
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.executemany("insert into classes (name,cid,start,end) values (%s,%s,%s,%s)",datas)
    db.commit()
    return "ok"
@classes.route("/onload")
def onload():
    res = make_response(send_from_directory('.', 'classes.xlsx', as_attachment=True))

    res.headers['content-disposition'] = 'attachment;filename=classes2.xlsx'  # 表明是个附件，而不是html文件

    return res
@classes.route("/oneadd",methods=["POST"])
def oneadd():
    name=request.form["name"]
    start=request.form["start"]
    end=request.form["end"]
    cid=request.form["inlineRadioOptions"]
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("insert into classes (name,cid,start,end) values (%s,%s,%s,%s)",(name,cid,start,end))
    db.commit()
    return "ok"
@classes.route("/selectclasses")
def selectclasses():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from classes,course where course.cid=classes.cid")
    result=cursor.fetchall()
    return json.dumps(result,default=str)   #pymysql将查询出来的开训时间默认为时间对象易于处理，default=str指定所有查出来的信息都为字符串