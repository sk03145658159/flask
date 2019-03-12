from flask import Blueprint
from flask import Flask,render_template,redirect,request,session,make_response  #make_response存cookie用
# from .shujuku import db,cursor
import pymysql
import json
import hashlib
user=Blueprint("user",__name__)
#用户的注册添加
@user.route("/adduser",methods=["POST"])
# def adduser():
#     name=request.form["name"]
#     password=request.form["password"]
#     phone = request.form["phone"]
#     profession = request.form["profession"]
#     md5 = hashlib.md5()
#     md5.update(password.encode("utf-8"))
#     password = md5.hexdigest()
#     db = pymysql.connect(host='localhost',
#                          user='root',
#                          password='03145658159shen',
#                          db='youyike',
#                          charset='utf8mb4',
#                          cursorclass=pymysql.cursors.DictCursor)
#     cursor = db.cursor()
#     cursor.execute("insert into user (name,password,phone,rid) values (%s,%s,%s,%s)",(name,password,phone,profession))
#     db.commit()
#     return render_template("tishi.html")
def adduser():
    name=request.form['name']
    password=request.form['password']
    phone=request.form['phone']
    rid=request.form['inlineRadioOptions']
    md5=hashlib.md5()
    md5.update(password.encode("utf-8"))
    upss=md5.hexdigest()
    db = pymysql.connect(host='localhost',
                                  user='root',
                                  password='03145658159shen',
                                  db='youyike',
                                  charset='utf8mb4',
                                  cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("insert into user (name,password,phone,rid) values (%s,%s,%s,%s)",(name,upss,phone,rid))
    db.commit()
    return redirect("http://localhost:8080/#/selectuser")
#查看用户
@user.route("/selectuser")
def selectuser():
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from user")
    result=cursor.fetchall()
    return json.dumps(result)
#删除用户
@user.route("/delete")
def delete():
    id=request.args.get("id")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("delete from user where id=%s",(id))
    db.commit()
    return "ok"
#查找修改用户
@user.route("/selectchange")
def selectchange():
    id=request.args.get("id")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from user where id=%s",(id))
    result=cursor.fetchone()
    return json.dumps(result)
#修改用户信息
@user.route("/changeuser",methods=["POST"])
def changeuser():
    id=request.form["id"]
    name = request.form["name"]
    phone= request.form["phone"]
    rid = request.form["inlineRadioOptions"]
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("update user set name=%s,phone=%s,rid=%s where id=%s",(name,phone,rid,id))
    db.commit()
    return redirect("http://localhost:8080/#/selectuser")
#精确查询
@user.route("/jingque")
def jingque():
    name=request.args.get("name")
    db = pymysql.connect(host='localhost',
                         user='root',
                         password='03145658159shen',
                         db='youyike',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("select * from user where name=%s", (name))
    result=cursor.fetchall()
    return json.dumps(result)