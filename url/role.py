from flask import Blueprint
from flask import Flask,render_template,redirect,request,session,make_response  #make_response存cookie用
# from .shujuku import db,cursor
import pymysql
import json
import hashlib
role=Blueprint("role",__name__)
#查看角色
@role.route("/selectrole")
def selectrole():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from role")
    result=cursor.fetchall()
    return json.dumps(result)
#添加角色
@role.route("/addrole")
def addrole():
    name=request.args.get("name")
    power=request.args.getlist("info")
    power1="|".join(power)
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("insert into role (name,power) values (%s,%s)",(name,power1))
    db.commit()
    # return redirect("/selectrole")
    return redirect("http://localhost:8080/selectrole#/juese")
#查询修改的角色信息
@role.route("/select")
def select():
    id=request.args.get("id")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from role where id=%s",(id))
    result=cursor.fetchone()
    result1=json.dumps(result)
    return result1
#修改角色信息
@role.route("/updaterole")
def updaterole():
    id=request.args.get("id")
    name = request.args.get("name")
    power = request.args.getlist("info")
    power1 = "|".join(power)
    print(id,name,power1)
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("update role set name=%s,power=%s where id=%s",(name,power1,id))
    db.commit()
    # return redirect("/selectrole")
    return redirect("http://localhost:8080/selectrole#/juese")
#删除角色
@role.route("/delrole")
def delrole():
    id=request.args.get("id")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("delete from role where id=%s",(id))
    db.commit()
    return "ok"