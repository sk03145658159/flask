from flask import Blueprint
from flask import Flask,render_template,redirect,request,session,make_response,send_from_directory  #make_response存cookie用
# from .shujuku import db,cursor
import pymysql
import json
shijuan=Blueprint("shijuan",__name__)
@shijuan.route("/select")
def select():
    typeid=request.args.get("typeid")
    cid=request.args.get("cid")
    stepid=request.args.get("stepid")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from tibase where typeid=%s and cid=%s and stepid=%s",(typeid,cid,stepid))
    result=cursor.fetchall()
    return json.dumps(result)
@shijuan.route("/selecttigan")
def selecttigan():
    con=request.args.get("con")
    arr=con.split("|")
    result=[]
    for item in arr:
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='03145658159shen',
                             db='youyike',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        cursor.execute("select * from tibase where id=%s",item)
        result.append(cursor.fetchone())
    print(result)
    return json.dumps(result)
@shijuan.route("/selectclasses")
def selectclasses():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from classes")
    result=cursor.fetchall()
    return json.dumps(result,default=str)
@shijuan.route("/success")
def success():
    starttime=request.args.get("starttime")
    endtime=request.args.get("endtime")
    classid=request.args.get("classid")
    ticon=request.args.get("ticon")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("insert into shijuan (starttime,endtime,classid,ticon) values (%s,%s,%s,%s)",(starttime,endtime,classid,ticon))
    db.commit()
    return "ok"