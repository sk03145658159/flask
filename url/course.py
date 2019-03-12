from flask import Blueprint
from flask import Flask,render_template,redirect,request,session,make_response,send_from_directory  #make_response存cookie用
# from .shujuku import db,cursor
import pymysql
import json
import hashlib
import xlrd
course=Blueprint("course",__name__)
@course.route("/shangchuan",methods=["POST"])
#表格文件上传的课程
def shangchuan():      #操作步骤1:文件=>2：表=>3:行=>4.单元格
    file=request.files["file"]
    file.save("a.xlsx")
    workbook = xlrd.open_workbook(r'a.xlsx')
    sheet1 = workbook.sheet_by_index(0)
    for item in range(1,sheet1.nrows):   #循环行
        # arr=[]
        con= sheet1.row_values(item)  #得到循环的每一行
        # db = pymysql.connect(host='localhost',
        #                       user='root',
        #                       password='03145658159shen',
        #                       db='youyike',
        #                       charset='utf8mb4',
        #                       cursorclass=pymysql.cursors.DictCursor)
        # cursor = db.cursor()
        # cursor.execute("insert into course (cname) values (%s)",(con[0]))
        # cid=db.insert_id()
        # step=con[1].split("\n")   #通过换行拆分内容
        # part=con[2].split("\n")
        # for index in range(len(step)):
        #     arr.append((step[index],part[index],cid))
        # cursor.executemany("insert into courseinfo (step,stepcon,cid) values (%s,%s,%s)",arr)   #批量处理
        # db.commit()
        chuli(con)
    return "ok"
#下载表格样式模板
@course.route("/onload")
def onload():
    # file=open("a.xlsx","rb")
    # con=file.read()
    res = make_response(send_from_directory('.', 'a.xlsx', as_attachment=True))

    res.headers['content-disposition'] = 'attachment;filename=2.xlsx'    #表明是个附件，而不是html文件

    return res
#单个上传的课程
@course.route("/submitone")
def submitone():
    result=request.args.get("result")
    result=json.loads(result)
    chuli(result)
    return "ok"
#处理上传课程的数据信息
def chuli(con):
    arr = []
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("insert into course (cname) values (%s)", (con[0]))
    cid = db.insert_id()
    step = con[1].split("\n")  # 通过换行拆分内容
    part = con[2].split("\n")
    for index in range(len(step)):
        arr.append((step[index], part[index], cid))
    cursor.executemany("insert into courseinfo (step,stepcon,cid) values (%s,%s,%s)", arr)  # 批量处理
    db.commit()
#查询已有的课程信息
@course.route("/selectcourse")
def selectcourse():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from course,courseinfo where course.cid=courseinfo.cid")
    result=cursor.fetchall()
    return json.dumps(result)
@course.route("/deletecourse")
def deletecourse():
    id=request.args.get("id")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("delete from courseinfo where id=%s",(id))
    db.commit()
    return "ok"
@course.route("/changecourse")
def changecourse():
    id=request.args.get("id")
    cid=request.args.get("cid")
    cname=request.args.get("cname")
    step=request.args.get("step")
    stepcon=request.args.get("stepcon")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("update course set cname=%s where cid=%s",(cname,cid))
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
    cursor.execute("update courseinfo set step=%s,stepcon=%s where id=%s", (step,stepcon,id))
    db.commit()
    return "ok"
