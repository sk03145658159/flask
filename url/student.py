from flask import Blueprint
from flask import Flask,render_template,redirect,request,session,make_response,send_from_directory  #make_response存cookie用
# from .shujuku import db,cursor
import pymysql
import json
import hashlib
import datetime
import xlrd
student=Blueprint("student",__name__)
@student.route("/shangchuan",methods=["POST"])
def shangchuan():
    file=request.files["file"]
    file.save("student.xlsx")
    workbook = xlrd.open_workbook(r'student.xlsx')
    sheet1 = workbook.sheet_by_index(0)
    datas1 = []
    datas2=[]
    for item in range(1, sheet1.nrows):
        con = sheet1.row_values(item)
        if (isinstance(con[3], float)):  # 判断是否为浮点型，是返回True
            con[3] = int(con[3])  # 将浮点型转化为整形
        if (isinstance(con[2], float)):  # 判断是否为浮点型，是返回True
            con[2] = int(con[2])  # 将浮点型转化为整形
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='03145658159shen',
                             db='youyike',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        cursor.execute("select id from classes where name=%s", (con[3]))  # 查询对应课程方向的cid
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
        md5 = hashlib.md5()
        md5.update(b"111111")
        password = md5.hexdigest()
        datas1.append([con[0],password,con[2]])
        datas2.append(con)
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.executemany("insert into user (name,password,phone,rid) values (%s,%s,%s,1)",(datas1))
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
    cursor.executemany("insert into student (sname,sex,phone,classid,school) values (%s,%s,%s,%s,%s)", (datas2))
    db.commit()
    return "ok"
@student.route("/onload")
def onload():
    res = make_response(send_from_directory('.', 'student.xlsx', as_attachment=True))

    res.headers['content-disposition'] = 'attachment;filename=student2.xlsx'  # 表明是个附件，而不是html文件

    return res
@student.route("/oneadd",methods=["POST"])
def oneadd():
    sname=request.form["name"]
    sex=request.form["sex"]
    phone=request.form["phone"]
    classid=request.form["classid"]
    school=request.form["school"]
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
    cursor.execute("insert into user (name,password,phone,rid) values (%s,%s,%s,1)", (sname, password, phone))
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
    cursor.execute("select id from classes where name=%s",(classid))
    result=cursor.fetchone()
    classid=result["id"]
    cursor.close()
    db.close()
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("insert into student (sname,phone,classid,sex,school) values (%s,%s,%s,%s,%s)",(sname,phone,classid,sex,school))
    db.commit()
    return "ok"
@student.route("/selectstudent")
def selectstudent():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from student,classes where student.classid=classes.id")
    result=cursor.fetchall()
    return json.dumps(result,default=str)
@student.route("/deletestudent")
def deletestudent():
    phone=request.args.get("phone")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("delete from student where phone=%s",(phone))
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
@student.route("/changestudent")
def changestudent():
    sname=request.args.get("sname")
    sex = request.args.get("sex")
    phone = request.args.get("phone")
    school = request.args.get("school")
    classname = request.args.get("classname")
    id = request.args.get("id")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select id from classes where name=%s",(classname))
    result=cursor.fetchone()
    classid=result["id"]
    cursor.close()
    db.close()
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("update user set name=%s where phone=%s",(sname,phone))
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
    cursor.execute("update student set sname=%s,sex=%s,phone=%s,school=%s,classid=%s where id=%s", (sname,sex,phone,school,classid,id))
    db.commit()
    return "ok"

@student.route("/teastudent")
def teastudent():
    phone=request.args.get("phone")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select student.*,classes.name from student,teacher,classes where student.classid=classes.id and teacher.clid=classes.id and teacher.phone=%s",(phone))
    result=cursor.fetchall()
    return json.dumps(result)