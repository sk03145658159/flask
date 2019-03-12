from flask import Blueprint
from flask import Flask,render_template,redirect,request,session,make_response,send_from_directory  #make_response存cookie用
# from .shujuku import db,cursor
import pymysql
import json
test=Blueprint("test",__name__)
@test.route("/selectinfo")
def selectinfo():
    phone=request.args.get("phone")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from shijuan,student where shijuan.classid=student.classid and student.phone=%s",(phone))
    result=cursor.fetchone()
    return json.dumps(result)