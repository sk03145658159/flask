from flask import Blueprint
from flask import Flask,render_template,redirect,request,session,make_response,send_from_directory  #make_response存cookie用
# from .shujuku import db,cursor
import pymysql
import json
import hashlib
import datetime
import xlrd
teacher=Blueprint("teacher",__name__)
@teacher.route("/shangchuan",methods=["POST"])
def shangchuan():
    file=request.files["file"]
    file.save("teacher.xlsx")
    workbook = xlrd.open_workbook(r'teacher.xlsx')
    sheet1 = workbook.sheet_by_index(0)
    datas1 = []
    datas2=[]
    for item in range(1, sheet1.nrows):
        con = sheet1.row_values(item)
        if (isinstance(con[1], float)):  # 判断是否为浮点型，是返回True
            con[1] = int(con[1])  # 将浮点型转化为整形
        if (isinstance(con[3], float)):  # 判断是否为浮点型，是返回True
            con[3] = int(con[3])  # 将浮点型转化为整形
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='03145658159shen',
                             db='youyike',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        cursor.execute("select id,cid from classes where name=%s", (con[3]))  # 查询对应课程方向的cid
        result = cursor.fetchone()
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
        con[3] = result["id"]
        con[2]=result["cid"]
        md5 = hashlib.md5()
        md5.update(b"111111")
        password = md5.hexdigest()
        datas1.append([con[0],password,con[1]])
        datas2.append(con)
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.executemany("insert into user (name,password,phone,rid) values (%s,%s,%s,2)",(datas1))
    db.commit()
    cursor.close()
    db.close()
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.executemany("insert into teacher (tname,phone,cid,clid) values (%s,%s,%s,%s)", (datas2))
    db.commit()
    return "ok"
@teacher.route("/onload")
def onload():
    res = make_response(send_from_directory('.', 'teacher.xlsx', as_attachment=True))

    res.headers['content-disposition'] = 'attachment;filename=teacher2.xlsx'  # 表明是个附件，而不是html文件

    return res
@teacher.route("/oneadd",methods=["POST"])
def oneadd():
    tname=request.form["name"]
    phone=request.form["phone"]
    clid=request.form["clid"]
    cid=request.form["inlineRadioOptions"]
    md5 = hashlib.md5()
    md5.update(b"111111")
    password = md5.hexdigest()
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("insert into user (name,password,phone,rid) values (%s,%s,%s,2)",(tname,password,phone))
    db.commit()
    cursor.close()
    db.close()
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select id from classes where name=%s",(clid))
    result=cursor.fetchone()
    clid=result["id"]
    cursor.close()
    db.close()
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("insert into teacher (tname,phone,cid,clid) values (%s,%s,%s,%s)", (tname,phone,cid,clid))
    db.commit()
    return "ok"
@teacher.route("/selectteacher")
def selectteacher():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from teacher,classes,course where teacher.cid=course.cid and teacher.clid=classes.id")
    result=cursor.fetchall()
    return json.dumps(result,default=str)
@teacher.route("/deleteteacher")
def deleteteacher():
    phone=request.args.get("phone")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("delete from teacher where phone=%s",(phone))
    db.commit()
    cursor.close()
    db.close()
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("delete from user where phone=%s", (phone))
    db.commit()
    return "ok"
@teacher.route("/changeteacher")
def changeteacher():
    tname=request.args.get("tname")
    phone= request.args.get("phone")
    phone2 = request.args.get("phone2")
    coursename = request.args.get("coursename")
    classname = request.args.get("classname")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("update user set name=%s,phone=%s where phone=%s",(tname,phone,phone2))
    db.commit()
    cursor.close()
    db.close()
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select id,cid from classes where name=%s",(classname))
    result=cursor.fetchone()
    cid=result["cid"]
    clid=result["id"]
    cursor.close()
    db.close()
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("update teacher set tname=%s,phone=%s,cid=%s,clid=%s where phone=%s", (tname, phone,cid,clid,phone2))
    db.commit()
    return "ok"

