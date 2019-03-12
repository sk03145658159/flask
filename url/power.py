from flask import Blueprint
from flask import Flask,render_template,redirect,request,session,make_response  #make_response存cookie用
# from .shujuku import db,cursor
import pymysql
import json
import hashlib
power=Blueprint("power",__name__)
#权限查询
@power.route("/selectpower")
def selectpower():
    global arr
    arr=[]
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from power where name=%s",(rid1))
    result=cursor.fetchall()
    results = digui(result, 0)
    return json.dumps(results)
arr = []
def digui(data, pid, now=None):
    global arr
    for item in data:
        if item["pid"] == pid:
            if not "children" in item:
                item["children"] = []
            if item["pid"] == 0:
                item["con"] = item["con"]
                item["name"] = item["name"]
                arr.append(item)
            else:
                item["con"] = item["con"]
                item["name"] = item["name"]
                now.append(item)
            digui(data, item["id"], item["children"])
    return arr
