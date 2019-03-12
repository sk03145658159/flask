from flask import Blueprint
from flask import Flask,render_template,redirect,request,session,make_response,send_from_directory  #make_response存cookie用
# from .shujuku import db,cursor
import pymysql
import json
shiti=Blueprint("shiti",__name__)
@shiti.route("/selecttype")
def selecttype():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from titype")
    result=cursor.fetchall()
    return json.dumps(result)
@shiti.route("/selectcourse")
def selectcourse():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from course")
    result=cursor.fetchall()
    return json.dumps(result)
@shiti.route("/courseinfo")
def courseinfo():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from courseinfo")
    result=cursor.fetchall()
    return json.dumps(result)
@shiti.route("/addshiti",methods=["POST"])
def addshiti():
    typeid=request.form["type"]
    cid = request.form["course"]
    stepid=request.form["step"]
    tigan=request.form["title"]
    grade=request.form["grade"]
    answer=request.form["answer"]
    sele=""
    if typeid=='1' or typeid=='2':
        select1 = request.form["select1"]
        select2 = request.form["select2"]
        select3 = request.form["select3"]
        select4 = request.form["select4"]
        sele=select1+"|"+select2+"|"+select3+"|"+select4
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("insert into tibase (typeid,cid,stepid,tigan,grade,sele,answer) values (%s,%s,%s,%s,%s,%s,%s)",(typeid,cid,stepid,tigan,grade,sele,answer))
    db.commit()
    return "ok"